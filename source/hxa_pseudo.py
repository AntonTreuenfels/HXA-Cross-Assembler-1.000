# Hobby Cross-Assembler (HXA) V1.002- Pseudo Opcode Handler

# (c) 2004-2024 by Anton Treuenfels

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

# source language: Python 3.11.4

# first created: 03/08/03	(in Thompson AWK 4.0)
# last revision: 02/05/24

# preferred public function prefix: PSOP

# -----------------------------
# other HXA modules
import hxa_usermesg as UM
import hxa_macro as MAC
import hxa_codegen as CG
import hxa_progctr as PC
import hxa_source as SRC
import hxa_symbol as SYM
import hxa_file as OS
import hxa_expressions as EXP
import hxa_strings as STR
import hxa_misc as UTIL

# -----------------------------
# we put these here so their references in _psOpcode are known
# - not the style we prefer, but the easiest fix

# -----------------------------
# psop: PSALIAS psop=alias [[, psop=alias]...]
# -----------------------------

def dopsalias(label, equate):
	''' handle PSALIAS psop '''
	psop, alias = equate
	if not ispseudo(psop):
		UM.undefined( psop )
	else:
		ok, alias = SYM.getglobal( alias )
		if ok and SYM.goodname( alias ):
			addalias( _normalize(psop), _normalize(alias) )

# -----------------------------
# psop: [label] PSNULL [expr [[, expr]...]]
# -----------------------------

def dopsnull(label=None, expr=None):
	''' handle PSNULL psop '''
	# do absolutely nothing...
	pass

# -----------------------------
# psop: ASSUME flag[:=]val [[, flag[:=]val]...]
# -----------------------------

def doassume(label, fields):
	''' handle ASSUME psop '''
	f = [ x.lower() for x in fields ]
	flag, val = f
	if not STR.doassume(flag, val):
		if not CG.doassume(flag, val):
			UM.warn( 'BadAssume', fields )

# built-in pseudo opcodes

# psop processing rules coding for label and expression types:

# - if capitalized, argument type is required
# - if not capitalized, argument type is checked whenever present

# "a" = accepted if present (optional; not evaluated)
# "e" = expression (any type)
# "f" = filename (defaults to name of first file used if not present)
# "g" = global name (literal or string expression)
# "h" = hex character string (opt-string)
# "i" = ignored if present (warning message generated)
# "l" = label (assigned current pc value; branch target labels are odd use)
# "m" = numeric argument only (no forward reference; strings compared to null)
# "n" = numeric argument (forward reference ok)
# "o" = opt-string (string expression or "as-is")
# "p" = numeric argument (no forward reference; negative odd)
# "q" = equate string (opt-string)
# "r" = argument required (but not evaluated)
# "s" = string constant (numbers converted to one-char Unicode strings)
# "u" = user label (assigned expression value; branch target labels are odd use)

# "?" = one argument only (evaluated)
# "+" = one or more type-identical arguments allowed (each evaluated)
# "&" = one or more string-ish arguments allowed (all evaluated, then concatenated)
# "!" = one or more type-different arguments allowed (each evaluated)
# "*" = one or more arguments (none evaluated)

# "^" = suffix to pass psop to handler (if not present, pass label instead)
# - used when multiple psops point to the same handler

_psOpcode = {
	# format of associated value:
	# ( label check, expr check, expression field collection, psop execution )

	# cpu

	'cpu': ( 'i', 'O', '?', CG.docpu ),

	# equ

	'equ':	( 'U', 'R', '?', EXP.doequ ),
	'plusequ':	('U', 'R', '?', EXP.doplusequ ),
	'minusequ':	('U', 'R', '?', EXP.dominusequ ),

	# files

	'errfile':		( 'i', 'f', '?^', OS.dofile ),
	'listfile':		( 'i', 'f', '?^', OS.dofile ),
	'objfile':		( 'i', 'f', '?^', OS.dofile ),
	'rawfile':		( 'i', 'f', '?^', OS.dofile ),
	'hexfile':		( 'i', 'f', '?^', OS.dofile ),
	'srecfile':		( 'i', 'f', '?^', OS.dofile ),
	'objbyseg':		( 'i', 'f', '?^', OS.dofile ),
	'rawbyseg':		( 'i', 'f', '?^', OS.dofile ),
	'hexbyseg':		( 'i', 'f', '?^', OS.dofile ),
	'srecbyseg':	( 'i', 'f', '?^', OS.dofile ),
	'objbyblk':		( 'i', 'f', '?^', OS.dofile ),
	'rawbyblk':		( 'i', 'f', '?^', OS.dofile ),
	'hexbyblk':		( 'i', 'f', '?^', OS.dofile ),
	'srecbyblk':	( 'i', 'f', '?^', OS.dofile ),

	'readonce':	( 'í', 'í', '*', OS.doreadonce ),
	'include':	( 'i', 'F', '?', OS.doinclude ),
	'incbin':	( 'i', 'Fmm', '!', OS.doincbin ),

	# program counter / segments

	'absorg':		( 'u', 'P', '?', PC.doabsorg ),
	'relorg':		( 'i', 'i', '*', PC.dorelorg ),
	'absend':		( 'u', 'P', '?', PC.doabsend ),
	'relend':		( 'i', 'i', '*', PC.dorelend ),
	'padto':		( 'i', 'Ph', '!', PC.dopadto ),
	'padfrom':		( 'i', 'Ph', '!', PC.dopadfrom ),
	'ds':			( 'l', 'P', '?', PC.dods ),
	'usesegments': 	( 'i', 'i', '*', PC.dousesegments ),
	'segment':		( 'i', 'G', '?', PC.dosegment ),
	'endsegment':	( 'i', 'g', '?', PC.doendsegment),
	'uninitialized':	('i', 'i', '*', PC.douninitialized ),
	'common':		( 'i', 'i', '*', PC.docommon ),

	# END

	'end':	( 'l', 'b', '?', OS.doend ),

	# macros and blocks

	'macro':	( 'a', 'a', '*,', MAC.domacro ),
	'endmacro':	( 'a', 'a', '?', MAC.doendmacro ),
	'putback':	( 'i', 'a', '*', SRC.doputback ),
	'putbacks':	( 'i', 'S', '&', SRC.doputback ),
	'exit':		( 'i', 'i', '*', MAC.doexit ),
	'exitif':	( 'i', 'C', '?', MAC.doexitif ),
	'ifdef':	( 'i', 'R', '?^', MAC.doifxdef ),
	'ifndef':	( 'i', 'R', '?^', MAC.doifxdef ),
	'undef':	( 'i', 'G', '+', MAC.doundef ),
	'repeat':	( 'a', 'R', '?', MAC.dorepeat ),
	'endrepeat':( 'a', 'i', '*', MAC.doendrepeat ),
	'while':	( 'a', 'R', '?', MAC.dowhile ),
	'endwhile':	( 'a', 'i', '*', MAC.doendwhile ),
	'if':		( 'i', 'R', '*', MAC.doif ),
	'elseif':	( 'i', 'R', '*', MAC.doelseif ),
	'else':		( 'i', 'i', '*', MAC.doelse ),
	'endif':	( 'i', 'i', '*', MAC.doendif ),

	# user-initiated
	
	'echo': 	( 'i', 'o', '?', UM.doecho ),
	'warn':		( 'i', 'o', '?', UM.dowarn ),
	'error':	( 'i', 'o', '?', UM.doerror ),
	'fatal':	( 'i', 'o', '?', UM.dofatal ),
	'assert':	( 'i', 'N', '?', CG.doassert ),
	'starttimer':	( 'i', 'G', '?', UTIL.dostarttimer ),
	'stoptimer':	( 'i', 'G', '?', UTIL.dostoptimer ),
	'showtimer':	( 'i', 'G', '?', UTIL.doshowtimer ),
	'warnon':		('i', 'i', '*^', UM.dowarnstate ),
	'warnoff':		('i', 'i', '*^', UM.dowarnstate ),
	'debugon':		( 'i', 'i', '*^', UM.dodebug ),
	'debugoff':		(' i', 'i', '*^', UM.dodebug ),

	# user customization

	'psalias':	( 'i', 'Q', '+', dopsalias ),
	'psnull':	( 'a', 'a', '*', dopsnull ),
	'mesgtext':	( 'i', 'Q', '+', UM.domesgtext ),
	'assume':	( 'i', 'Q', '+', doassume ),
	'xlate':	( 'i', 'Q', '+', STR.doxlate ),
	'maxwarn':	( 'i', 'P', '?^', UTIL.domax ),
	'maxerr':	( 'i', 'P', '?^', UTIL.domax ),
	'maxdepth':	( 'i', 'P', '?^', UTIL.domax ),
	'maxloop':	( 'i', 'P', '?^', UTIL.domax ),
	'maxputback':	( 'i', 'P', '?^', UTIL.domax ),
	'maxseg':	( 'i', 'P', '?^', UTIL.domax ),
	'maxstack':	( 'i', 'P', '?^', UTIL.domax ),
	'liston':	( 'i', 'o', '+^', SRC.dolist ),
	'listoff':	( 'i', 'o', '+^', SRC.dolist ),

	# listing

	'title':	( 'i', 'o', '?', SRC.dotitle ),
	'pagesize':	( 'i', 'Pp', '!', SRC.dopagesize ),
	'margins':	( 'i', 'PPpp', '!', SRC.domargins ),
	'linespace':	( 'i', 'P', '?', SRC.dolinespace ),
	'page':		( 'i', 'i', '*', SRC.dopage ),

	# storage

	'string':	( 'l', 'S', '&', CG.dostring ),
	'stringr':	( 'l', 'S', '&', CG.dostringr ),
	'fill':		( 'l', 'Ph', '!', PC.dofill ),
	'hex':		( 'l', 'H', '+', CG.dohex ),
	'pushs':	( 'i', 'S', '&', UTIL.dopushs ),
}

# built-in (and user-defined) aliases for pseudo ops

_psAlias = {

	'=':	'equ',
	'+=':	'plusequ',
	'-=':	'minusequ',
	'*=':	'absorg',
	'$=':	'absorg',
	'elif':	'elseif',
	'endm':	'endmacro',
	'endr':	'endrepeat',
	'ends':	'endsegment',
	'endseg': 'endsegment',
	'endw': 'endwhile',
	'hexbyblock': 'hexbyblk',	# candidate for removal
	'mac':	'macro',
	'nodata':	'uninitialized',
	'nowarn':	'warnoff',
	'objbyblock': 'objbyblk',	# candidate for removal
	'onexpand':	'putback',		# candidate for removal
	'org':	'absorg',
	'putstr' : 'putbacks',
	'revstr':	'stringr',
	'srecbyblock': 'srecbyblk',	# candidate for removal
	'str':	'string',
}

# psop argument type collection and error messages

_psArgType = {

	'A': ( "BadField",	None ),				# ACCEPT anything or nothing, no evaluation
	'B': ( "NeedNumVal", EXP.getaddr ),		# ONLYNUM, forward ok, strings are errors
	'C': ( "NeedCond",	EXP.getconstnum ),	# CONDITION, no forward, strings converted to numbers
	'F': ( "NeedFile",	EXP.getfname ),		# FILENAME, no forward, OPTIONAL-type string
	'G': ( "NeedGlobal", EXP.getconstglb ),	# GLOBAL NAME, no forward
	'H': ( "NeedHex",	EXP.gethexstr ),	# HEXADECIMAL, no forward
	'L': ( "NeedLabel",	SYM.labelhere ),	# LABEL, any type
	'M': ( "NeedNumVal", EXP.getonlynum ),	# ONLYNUM, no forward, strings are errors
	'N': ( "NeedNum",	EXP.getnum ),		# NUMBER, forward ok, strings converted to numbers
	'O': ( "NeedStr",	EXP.getoptstr ),	# OPTIONAL raw string or evaluated string expresssion
	'P': ( "NeedPos",	EXP.getposnum ),	# POSITIVE number, no forward 
	'Q': ( "NeedEqu",	EXP.getequate ),	# EQUATE expression, no forward
	'R': ( "BadField",	None ),				# REQUIRED something, no evaluation
	'S': ( "NeedStr",	EXP.getconststr ),	# STRING; no forward, numbers NOT converted to strings
	'U': ( "NeedLabel",	SYM.warnanon ),		# LABEL, anonymous labels odd
}

# -----------------------------

# module variables

class PSOPvariables(object):

	def __init__(self):

		self.targetpsop = None		# not None if skipping source lines

_PSOP = PSOPvariables()

# -----------------------------

def addalias(psop, alias):
	''' add (normalized) alias for a pseudo-op '''
	_psAlias[ alias ] = psop

def addbitop(psop):
	''' add a -BIT-- psop to known psops'''
	# all -BIT-- psops have the same signature
	# -'N' accepts strings (and compares them to the null string)
	_psOpcode[ psop ] = ('l', 'N', '+^', CG.store )

# -----------------------------

def _normalize(this):
	''' convert token to normalized form '''

	# prefixes allowed for visual distinctiveness but are otherwise ignored
	# - "manifest type", if you wish

	if this.startswith(('.', '#')):
		this = this[1:]

	this = this.lower()

	return _psAlias[this] if this in _psAlias else this

def ispseudo(this):
	''' check if token is a recognized pseudo opcode '''
	return _normalize(this) in _psOpcode
 
# -----------------------------

def skipto(stops):
	''' enable source line skipping until a psop in the stop list is found '''
	_PSOP.targetpsop = stops.copy()

def taking():
	''' check whether processing or skipping source line '''
	return _PSOP.targetpsop is None
		
def skipping(psop):
	''' check whether to process or skip this psop '''
	# once enabled, only another psop can turn skipping off
	# if we are taking, we are not skipping
	if _PSOP.targetpsop is None:
		return False

	# can we stop now ?
	if psop in _PSOP.targetpsop:
		_PSOP.targetpsop = None
		return False

	# continue skipping
	return True

# -----------------------------

def getvalueof(type, expr):
	''' collect psop argument value '''

	argfail, handler = _psArgType[type.upper()] if type.upper() in _psArgType else ('NoWay', None)

	# do we have an expression ?
	if expr is not None:

		# can we evaluate it ?
		if handler is not None:
			return handler( expr )			# a (flag, value) tuple

		# is the type 'A' or 'R' ?
		elif type != 'i':					# ...it turns out an ignored expression can't also be required...
			return (True, expr)				# (return as-is)

		UM.ignored( expr )					# ignore expression and return default value

	# do we need an expression ?
	# - required if type char is uppercase AND in dictionary
	elif type in _psArgType:
		UM.error( argfail )
		return (False, None)

	# return a default value
	# - things are OK (just not of any further use)
	return (True, None)

# -----------------------------

def dopseudo(label, psop, exprfield):
	''' dispatch psop '''
	basepsop = _normalize( psop )
	if skipping(basepsop):
		return

	lbltype, argtype, argctrl, handler = _psOpcode[ basepsop ]

	ok, label = getvalueof( lbltype, label )
	if not ok:
		return

	# no expression ?
	if exprfield is None:
		# do we need one ?
		if argtype in _psArgType:
			UM.error( _psArgType[argtype][0] )
			return
	# are we not going to use it ?
	elif argtype == 'i':
		UM.ignored( exprfield )

	# make a list of the expressions in the expression field
	# - if splitting not required by psop, just checks for errors
	ok, expr = STR.splitfield( exprfield )
	if not ok:
		return

	# first parameter should be 'basepsop' or 'label' ?
	firstarg = basepsop if argctrl.endswith('^') else label

	match argctrl[0]:
		# no evaluation ?
		case '*':
			handler( firstarg, expr if argctrl == '*,' else exprfield )

		# single argument evaluated ?
		case '?':

			expr = UTIL.maxfields( expr, 1 )
			ok, argval = getvalueof( argtype, expr.pop() )
			if ok:
				handler( firstarg, argval )

		# each argument evaluated, call after each ?
		case '+':

			while len(expr):
				ok, argval = getvalueof( argtype, expr.pop(0) )
				if ok:
					handler( firstarg, argval )

		# fixed number of (possibly different) arguments evaluated, then single call ?
		# - tries to evaluate each provided argument even if one fails
		case '!':

			expr = UTIL.maxfields( expr, len(argtype) )

			argvals = []
			for type in argtype:
				oknow, argval = getvalueof( type, expr.pop(0) if len(expr) > 0 else None )
				if oknow:
					argvals.append( argval )
				else:
					ok = False

			if ok:	# call with unpacked args
				handler( firstarg, *argvals )

		# concatenate multiple string-ish arguments, then single call ?
		case '&':

			argcat = []
			while len(expr) > 0:
				oknow, argval = getvalueof( argtype, expr.pop(0) )
				if oknow:
					argcat.append( argval if argval is not None else '' )
				else:
					ok = False

			if ok:	# call with concatenated string
				handler( firstarg, ''.join(argcat) )

		# oops!
		case '_':
			UM.noway( basepsop )
