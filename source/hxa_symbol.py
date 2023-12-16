# Hobby Cross-Assembler (HXA) V1.00 - Symbol Table Management

# (c) 2004-2023 by Anton Treuenfels

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# -----------------------------

# by Anton Treuenfels

# 5248 Horizon Dr
# Fridley, MN 55421

# e-mail: teamtempest@yahoo.com

# source language: Python 3.7.1

# first created: 03/08/03	(in Thompson AWK 4.0)
# last revision: 08/05/23

# preferred public function prefix: SYM

# -----------------------------
import re
# other HXA modules
import hxa_progctr as PC
import hxa_usermesg as UM
import hxa_pseudo as PSOP
import hxa_macro as MAC
import hxa_codegen as CG
import hxa_source as SRC
from hxa_expressions import isfunc
# -----------------------------

# public constants

# for ease of consistent definition, all recognized symbol/label patterns
# are defined here (even if not used in this module)

# global numeric - [A-Z_]([.]?[A-Z_0-9])*[:]?
# global string  - [A-Z_]([.]?[A-Z_0-9])*[$][:]?

# local numeric  - [@]([.]?[A-Z_0-9])*[:]?
# local string   - [@]([.]?[A-Z_0-9])*[$][:]?

# variable numeric  - []]([.]?[A-Z_0-9])*[:]?
# variable string   - []]([.]?[A-Z_0-9])*[$][:]?

# anonymous numeric - [:]|[+][-]?|[-][+]?
# anonymous string  - (none)

strLabel  = '([]@][0-9]*|[_A-Z])([.]?[_A-Z0-9])*[$][:]?'	# string label

glbLabel  = '[_A-Z]([.]?[_A-Z0-9])*[$]?[:]?'		# global label

anonLabel = [ ':', '+', '-', '+-', '-+' ]			# anonymous label (in label field)

# legal label - all the forms available to the user (in label field)
# - global, local and variable numeric labels
# - global, local and variable string labels
# - anonymous labels (different than in expression field)

symLabel = '[]@_A-Z]([.]?[_A-Z0-9])*[$]?[:]?|:|[-][+]?|[+][-]?'

# legal label - all the forms available to the user (in expression field)
# - global, local and variable numeric labels
# - global, local and variable string labels
# - anonymous labels (different than in label field)

symExpr  = '[]@_A-Z]([.]?[_A-Z0-9])*[$]?[:]?|:([+]+|[-]+)'

# ...except one...which is legal only when it is a lone operand...

anonExpr = '[+]+|[-]+'

# macro formal arguments

macLabel = '[?][_A-Z]([.]?[_A-Z0-9])*'				# straight text replacement
equLabel = '[]@][_A-Z]([.]?[_A-Z0-9])*[$]?'			# evaluate and assign

macReplacePrefix = '?'								# macLabel prefix

# -----------------------------

# module variables

class SYMvariables(object):

	def __init__(self):

		self.reserved = [ ]							# reserved symbols
		self.labels = {}							# user defined symbols
		self.refcnt = {}							# symbol reference count

		self.fwdcnt = 0								# forward anonymous label count
		self.bakcnt = 0								# backward anonymous label count
		self.localcnt = 0							# local label count

		self.locals = [ {} ]						# local label unique replacements

_SYM = SYMvariables()

# -----------------------------

def _normalize(this):
	''' normalize symbol token '''
	return this.rstrip(":").upper()

# -----------------------------

def islabel(this):
	''' check if token is a label '''
	return bool( re.fullmatch(symLabel, this, flags=re.IGNORECASE) )

def isglobal(label):
	'''global label?'''
	return bool( re.fullmatch(glbLabel, label, flags=re.IGNORECASE) )

def isstr(label):
	'''string label?'''
	return label.endswith( ('$', '$:') )

def isvar(label):
	'''variable label?'''
	return label.startswith(']')

def _islocal(label):
	'''local label?'''
	return label.startswith('@')

def isauto(label):
	'''anonymous label?'''
	return label.startswith('&')			# internal form

def isreserved(label):
	''' reserved symbol? '''
	return _normalize(label) in _SYM.reserved or PSOP.ispseudo(label) or CG.isop(label) or isfunc(label)

def ismacroreplace(label):
	''' macro text replacement label? '''
	return bool( re.fullmatch(macLabel, label) )

def ismacroequate(label):
	''' macro eval/assign label? '''
	return bool( re.fullmatch(equLabel, label) )

# -----------------------------

def goodname(name):
	''' verify name is legal to define/reserve '''
	if not isglobal(name):
		UM.error( 'NeedGlobal', name)
	elif isreserved(name):
		UM.reserved( name )
	elif name in _SYM.labels or MAC.ismacro(name):
		UM.duplicate( name )
	else:
		return True

	return False

def addreserve(labels):
	''' add reserved labels '''
	for label in labels:
		name, val = label
		name = _normalize( name )
		if goodname( name ):				# sanity check
			_SYM.reserved.append( name )
			_SYM.labels[ name ] = val

# -----------------------------

def _makeforward(num):
	''' make unique forward label '''
	return f'&{num:03X}:+'

def _makebackward(num):
	''' make unique backward label '''
	return f'&{num:03X}:-'

def _makelocal(label):
	''' make unique local label '''
	key = _normalize(label)

	# this key not in local table already ?
	if key not in _SYM.locals[-1]:
		_SYM.localcnt += 1
		_SYM.locals[ -1 ][ key ] = f'&{_SYM.localcnt:03X}_{key}'

	return _SYM.locals[ -1 ][ key ]

def unmakeauto(this):
	'''remove internal auto prefix (if any; for error reporting)'''
	return re.sub('&[0-9]+[_]?', '', str(this)).upper()

# -----------------------------

def pushlocals():
	_SYM.locals.append( {} )

def poplocals():
	_SYM.locals.pop()

# -----------------------------

def normalize(label):
	''' normalize all forms of labels legal in expressions '''
	# local ?
	if _islocal(label):
		return _makelocal( label )

	# forward anonymous ?
	m = re.search( '[+]+', label )
	if m is not None:
		return _makeforward( _SYM.fwdcnt + (m.end() - m.start()) )

	# backward anonymous ?
	m = re.search( '[-]+', label )
	if m is not None:
		return _makebackward( _SYM.bakcnt + 1 - (m.end() - m.start()) )

	# must be variable or global 
	return _normalize(label)

# -----------------------------

def add(label, val):
	''' add a label to symbol table '''
	# a null label ?
	if label is None:
		return

	# variable label ?
	if isvar(label):
		_SYM.labels[ _normalize(label) ] = val

	# anonymous label ?
	elif label in anonLabel:

#		if label in [':', '+', '+-', '-+']:
		if label != '-':
			_SYM.fwdcnt += 1
			_SYM.labels[ _makeforward(_SYM.fwdcnt) ] = val

#		if label in [':', '-', '+-', '-+']:
		if label != '+':
			_SYM.bakcnt += 1
			_SYM.labels[ _makebackward(_SYM.bakcnt) ] = val

	# ...must be a local or global label
	else:

		# local label ?
		if _islocal(label):
			key = _makelocal( label )

		# ...must be a global
		else:

			key = _normalize( label )
			if isreserved( key ):
				UM.reserved( label )
				return

			_SYM.locals[-1].clear()			# clear local labels
			SRC.glbequate( key )			# xref

		# a new label ?
		if key not in _SYM.labels:
			_SYM.labels[ key ] = val

		# multiple assignment okay as long as always same value
		# - we're simply not going to change anything already fixed

		elif _SYM.labels[key] != val:
			UM.odduse( label )
			UM.duplicate( label )

# -----------------------------

def here(label, byitself=False):
	''' assign current program counter value to label '''
	if label is not None:
		addr = PC.get()		# a (segment, offset) tuple

		# if this is an absolute address, store it as 
		# a string or an integer depending on the label's type
		if not PC.gotrel(addr):
			addr = PC.getabs( addr )
			if isstr(label):
				addr = str( addr )

		# ...otherwise the label's relative value will not be resolved
		# until the pc becomes absolute (which is what we want)
		add( label, addr )

		# was the label on a line by itself ?
		if byitself:
			CG.store( 'strlbl' if isstr(label) else 'numlbl', addr )

# -----------------------------

def warnanon(label):
	''' warn if label is anonymous '''
	if label in anonLabel:
		UM.odduse( label )
	return ( True, label )

def checkloneanon(expr):
	'''check for lone anonymous label in expression field'''
	# we don't want to confuse them with unary prefix operators
	return expr if re.fullmatch(anonExpr, expr) is None else f':{expr}'

def labelhere(label):
	''' add label with value of current program counter '''
	_ = warnanon( label )
	here( label )
	return (True, label )

def isglobalnumeric(this):
	'''verify symbol is global numeric'''
	return isinstance(this, str) and isglobal(this) and not isstr(this)

def getglobal(this):
	''' verify symbol is global numeric'''
	if isglobalnumeric(this):
		return ( True, _normalize(this) )
	else:
		UM.notglobal( this )
		return ( False, None )

# -----------------------------

def exists(label):
	'''test if label is known'''
	# caller must normalize label !

	# for cross-reference (if enabled)
	if isglobal(label):
		SRC.glbreference( label )	# xref

	# known label ?
	if label in _SYM.labels:
		_SYM.refcnt[ label ] = _SYM.refcnt.get(label, 0) + 1
		return True
		
	# unknown label - forward reference to variable label ?
	elif isvar(label):
		UM.odduse( label )

	return False

def lookup(label):
	''' get known label value '''
	if label in _SYM.labels:
		return _SYM.labels[ label ]
	else:
		UM.debug( ("label", label), ("len", len(label)),  ("symbols", _SYM.labels) )
		UM.noway( label )

# ----------------------------

def verplusminus(label, expr, nostring=False):
	'''verify variable label is correct for PLUSEQU and MINUSEQU'''
	if label not in anonLabel:
		label = _normalize( label )
	if not isvar(label):
		UM.error( "NeedVarble", label )
	elif nostring and isstr(label):
		UM.error( "NeedNumNam", label )
	elif exists(label):
		return ( True, label )

	return ( False, None )

# ----------------------------
# Pass Two-only functions
# ----------------------------

def makeabsolute():
	''' make all pc-dependant label values absolute '''
	for label in _SYM.labels:
		val = _SYM.labels[ label ]
		if PC.isaddr(val):
			absval = PC.getabs( val )
			_SYM.labels[ label ] = str(absval) if isstr(label) else absval

# -----------------------------
# Listing support
# -----------------------------

def acceptnum(sym):
	return isglobal(sym) and not (isstr(sym) or isreserved(sym))

def acceptstr(sym):
	return isglobal(sym) and isstr(sym) and not isreserved(sym)

def acceptnumauto(sym):
	return not isglobal(sym) and not isstr(sym)
	
def acceptstrauto(sym):
	return not isglobal(sym) and isstr(sym)

def getlabels(accept, field):
	'''user symbols in sorted order'''
	labels = []
	for sym in _SYM.labels:
		if accept(sym):
			labels.append( (sym, _SYM.labels[sym], _SYM.refcnt.get(sym, 0)) )

	labels.sort( key= lambda f: f[field] )
	return labels
	
def getnumalpha():
	'''global numeric symbols in alpha order'''
	return getlabels(acceptnum, 0)
	
def getnumvalue():
	'''global numeric symbols in value order'''
	return getlabels(acceptnum, 1)
	
def getnumauto():
	'''variable, local and anonymous numeric symbols in alpha order'''
	return getlabels(acceptnumauto, 0)

def getstralpha():
	'''global string symbols in alphabetic order'''
	return getlabels(acceptstr, 0)

def getstrauto():
	'''variable and local string symbols in alpha order'''
	return getlabels(acceptstrauto, 0)
