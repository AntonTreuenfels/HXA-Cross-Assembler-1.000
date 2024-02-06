# Hobby Cross-Assembler (HXA) V1.002 - Macro and Block Processing

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

# first created: 02/22/03 (in Thompson AWK 4.0)
# last revision: 02/05/24

# preferred public function prefix: "MAC"

# -----------------------------
import re
# other HXA modules
import hxa_usermesg as UM
import hxa_pseudo as PSOP
import hxa_symbol as SYM
import hxa_source as SRC
import hxa_expressions as EXP
import hxa_strings as STR
import hxa_misc as UTIL
# -----------------------------

# constants

# block types

_macDummy = '__DUMMY'

_incBlk = '__INCLUDE'

_ifBlk = '__IFBLK'

_segBlk = '__SEGBLK'

# pseudo ops we're looking for if we want to check another condition

_nextCond = [ 'if', 'ifdef', 'ifndef', 'elseif', 'else', 'endif' ]

# pseudo ops we're looking for if we don't want to check another condition

_endIf = [ 'if', 'ifdef', 'ifndef', 'endif' ]

_macDefBlk = '__MACDEF'
_macExpBlk = '__MACEXP'
_macNestBlk = '__MACNEST'

_rptDefBlk = '__RPTDEF'
_rptExpBlk = '__RPTEXP'

_whlDefBlk = '__WHLDEF'
_whlExpBlk = '__WHLEXP'

# skip targets while defining blocks

_macSkips = [ 'macro', 'endmacro' ]
_rptSkips = [ 'repeat', 'endrepeat' ]
_whlSkips = [ 'while', 'endwhile' ]

# "looking for crossed block" types

_macCrossBlk = '_MAC'
_rptCrossBlk = '_RPT'
_whlCrossBlk = '_WHL'
_expCrossBlk = 'EXP'

# module variables

class MACvariables(object):

	def __init__(self):

		# lowest level of code block stack is "dummy"
		# - so last actual block structure needs no special treatment
		self.blockstack = [ (_macDummy, 0, 0, 0) ]

		self.defineLevel = 0			# track definition nesting
		self.defining = []				# macro(s) being defined

		self.macropool = {}				# macro definitions
		self.actualargs = []			# current macro arguments
		self.expcnt = {}				# expansion count

		self.expandbeg = []				# expansion block start
		self.expandsrc = []				# current source line index
		self.expandend = []				# expansion block end

		self.loopbeg = None				# loop block starts
		self.loopexpr = None			# loop block termination conditions (while defining)
		self.loopcontrol = []			# loop block termination conditions (while executing)
		self.loopcount = []				# loop count

		self.condstack = [[True, True]]	# IF block stack (treats whole program as being in TRUE branch)

		self.xref = []					# cross reference

_MAC = MACvariables()

# -----------------------------
# Code Blocks stack
# -----------------------------

def pushblock(type):
	# - fields: block type, master line, offset in master line, error count at block instantiation
	_MAC.blockstack.append( (type, SRC.getmaster(), SRC.getoffset(), UM.geterr()) )
	UTIL.checkmax( 'maxdepth', len(_MAC.blockstack) - 1 )

def popblock():
	return _MAC.blockstack.pop()

def noerrs():
	''' any errors since block opened ? '''
	return UM.geterr() == _MAC.blockstack[-1][3]

def topblocktype():
	return _MAC.blockstack[-1][0]

def blockstart():
	return _MAC.blockstack[-1][1]

def openblock():
	''' is there an open block on the stack ? '''
	return len(_MAC.blockstack) > 1

def getblockstarts(errline):
	''' get state of block stack (for error reporting)'''
	# the first element is the dummy element at line 0 (so skip it)
	blockstarts = [ (tpl[1], tpl[2]) for tpl in _MAC.blockstack if tpl[1] > 0 and tpl[1] <= errline ]
	erroffset = SRC.getoffset()
	# make sure the line that triggered the error is shown
	if len(blockstarts) < 1 or blockstarts[-1][0] != errline:
		blockstarts.append( (errline, 0) )
	# make sure the error is shown only once
	if blockstarts[-1][1] != erroffset:
		blockstarts.append( (errline, erroffset) )
	return blockstarts

# -----------------------------

def begindefinition(type):
	'''begin block definition'''
	pushblock( type )

	_MAC.defineLevel += 1
	# TRUE if un-nested definition, FALSE if nested definition
	return bool( _MAC.defineLevel == 1 )

def enddefinition(name=None):
	'''end block definition'''
	if not noerrs():
		UM.warn( "BadDef", name )

	_ = popblock()

	_MAC.defineLevel -= 1
	# TRUE if un-nested definition, FALSE if nested definition
	return bool( _MAC.defineLevel == 0 )

# -----------------------------

def newscope(type):
	''' begin new local label scope '''
	pushblock( type )
	SYM.pushlocals()

def oldscope():
	''' restore old local label scope '''
	SYM.poplocals()
	_ = popblock()

# -----------------------------

def beginexpansion(type, start, end):
	''' begin an expansion block '''
	newscope( type )
	_MAC.expandbeg.append( start )
	_MAC.expandsrc.append( start )
	_MAC.expandend.append( end )

def endexpansion(label):
	'''terminate block expansion'''
	if openblock():
		SYM.here( label )
		_ = _MAC.expandend.pop()
		_ = _MAC.expandsrc.pop()
		_ = _MAC.expandbeg.pop()
		oldscope()
	else:
		UM.noway()

def expanding():
	''' one or more mexpansions active ? '''
	return len(_MAC.expandsrc) > 0

def inexpansion():
	''' some operations only allowed within block expansions '''
	if expanding():
		return True
	else:
		UM.error( 'BadOutExp' )
		return False

# -----------------------------

def badblock(sought):
	''' block type mismatch '''
	# we know there is a block mismatch...
	UM.error( "BadBlock" )

	# but it could be just an orphan (misplaced psop)
	# - is the target type in the block stack at all ?
	for e in _MAC.blockstack:
		# if so, then recovery is difficult
		# - many lines potentially affected
		if sought in e[0]:
			UM.fatal( "BadOpenBlk" )

# -----------------------------

def topblock(type):
	''' check type of top block on stack '''
	if type == topblocktype():
		return True
	else:
		badblock( type )
		return False

def endsource():
	'''end of first pass'''
	#kill all active expansions (if any)
	_MAC.expandbeg = []
	_MAC.expandsrc = []
	_MAC.expandend = []

	# check that block stack is empty
	_ = topblock( _macDummy )

# -----------------------------
# Conditional Assembly
# -----------------------------

# conditional stack entry: [ foundTrue, inTrue ]
# - foundTrue: found a true branch (for IF..ELSEIF..ELSE..ENDIF)
# - inTrue: in true branch (for nested IFs)

def intruebranch():
	return _MAC.condstack[ -1 ][ 1 ]

def truenotfound():
	return not _MAC.condstack[ -1 ][ 0] 

def truebranch():
	''' mark conditional branch as TRUE '''
	_MAC.condstack[ -1 ] = [ True, True ]
	SRC.setcond( True )

def falsebranch():
	''' mark conditional branch as FALSE and skip to end '''
	_MAC.condstack[-1][1] = False
	SRC.setcond( False )
	PSOP.skipto( _endIf )

def testcond(result):
	''' test result of conditional evaluation '''
	ok, val = result

	# if couldn't evaluate, we're done with this branch altogether
	if not ok:
		falsebranch()

	# if in TRUE branch mark it and continue 
	elif val:
		truebranch()

	# if in FALSE branch mark it and skip to next condition (or end)
	else:
		_MAC.condstack[ -1 ] = [ False, False ]
		SRC.setcond( False )
		PSOP.skipto( _nextCond )

# -----------------------------
# psop: IF cond
# -----------------------------

def doif(label, expr):
	''' handle IF psop '''
	pushblock( _ifBlk )
	_MAC.condstack.append( [False, intruebranch()] )
	if intruebranch():
		testcond( EXP.getconstnum(expr) )
	else:
		falsebranch()

# -----------------------------
# psop: ELSEIF cond
# -----------------------------

def doelseif(label, expr):
	''' handle ELSEIF psop '''
	if topblock(_ifBlk):
		if truenotfound():
			testcond( EXP.getconstnum(expr) )
		else:
			falsebranch()

# -----------------------------
# psop: ELSE
# -----------------------------

def doelse(label, expr):
	''' handle ELSE psop '''
	if topblock(_ifBlk):
		if truenotfound():
			truebranch()
		else:
			falsebranch()

# -----------------------------
# psop: ENDIF
# -----------------------------

def doendif(label, expr):
	''' handle ENDIF psop '''
	if topblock(_ifBlk):
		_ = _MAC.condstack.pop()
		_ = popblock()
		if intruebranch():
			SRC.setcond( True )
		else:
			PSOP.skipto( _nextCond )

# -----------------------------
# psop: EXITIF cond_expr
# -----------------------------

def doexitif(label, exit):
	'''handle EXITIF psop'''
	if inexpansion() and exit:

		# discard nested block types we don't care about
		type = topblocktype()
		while type in [ _macNestBlk, _ifBlk ]:
			_ = popblock()
			type = topblocktype()

		# top block should now be an expansion block
		# - if not, there's still an unclosed nested block (fatal error)
		# - make sure loop continuation check will evaluate to FALSE
		if type == _rptExpBlk:
			_MAC.loopcontrol[-1][-1] = 0
		elif type == _whlExpBlk:
			_MAC.loopcontrol[-1][-1] = "0"
		elif type != _macExpBlk:
			badblock( _expCrossBlk )

		# set fetch pointer to just before block's 'END--' psop
		_MAC.expandsrc[-1] = _MAC.expandend[-1] - 1

# -----------------------------
# psop: EXIT
# -----------------------------

def doexit(label, expr):
	'''handle EXIT psop'''
	doexitif( None, True )

# -----------------------------
# psop: MACRO name [,arg1 [[,arg2] ... ]]
# psop: name MACRO [arg1 [[,arg2] ... ]]
# -----------------------------

def domacro(name, formalargs):
	'''' handle MACRO psop '''
	# are we expanding a macro now ?
	# - if so, this begins nested definition
	# - note it and continue current expansion
	if expanding():
		pushblock( _macNestBlk )
		return

	# a new macro definition
	# - we try to find as many errors as we can right at start
	begindefinition( _macDefBlk )

	# name MACRO [args] form of definition ?
	if name is not None:
		ok, name = SYM.getglobal( name )

	# "MACRO name [[,?args]..]" form ?
	elif formalargs[0] != None:
		ok, name = EXP.getconstglb( formalargs.pop(0) )
		if ok:
			ok, name = SYM.getglobal( name )

	# macro name error ?
	if name is None:
		UM.error( 'NeedMacName' )
	# validate name
	# - can't already be defined (anywhere)
	# - can't be in process of being defined (as macro)
	elif SYM.goodname(name):
		if name in [ mac[0] for mac in _MAC.defining ]:
			UM.duplicate( name )

	# validate formal argument list names (if any),
	# and collect default actual arguments (if any)
	formals = {}
	hasdefault = False
	for formalarg in formalargs:

		if formalarg is None:
			continue

		# default actual argument supplied ?
		if '=' in formalarg:
			ok, equate = STR.splitequate( formalarg )
			if ok:
				formalarg, default = equate
				hasdefault = True
			else:
				continue

		# any previous formal argument has a default ?
		elif hasdefault:
			UM.error( "NeedArgDflt", formalarg )
			continue

		# ...no, so no default
		else:
			default = None

		# formal name is legal ?
		formalarg = _normalize( formalarg )
		if not (SYM.ismacroreplace(formalarg) or SYM.ismacroequate(formalarg)):
			UM.error( "NeedArgName", formalarg )
			continue

		# formal name is not a duplicate of previous name ?
		if formalarg in formals:
			UM.duplicate( formalarg )
			continue

		formals[ formalarg ] = default

	# record partial definition
	if noerrs():
		SRC.macdefine( name )	# xref
	else:
		name = None
	_MAC.defining.append( (name, formals) )

	# look for end of definition
	PSOP.skipto( _macSkips )

# -----------------------------
# psop: [label] ENDMACRO [name]
# -----------------------------

def doendmacro(label, ename):
	''' handle ENDMACRO psop '''

	def _verifyargs(i, end, args):
		'''verify text replacement args'''

		def _findallfix(m):
			formals.append( m.group().upper() )
			return ''
			
		# put any formal arguments into a more convenient form for checking

		checkargs = args.keys()

		# if there aren't any formal arguments we're still checking for
		# their improper use within the definition body

		while i < end:
			i, text = SRC.fetch( i+1 )
			SRC.setmaster( i )
			# this doesn't work ! :-(
			# formals = re.findall( SYM.macLabel, text, flags=re.IGNORECASE )
			# but this does...
			# - the problem is caused by grouping and can also be fixed by
			# defining the pattern to ignore grouping
			formals = []
			_ = re.sub( SYM.macLabel, _findallfix, text, flags=re.IGNORECASE )
			for formal in formals:
				if not formal in checkargs:
					UM.undefined( formal )

		SRC.setmaster( end )

	match topblocktype():

		# end of a macro expansion ?
		# - terminate expansion
		case "__MACEXP":
			_ = _MAC.actualargs.pop()
			endexpansion( label )

		# end of a nested macro definition during expansion of nesting macro ?
		# - ignore (except for any label )
		case "__MACNEST":
			_ = popblock()
			SYM.here( label )

		# terminating a definition ?
		# - name error at first definition line saves a "bad" name
		# - if name being defined is okay:
		# -   verify any formal arguments in definition body
		# -   if ending name provided, check that it matches current name
		# (note that one check at definition time all is we need to do)
		# - check if this is the first time the name has been defined
		# - finish definition
		# - if nested, also go on to finish enclosing definition
		case "__MACDEF":
			bname, formals = _MAC.defining.pop()
			if ename is not None:
				ok, ename = EXP.getconstglb( ename )
				if ok:
					_ = UTIL.samename( ename, bname )
			blockbeg = blockstart()
			blockend = SRC.getmaster()
			if bname is not None:
				_verifyargs( blockbeg, blockend, formals )

			if noerrs():
				_ = _MAC.expcnt.setdefault( bname, 0 )
				_MAC.macropool[ bname ] = ( blockbeg, blockend, formals )

			if not enddefinition(bname):
				PSOP.skipto( _macSkips )

		# an orphan !
		case _:
			badblock( _macCrossBlk )

# -----------------------------

def _normalize(this):
	return this.upper()

def ismacro(this):
	''' check if token is a recognized macro '''
	# names currently *being* defined are NOT defined
	return _normalize(this) in _MAC.macropool

# -----------------------------
# psop: IFxDEF name
# -----------------------------

def doifxdef(psop, expr):
	'''handle IFDEF and IFNDEF psops'''

	def testdef():
		# IFxDEF is skipped if in a false branch, so we check only now
		ok, name = EXP.getconstglb( expr )
		if ok:
			known = ismacro( name ) or SYM.exists( name )
			return ( True, known if psop == 'ifdef' else not known )
		else:
			return ( False, None )

	pushblock( _ifBlk )
	_MAC.condstack.append( [False, intruebranch()] )
	if intruebranch():
		testcond( testdef() )
	else:
		falsebranch()

# -----------------------------
# psop: UNDEF name
# -----------------------------

def doundef(label, name):
	''' handle UNDEF psop '''
	# record xref event even if 'name' is not (nor ever becomes) a macro
	SRC.macundef( name )
	if ismacro(name):
		del _MAC.macropool[ _normalize(name) ]

# -----------------------------

def invoke(name, exprfield):
	'''invoke a macro expansion'''
	name = _normalize( name )
	macbegin, macend, formals = _MAC.macropool[ name ]

	if exprfield is None:
		actuals = None
	else:
		ok, actuals = STR.splitfield( exprfield )
		if ok:
			actuals = UTIL.maxfields( actuals, len(formals) )
		else:
			return

	# we rely here on dictionaries "remembering" insertion order

	errs = UM.geterr()
	replacements = {}
	for formal in formals:
		if actuals is not None and len(actuals):
			replacements[ formal ] = actuals.pop(0)
		elif formals[formal] is not None:
			replacements[ formal ] = formals[ formal ]
		else:
			UM.error( "NeedArgVal", formal )

	# if all okay so far, begin macro expansion

	if errs == UM.geterr():
		SRC.macexpand( name )	# xref
		beginexpansion( _macExpBlk, macbegin, macend )
		_MAC.actualargs.append( replacements )
		_MAC.expcnt[ name ] += 1

	# do assignments to label formal arguments
	# - assignments occur in the same order the formal arguments do in
	# the macro definition
	# - we wait until now to do the assigment so that implicit and
	# explicit assignment of formal arguments to labels behave identically
	# (particularly the effects of errors during explicit assigment)
	# - note that beginning an expansion creates new local label scope

		for formal in replacements:
			if SYM.ismacroequate(formal):
				EXP.doequ( formal, replacements[formal] )

# -----------------------------
# Repeat and While Blocks
# -----------------------------

# get source text index of loop block delimiter
# - first loop expansion level and macro expansions always fetch
# saved text which was read directly from file
# - we make nested loop expansions fetch from the current position of their
# parent so they will too (and never from expanded text)

def getloopdelim():
	''' get source text index of loop block delimiter '''
	return _MAC.expandsrc[-1] if expanding() else SRC.getmaster()

# save starting loop definition values
# - there is at most only one loop block we're defining at a time
# - note loops nested within this one will not be formally "defined"
# until this one is expanded, so it is okay for control expressions
# of those loops to depend on values that will be set only during
# that expansion
# - note we don't care if evaluation of 'condition' failed since
# if it did, the loop definition will be ignored once we reach its end

def begloopdef(label, condition):
	''' start loop block definition '''
	SYM.here( label )
	_MAC.defining.append( [SRC.getmaster(), SRC.getoffset(), getloopdelim(), condition] )

def endloopdef(skips):
	''' end loop block definition '''
	ok = noerrs()

	if enddefinition():
		control = _MAC.defining.pop()
		return control if ok else None
	else:
		PSOP.skipto( skips )

def begloopexp(type, control):
	''' start loop expansion '''
	beginexpansion( type, control[2], getloopdelim() )
	_MAC.loopcontrol.append( control.copy() )
	_MAC.loopcount.append( 1 )
	UTIL.checkmax( 'maxloop', _MAC.loopcount[-1] )

def nextexpansion():
	''' restart loop expansion '''
	_MAC.expandsrc[ -1 ] = _MAC.expandbeg[ -1 ]
	_MAC.loopcount[ -1 ] += 1
	UTIL.checkmax( 'maxloop', _MAC.loopcount[-1] )

def endloopexp(label):
	''' end loop expansion '''
	_ = _MAC.loopcount.pop()
	_ = _MAC.loopcontrol.pop()
	endexpansion( label )

# -----------------------------
# psop: [label] REPEAT count
# -----------------------------

def dorepeat(label, expr):
	''' handle REPEAT psop '''
	# - note that only the outermost repeat is defined, but that any
	# nested repeats will be defined in turn as they are encountered
	# when the outer repeat is expanded (so they work properly)
	if begindefinition(_rptDefBlk):
		ok, count = EXP.getonlynum( expr )
		begloopdef( label, count )
	PSOP.skipto( _rptSkips )

# -----------------------------
# psop: [label] ENDREPEAT
# -----------------------------

def doendrepeat(label, expr):
	''' handle ENDREPEAT psop '''
	blktyp = topblocktype()

	# end of a repeat expansion ?
	if blktyp == _rptExpBlk:
		_MAC.loopcontrol[-1][-1] -= 1
		if _MAC.loopcontrol[-1][-1] > 0:
			nextexpansion()
		else:
			endloopexp( label )

	# terminating a definition ?
	elif blktyp == _rptDefBlk:
		control = endloopdef( _rptSkips )
		if control is not None and control[-1] > 0:
			begloopexp( _rptExpBlk, control )

	# an orphan !
	else:
		badblock( _rptCrossBlk )

# -----------------------------
# psop: [label] WHILE cond
# -----------------------------

def dowhile(label, expr):
	''' handle WHILE psop '''
	# - note that only the outermost while is defined, but that any
	# nested whiles will be defined in turn as they are encountered
	# when the outer while is expanded (so they work properly)
	if begindefinition(_whlDefBlk):
		_ = EXP.getconstnum( expr )		# just make sure we can evaluate
		begloopdef( label, expr )
	PSOP.skipto( _whlSkips )

# -----------------------------
# psop: [label] ENDWHILE
# -----------------------------

def doendwhile(label, expr):
	''' handle ENDWHILE psop '''
	blktyp = topblocktype()

	# end of a while expansion ?
	if blktyp == _whlExpBlk:
		ok, doloop = EXP.getconstnum( _MAC.loopcontrol[-1][-1] )
		if ok and doloop:
			nextexpansion( )
		else:
			endloopexp( label )

	# terminating a definition ?
	elif blktyp == _whlDefBlk:
		control = endloopdef( _whlSkips )
		if control is not None:
			ok, doloop = EXP.getconstnum( control[-1] )
			if ok and doloop:
				begloopexp( _whlExpBlk, control )

	# an orphan !
	else:
		badblock( _whlCrossBlk )

# -----------------------------
# expand blocks
# -----------------------------

def getreadndx():
	'''return index of next line to read from source store'''
	if _MAC.expandsrc[-1] < _MAC.expandend[-1]:
		_MAC.expandsrc[ -1 ] += 1
		return _MAC.expandsrc[ -1 ]

	# ...an unclosed block definition within an expansion (fatal)
	else:
		UM.fatal( "BadNestBlk" )

def subactualargs(this):
	'''replace any formal args with actual args'''
	# because we verified any formal arguments at definition time
	# and verified actual arguments at invocation time,
	# we know if we detect a formal argument now we can substitute
	# without needing any more error checks

	# is there an active macro expansion and something that might need to be substituted for ?
	if len(_MAC.actualargs) and SYM.macReplacePrefix in this:
		return re.sub( SYM.macLabel, lambda m: _MAC.actualargs[-1][m.group().upper()], this, flags=re.IGNORECASE )
	else:
		return this

# -----------------------------
# Listing support
# -----------------------------

def getmacros():
	'''macro names, expansion counts and definition line'''
	macros = []
	for name in _MAC.expcnt:
		macros.append( (name, _MAC.expcnt[name]) )
	macros.sort( key = lambda f: f[0] )
	return macros