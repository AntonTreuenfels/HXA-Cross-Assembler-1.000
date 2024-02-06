# Hobby Cross-Assembler (HXA) V1.002 - Expression Parsing and Evaluation

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

# first created: 04/09/03	(in Thompson AWK 4.0)
# last revision: 02/05/24

# preferred public function prefix: EXP

# HXA has arithmetic, logical, string and regular expression operators
# - arithmetic is integer-only 
# - Python 3 itself has no built-in limit on integer values,
# nor does HXA's evaluator
# - however the largest arithmetic results HXA can store are 32 bit values
# - this restriction is enforced by 'hxa_codgen' only when storage is
# actually attempted

# -----------------------------
import re
# other HXA modules
import hxa_macro as MAC
import hxa_codegen as CG
import hxa_symbol as SYM
import hxa_progctr as PC
import hxa_file as OS
import hxa_source as SRC
import hxa_strings as STR
import hxa_misc as UTIL
import hxa_usermesg as UM
# -----------------------------

# private constants

# character, string and regular expression literal operand patterns
# - basic pattern is:
# delimiter
# (1) any single char except delimiter or backslash, or 
# (2) backslash plus next char as a pair
# delimiter

chrLiteral   = r"'([^\'\\]|\\.)+'"			# character literal (cannot be null)
strLiteral   = r'"([^\"\\]|\\.)*"'			# string literal (can be null string)
regexLiteral = r'/([^\/\\]|\\.)+/i?'		# regex literal (cannot be null)

# -----------------------------

# module variables

class EXPvariables(object):

	def __init__(self):

		# we put these here so both 'doeval()'and '_eval()' can see them
		# - we'd really rather nest '_eval()' within 'doeval()'
		# (so as to hide them from everything outside 'doeval()')
		# - but we need to separate them so the user function 'val()' works

		self.skipLevel = 0			# current skip level
		self.downToken = None		# token that decrease skip level
		self.upToken = None			# token that increases skip level
		self.evalstk = []			# evaluation stack

_EXP = EXPvariables()

# -----------------------------
# Built-in Functions
# -----------------------------

# helpers for built-ins
# - in Thompson AWK strings are one-based rather than zero-based
# - we try to keep behavior consistent with earlier versions

def startpos(strlst, pos):
	'''find start position within string'''
	# null strings not allowed
	if all(len(str) for str in strlst):
		slen = len( strlst[0] )
		# adjust for negative values
		if pos < 0:
			pos += slen + 1
		# is the start position within the string ?
		return ( pos > 0 and pos <= slen, pos-1 )
	else:
		return ( False, None )

# -----------------------------

def fncAbs(val):
	''' absolute value '''
	return ( True, abs(val) )

def fncCfn():
	'''current file name'''
	return ( True, OS.currfn() )

def fncDir():
	'''current directory (path)'''
	return ( True, OS.currdir() )

def fncChr(val):
	''' integer to character '''
	return ( True, STR.unichr(val) )

def fncCpu():
	''' processor name '''
	return ( True, CG.cpu() )

def fncEOS():
	'''is user stack empty?'''
	return ( True, UTIL.eos() )

def fncFwd(str):
	'''check expression for forward reference'''
	ok, rpn = doparse( str, 'number' )
	if not ok:
		return ( False, None )
	# recurse ! forward reference is whole point !
	ok, _ = _eval( rpn )
	return ( True, 0 if ok else 1 )

def fncLbl(label):
	''' label exists ? '''
	ok, sym = SYM.getglobal( label )
	return ( ok, 1 if ok and SYM.exists(sym) else 0 )

def fncLen(str):
	''' string length '''
	return ( True, len(str) )

def fncLwr(str):
	'''lowercase'''
	return ( True, str.lower() )

def fncMac(label):
	''' macro exists ? '''
	ok, sym = SYM.getglobal( label )
	return ( ok, 1 if ok and MAC.ismacro(sym) else 0 )

def fncMat(str, regex, pos=1):
	'''substring by pattern match'''
	rstr = ''
	canmatch, start = startpos( [str], pos )
	if canmatch:
		m = regex.search( str, start )
		if m is not None:
			rstr = m.group()
	return ( True, rstr )

def fncMid(str, start, count=None):
	''' substring by indices'''
	rstr = ''
	canslice, first = startpos( [str], start )
	if canslice:
		if count is None:
			rstr = str[first:]
		elif count > 0:
			rstr = str[first:min(first+count, len(str))]
		# counts less than one
		else:
			rstr = ''
	return ( True, rstr )

def fncMsg(key):
	'''internal message text'''
	return ( True, UM.expandtext(key) )

def fncNxL(haystk, needle, pos=1):
	''' lowest index of needle in haystack '''
	canlook, pos = startpos( [haystk, needle], pos )
	return ( True, haystk.find(needle, pos) + 1 if canlook else 0 )

def fncNxR(haystk, needle, pos=None):
	''' highest index of needle in haystack '''
	canlook, pos = startpos( [haystk, needle], len(haystk) if pos is None else pos )
	return ( True, haystk.rfind(needle, 0, pos+1) + 1 if canlook else 0 )

def fncOrd(str, pos=1):
	'''numeric value of character'''
	canlook, pos = startpos( [str], pos )
	return ( True, ord(str[pos:pos+1]) if canlook else 0 )

def fncPeek(ndx=1):
	'''user stack item at "ndx"'''
	return ( True, UTIL.dopeek(ndx) )

def fncPop():
	'''top item on user stack'''
	return ( True, UTIL.dopop() )

def fncRfn():
	''' root file name '''
	return  ( True, OS.rootfn() )

def fncSegbeg(name):
	'''absolute start address of segment'''
	return PC.getsegbeg( name ) 

def fncSegend(name):
	'''absolute end address of a segment'''
	return PC.getsegend( name ) 

def fncSeglen(name):
	'''byte length of segment'''
	return PC.getseglen( name )

def fncSegoff(name):
	'''byte offset of segment in binary oputput file'''
	return PC.getsegoff( name )

def fncSgn(val):
	'''sign '''
	return ( True, 1 if val > 0 else -1 if val < 0 else 0 )

def fncStr(val):
	'''decimal string representation'''
	return ( True, str(val) )

def fncTim():
	'''current time as ASCII string'''
	# - ex: "Wed Feb  1 19:27:03 2023"
	return ( True, OS.getasctime() )

def fncUpr(str):
	'''uppercase'''
	return ( True, str.upper() )

def fncVal(str):
	'''evaluate string as expression'''
	ok, rpn = doparse( str, 'number' )
	if not ok:
		return( False, None )
	# recurse ! forward reference OK !
	return _eval( rpn )

def fncVrN():
	''' version number '''
	return( True, SYM.lookup('__VER__') )

def fncVrS():
	''' version string '''
	return ( True, SYM.lookup('__VER__$') )

def fncXlt(chr):
	'''character translation'''
	return( True, STR.xlate(chr) )

# function dispatch (and description) dictionary

_fncDispatch = {
	'ABS':		(fncAbs, 1, 1, 'n2n'),
	'CHR$':		(fncChr, 1, 1, 'n2s'),
	'CPU$':		(fncCpu, 0, 0, '2s'),
	'DEFINED':	(fncMac, 1, 1, 'g2n'),
	'DIR$':	 	(fncDir, 0, 0, '2s'),
	'EMPTY':	(fncEOS, 0, 0, '2n' ),
	'FILE$':	(fncCfn, 0, 0, '2s' ),
	'FORWARD':	(fncFwd, 1, 1, 's2n' ),
	'INDEX':	(fncNxL, 2, 3, 'ssn2n'),
	'INDEXR':	(fncNxR, 2, 3, 'ssn2n'),
	'ISLABEL':	(fncLbl, 1, 1, 'g2n' ),
	'ISMACRO':	(fncMac, 1, 1, 'g2n' ),
	'LABEL':	(fncLbl, 1, 1, 'g2n' ),
	'LEN':		(fncLen, 1, 1, 's2n' ),
	'MATCH$':	(fncMat, 2, 3, 'srn2s' ),
	'MESG$':	(fncMsg, 1, 1, 's2s' ),
	'MID$':		(fncMid, 2, 3, 'snn2s' ),
	'ORD':		(fncOrd, 1, 2, 'sn2n' ),
	'PEEK$':	(fncPeek, 0, 1, 'n2s' ),
	'POP$':		(fncPop, 0, 0, '2s' ),
	'ROOTFILE$':	(fncRfn, 0, 0, '2s' ),
	'SEGBEG':	(fncSegbeg, 1, 1, 'g2n' ),
	'SEGEND':	(fncSegend, 1, 1, 'g2n' ),
	'SEGLEN':	(fncSeglen, 1, 1, 'g2n' ),
	'SEGOFF':	(fncSegoff, 1, 1, 'g2n' ),
	'SGN':		(fncSgn, 1, 1, 'n2n'),
	'STR$':		(fncStr, 1, 1, 'n2s'),
	'TIME$':	(fncTim, 0, 0, '2s' ),
	'TOLOWER$':	(fncLwr, 1, 1, 's2s' ),
	'TOUPPER$':	(fncUpr, 1, 1, 's2s'),
	'VAL':		(fncVal, 1, 1, 's2n'),
	'VER':		(fncVrN, 0, 0, '2n' ),
	'VER$':		(fncVrS, 0, 0, '2s' ),
	'XLATE':	(fncXlt, 1, 1, 'n2n' ),
}

def _normalize(this):
	''' normalize expression tokend '''
	#  - separated so it can be easily changed if ever needed
	return this.upper()

def isfunc(this):
	return _normalize(this) in _fncDispatch

# -----------------------------
# Parser
# -----------------------------

# operands accepted:
# - binary, decimal and hexadecimal integer literals
# - numeric, string and anonymous labels
# - string, character and regex literals
# - program counter

# operators accepted:
# unary numeric:
# - negation, plus
# - bitwise NOT
# - byte/word extraction
# binary numeric: 
# - addition, subtraction, multiplication, division, modulus
# - left shift, right shift
# - bitwise AND, OR, XOR
# logical unary (numeric result):
# - logical not, equality, inequality
# - greater than, less than, greater or equal, less or equal
# function call parentheses
# grouping parentheses

# errors detected:
# - unrecognized input
# - out of range numeric literals
# - malformed expression
# - type mismatches
# - function names
# - function argument counts

# result tuple:
# - (True, [rpn])
# - (False, None)

# -----------------------------

def doparse(this, want):
	'''convert algebraic expression to Reverse Polish Notation'''

# -----------------------------

	def parsestate(key, detail):
		UM.debug(
			("Input expr", this),
			("Current expr", expr),
			("Current token", token),
			("Current RPN", rpn),
			("Parse stack", parsestk),
			("Type stack", typestk),
			("Need Operand", wantoperand),
			("Error key", key),
			("Detail", detail),
		)

# -----------------------------

	def _parserr(key, detail=None):
		''' report parse errors '''

#		parsestate( key, detail )

		UM.error( key, detail if detail is not None else this )
		return False

# -----------------------------

	def _topop():
		''' remove and return top operator on parse stack '''
		return parsestk.pop()[0]

	def _typecheck(operator):
		''' type check operand(s) of operator '''

		def _rpnerr(key, pos=None):
			return _parserr( key, rpn[pos-1] if pos is not None else None )

		def _numerr(pos=None):
			'''not numeric'''
			return _rpnerr( 'NeedNum', pos )

		def _strerr(pos=None):
			'''not string'''
			return _rpnerr( 'NeedStr', pos )

		def _glberr(pos=None):
			'''not global name'''
			return _rpnerr( 'NeedGlobal', pos )

		def _ter1err():
			''' ? without : '''
			return _parserr( 'BadTrnry1' )

		def _ter2chk():
			''' : without ? '''
			return _parserr( 'BadTrnry2' ) if _topop() != 'C?-' else True

		def _rpush(type):
			''' push operator result type on stack '''
			# technically an intermediate result has no RPN position
			typestk.append( (type, None) )
			return True

		def _rnumber():
			''' push numeric result '''
			return _rpush( 'number' )

		def _rstring():
			''' push string result '''
			return _rpush( 'string' )

		def _rregex():
			''' push regex result '''
			return _rpush( 'rgxlit' )

		def _rglobal():
			'''push global result'''
			return _rpush( 'global' )

		def _argsep():
			''' type check function argument separator '''
			if len(parsestk) < 2 or parsestk[-2][0] != 'B(':	# within a function call ?
				return _parserr( 'BadArgSep' )
			else:
				rpn.pop()										# remove 'F,' from RPN
				return True

		def _fncsig():
			''' type check function signature '''
			nonlocal checkers

			argcnt = argstk[ -1 ]
			type, rpnpos = typestk.pop( -(argcnt+1) )
			if not 'sym' in type:
				return _rpnerr( 'NeedFunction', rpnpos )
			fnc = rpn[ rpnpos-1 ]
			if not fnc in _fncDispatch:
				return _parserr( 'BadFunction', fnc )
			_, min, max, chk = _fncDispatch[ fnc ]
			if not UTIL.inrange(argcnt, min, max):
				return _parserr( 'BadArgCnt', fnc )
			newchecks = list( _checklist[chk] )					# type check argument(s)
			if argcnt < max:
				newchecks = newchecks[:argcnt+1]				# remove unneeded checks
			checkers.extend( newchecks )
			return True

		def _argcnt():
			'''add function argument count to RPN'''
			rpn.insert( -1, argstk.pop() )
			return True

		def _zargcnt():
			'''remove zero value from argument count stack'''
			_ = argstk.pop()
			return True
 
		def _number():
			''' type check numeric operand '''
			type, rpnpos = typestk.pop()
			if type != 'number':

				if type == 'numsym':							# convert labels to values
					rpn.insert( rpnpos, 'SY*' )

				elif 'num' not in type:
					return _numerr( rpnpos )

			return True

		def _string():
			''' type check string operand '''
			type, rpnpos = typestk.pop()
			if type != 'string':

				if type == 'strsym':							# convert labels to values
					rpn.insert( rpnpos, 'SY*' )

				elif not 'str' in type:
					return _strerr( rpnpos )

			return True

		def _regex():
			''' type check regex operand '''
			type, rpnpos = typestk.pop()
			if type == 'rgxlit':
				return True
			else:
				return _rpnerr( 'NeedRegex', rpnpos )

		def _global():
			'''type check global symbol operand '''
			type, rpnpos = typestk.pop()
			if type == 'strsym':
				rpn.insert( -1, 'SY*' )		# de-reference symbol
			elif type not in ['number', 'numsym', 'string', 'strlit']:
				return _glberr( rpnpos )

			rpn.insert( -1, 'SYG' )
			return True

		def _cmpnul():
			''' insert "compare to null string" operator '''
			rpn.insert( -1, '$U!=' )
			return True

		def _addrgx():
			rpn.insert( -1, '/U*' )
			return True

		def _select():
			''' disambiguate polymorphic operator '''
			nonlocal checkers

			# not always necessary due to Python's loose typing
			# - but we like to anyway
			# numeric check at index 0 in 'checkers'
			# string check at index 1
			# - we've popped off everything before these, so indices are constant

			ndx = 1 if 'str' in typestk[-1][0] else 0
			checkers = list ( _checklist[checkers.pop(ndx)] )
			return True

		def _final():
			''' check if final type is the desired type '''
			have, rpnpos = typestk.pop()	# left by final parse stack clearance
			want, _ = typestk.pop()			# pushed on at start of evaluation

			if want != have:

				# do we have a numeric expression ?
				# - number, numlit, numsym

				if 'num' in have:

					if want == 'typstr':
						return _parserr( "NeedStr", this )

					if want in ['number', 'typnum']:
						if have == 'numsym':
							rpn.append( 'SY*' )

					elif want == 'string':
						if have == 'numsym':
							rpn.append( 'SY*' )
						rpn.append( '$CH*' )

					elif want == 'global':
						if have == 'numsym':
							rpn.append( 'SYG' )
						else:
							return _glberr( rpnpos )

					# we don't need to do anything here about: have == 'numlit'

				# do we have a string expression ?
				# - string, strlit, strsym

				elif 'str' in have:

					if want == 'typnum':
						return _parserr( "NeedNum", this )

					if want in ['string', 'typstr']:
						if have == 'strsym':
							rpn.append( 'SY*' )

					elif want == 'number':
						if have == 'strsym':
							rpn.append( 'SY*' )
						rpn.append( '$U!=' )

					elif want == 'global':
						if have == 'strsym':
							rpn.append( 'SY*' )
						rpn.append( 'SYG' )

					# we don't need to do anything here about: have == 'strlit'

				# more like 'NoWay' fatal error ?
				else:
					return _rpnerr( 'BadType', rpnpos )

			return True

		# operator type checks
		
		_typechecks = {
			'B(': 'f()',		# function with arguments
			'EOE': 'final',		# end of expression
			'F,': 'f,',			# function argument separator
			'PC*': '2n',		# read program counter
			'$U*': 's2s',		# convert string literal
			'/U*': 'r2r',		# convert regex literal
			'Z()*': 'z()',		# function with no arguments

			'U-': 'b2n',		# negation
			'U+': 'b2n',		# plus
			'U!': 'b2n',		# logical not
			'U~': 'b2n',		# bitwise-NOT
			'U<': 'b2n',		# extract least significant byte
			'U>': 'b2n',		# extract most significant byte
			'U^': 'b2n',		# extract most significant word

			'B*': 'bn2b',		# multiply
			'B/': 'nn2n',		# divide
			'B%': 'nn2n',		# modulus
			'B+': 'bb2b',		# add
			'B-': 'nn2n',		# subtract
			'B<<': 'nn2n',		# left shift
			'B>>': 'nn2n',		# right shift
			'B<': 'bb2n',		# less than
			'B>': 'bb2n',		# greater than
			'B<=': 'bb2n',		# less or equal
			'B>=': 'bb2n',		# greater or equal
			'B==': 'bb2n',		# equal
			'B!=': 'bb2n',		# not equal
			'B~':  'sb2n',		# pattern match
			'B!~': 'sb2n',		# pattern not match
			'B&': 'nn2n',		# bitwise-AND
			'B^': 'nn2n',		# bitwise-XOR
			'B|': 'nn2n',		# bitwise-OR

			'C&&+': 'b2_',		# left logical AND
			'C&&-': 'b2n',		# right logical AND
			'C||+': 'b2_',		# left logical OR
			'C||-': 'b2n',		# right logical OR
			'C?+':  'b2_',		# left ternary ?
			'C?-':  '?-err',	# right ternary ?
			'C:+':  'b2b',		# left ternary :
			'C:-':  '?:bb2b',	# right ternary :
		}

		# operator/function check lists
		# - some of these are never used but included for completeness

		_checklist = {
			# polymorphic disambiguation
			'?:bb2b':	[ 'nn2n', 'ss2s', _select, _ter2chk ],
			'b2_':		[ 'n2_', 's2n2_', _select ],
			'b2b':		[ 'n2n', 's2s', _select ],
			'b2n':		[ 'n2n', 's2n2n', _select ],
			'bb2n':		[ 'nn2n', 'ss2n', _select ],
			'bb2b':		[ 'nn2n', 'ss2s', _select ],
			'bn2b':		[ 'n2n', 's2s', _select, _number ],
			'sb2n':		[ 'sr2n', 'ssr2n', _select ],
			# monomorphic - order matters for mixed types !
			'2n':		[ _rnumber ],
			'2s':		[ _rstring ],
			'f()':		[ _argcnt, _fncsig ],
			'f,':		[ _argsep ],
			'final':	[ _final ],
			'g2n':		[ _rnumber, _global ],
			'n2_':		[ _number ],
			'n2n':		[ _rnumber, _number ],
			'n2s':		[ _rstring, _number ],
			'nn2n':		[ _rnumber, _number, _number ],
			'r2r':		[ _rregex, _regex ],
			's2n':		[ _rnumber, _string ],
			's2n2_':	[ _cmpnul, _string ],
			's2n2n':	[ _rnumber, _cmpnul, _string],
			's2s':		[ _rstring, _string ],
			'sn2n':		[ _rnumber, _string, _number ],
			'snn2s':	[ _rstring, _string, _number, _number ],
			'sr2n':		[ _rnumber, _string, _regex ],
			'srn2s':	[ _rstring, _string, _regex, _number ],
			'ss2n':		[ _rnumber, _string, _string ],
			'ss2s':		[ _rstring, _string, _string ],
			'ssn2n':	[ _rnumber, _string, _string, _number ],
			'ssr2n':	[ _rnumber, _string, _string, _addrgx ],
			'z()':		[ _zargcnt, _fncsig ],
			# error
			'?-err':	[ _ter1err ],
		}

		# main loop

		# we can dynamically change the contents of 'checkers' as we go along
		checkers = list( _checklist[_typechecks[operator]] )	# 'list' to avoid aliasing

		ok = True
		while ok and len(checkers) > 0:
			ok = checkers.pop()()
		return ok

	def _addoperand(operand, type):
		''' add operand to RPN and save its type and RPN position'''
		rpn.append( operand )
		typestk.append( (type, len(rpn)) )

		
	def _addoperator():
		'''add operator to RPN and type check its operand(s) '''
		operator, _ = parsestk.pop()				# here we care about the operator
		rpn.append( operator )
		ok = _typecheck( operator )
		return ok
		
	def _popgreaterorequal(prec):
		'''pop operators of equal or greater precedence'''
		ok = True
		while ok and prec <= parsestk[-1][1]:		# here we care about operator precedence
			ok = _addoperator()
		return ok

	def _pushleft(op, prec):
		'''push left associative operator on stack'''
		ok = _popgreaterorequal( prec )
		if ok:
			parsestk.append( (op, prec) )
		return ok

	def _popgreater(prec):
		'''pop operators of greater precedence'''
		ok = True
		while ok and prec < parsestk[-1][1]:		# here we care about operator precedence
			ok = _addoperator()
		return ok

	def _pushright(op, prec):
		'''push right associative operator on stack'''
		ok = _popgreater( prec )
		if ok:
			parsestk.append( (op, prec) )
		return ok

	def _popuntil(op, prec):
		'''clear and check operator stack'''
		if not _popgreaterorequal(prec):
			return False
		elif op == _topop():							# top remaining operator is the one we want to see ?
			return True
		elif op == '(':
			return _parserr( 'BadRgtPar', ')' )
		elif op == 'EOE':
			return _parserr( 'BadLftPar', '(' )
		else:
			UM.noway( 'popuntil', op )

	def _convertuint(ulit, base, significant):
		'''convert unsigned literal to internal form'''
		# isolate the significant portion of 'ulit'
		# - if no match, digits are all zeroes
		m = re.search( significant, ulit.upper() )

		uint = int( m.group(), base ) if m is not None else 0

		_addoperand( uint, 'numlit' )
		return True

	def _startswith(regex):
		'''test if expression starts with given regular expression'''
		nonlocal expr, token

		m = re.match( regex, expr, flags=re.IGNORECASE )
		if m is None:
			token = None
			return False
		else:
			token = m.group()						# what we matched
			expr = expr[len(token):]				# "chop off" what we matched
			return True

	# unary operator matching

	_unPrefxOp = '[-+!~<>^]'

	# unary precedence

	_unPrec = {
		'-': 140,		# negation
		'+': 140,		# plus
		'!': 140,		# logical not
		'~': 140,		# bitwise-NOT
		'<': 140,		# extract least significant byte
		'>': 140,		# extract most significant byte
		'^': 140,		# extract most significant word
}

	# binary operator matching

	_binInfxOp = '[-+*/%&^|(]|<[<=]?|>[>=]?|[!=]=|!?~'

	# binary precedence

	_binPrec = {
		'(':  180,		# function call opening parenthesis
		'*':  130,		# multiply
		'/':  130,		# divide
		'%':  130,		# modulus
		'+':  120,		# add
		'-':  120,		# subtract
		'<<': 110,		# left shift
		'>>': 110,		# right shift
		'<':  100,		# less than
		'>':  100,		# greater than
		'<=': 100,		# less or equal
		'>=': 100,		# greater or equal
		'==': 90,		# equal
		'!=': 90,		# not equal
		'~':  80,		# pattern match
		'!~': 80,		# pattern not match
		'&':  70,		# bitwise-AND
		'^':  60,		# bitwise-XOR
		'|':  50,		# bitwise-OR
	}

	# conditional operator matching

	_condOp = '&&|[|]{2}|[?:]'

	# conditional precedence

	_condPrec = {
		'&&': (40, 40, _pushleft),	# logical AND
		'||': (30, 30, _pushleft),	# logical OR
		'?':  (28, 24, _pushright),	# ternary conditional '?'
		':':  (26, 24, _pushright), # ternary conditional ':'
	}

	# "helper" operators
	# - we use them to make certain tasks easier
	# - they may or may not appear in original expression
	# - they may or may not appear in final RPN

	_helperPrec = {
		'PC*': 180,		# program counter value
		'$U*': 180,		# string literal
		'Z()*': 180,	# zero argument function call
		'/U*': 180,		# regex literal
		'(': 2,			# left (opening) parenthesis
	}
	
	def _pushoperator(token):
		''' unconditionally push helper operator on parse stack '''
		parsestk.append( (token, _helperPrec[token]) )

	# initialize

	expr = SYM.checkloneanon( this.strip() )		# save to new variable but retain original for error reports
	token = None									# anything successfully matched
	ok = wantoperand = True							# flags
	rpn = []										# built-up rpn expression
	parsestk = [ ('EOE', 1) ]						# operator stack
	typestk = [ (want, None) ]						# type stack
	argstk = []										# function argument count stack

	# top level main loop

	while ok and len(expr):

		expr = expr.lstrip()						# skip leading whitespace

		# looking for operand
		if wantoperand:

			# left parenthesis ?
			if _startswith('[(]'):
				_pushoperator( '(' )

			# unary prefix operator ?
			elif _startswith(_unPrefxOp):
				ok = _pushright( 'U' + token, _unPrec[token] )

			else:

				wantoperand = False					 # flip

				# label ?
				if _startswith( SYM.symExpr ):
					token = SYM.normalize( token )
					_addoperand( token, 'strsym' if SYM.isstr(token) else 'numsym' )

				# unsigned hexadecimal literal ?
				elif _startswith( '([$]|0X)[0-9A-F]+|[0-9][0-9A-F]*H' ):
					ok = _convertuint( token, 16, '[1-9A-F][0-9A-F]*' )

				# unsigned binary literal ?
				elif _startswith( '(%|0b)[01]+|[01]+b' ):
					ok = _convertuint( token, 2, '1[01]*' )

				# unsigned decimal literal ?
				elif _startswith( '[0-9]+D?' ):
					ok = _convertuint( token, 10, '[1-9][0-9]*' )

				# string literal ?
				elif _startswith( strLiteral ):
					_addoperand( token, 'strlit' )
					_pushoperator( '$U*' )

				# character literal ?
				elif _startswith( chrLiteral ):
					_addoperand( STR.chrlit(token), 'numlit' )	# convert to number immediately

				# regular expression literal ?
				elif _startswith( regexLiteral ):
					_addoperand( token, 'rgxlit' )
					_pushoperator( '/U*' )

				# program counter ?
				elif _startswith( '[*$]' ):
					_pushoperator( 'PC*' )

				# malformed !
				else:
					ok = _parserr( 'NeedOperand', expr )

		# looking for operator
		else:

			# right parenthesis ?
			if _startswith('[)]'):
				ok = _popuntil( '(', 4 )

			# zero argument function ?
			elif _startswith( '\([ ]*\)' ):
				''' zero argument function() ?'''
				_pushoperator( 'Z()*' )
				argstk.append( 0 )

			else:

				wantoperand = True							# flip

				# conditional operator ?
				if _startswith( _condOp ):
					lftp, rgtp, pushtyp = _condPrec[ token ]
					ok = pushtyp(f'C{token}+', lftp) and pushtyp(f'C{token}-', rgtp)

				# binary infix operator ?
				elif _startswith( _binInfxOp ):
					ok = _pushleft( 'B' + token, _binPrec[token] )
					if token == '(':			# possible function call ?
						_pushoperator( '(' )
						argstk.append( 1 )		# at least one argument

				# function argument separator ?
				elif _startswith( ',' ):
					ok = _pushleft( 'F,', 6 )
					argstk[ -1 ] += 1			# one more argument

				# malformed !
				else:
					ok = _parserr( 'NeedOperator', expr )

	if ok:
		if wantoperand:
			ok = _parserr( 'BadEOE', this )		# must be in 'wantoperator' state   
		else:
			ok = _popuntil( 'EOE', 3 )			# clear operator stack
			if ok:
				ok = _typecheck( 'EOE' )		# final type check

	return ( ok, rpn if ok else None )			# done

# -----------------------------
# Evaluator
# -----------------------------

def _eval(rpn):
	# - doesn't care if evaluation is complete or not

	def _pushback(lst):
		''' push back unevaluated operands and operators on operand stack '''
		# error may be unrecoverable, but ignore that for now
		# - we may find another error if we continue evaluation
		_evalstk.extend( lst )

	def _err_divzero(undo):
		_pushback( undo )
		UM.error( 'DivZero' )

	def _set_skipping(down, up, save=False):
		'''set short-circuit skip flags'''
		nonlocal _skiplevel, _downtoken, _uptoken, _savetoken
		_skiplevel = 1				# start skipping over tokens without evaluating them
		_downtoken = down			# decrease skip level if this token shows up
		_uptoken = up				# increase skip level if this token show up
		_savetoken = save			# save skipped over tokens for later evaluation ?

	# nonary operators

	def _pc_get():
		''' read program counter '''
		pc = PC.get()
		if PC.gotrel( pc ):				# relative value ?
			_pushback( [pc, 'PC**'] )	# ...make absolute in next pass
		else:
			_evalstk.append( PC.getabs(pc) )

	def _func_zero():
		''' zero argument function '''
		fnc = _evalstk.pop()
		ok, val = _fncDispatch[fnc][0]()
		if ok:
			_evalstk.append( val )
		else:
			_pushback( [fnc, 'Z()'] )

	# unary operators

	def _arith_negate(arg):
		''' unary negation '''
		_evalstk.append( -arg )

	def _arith_plus(arg):
		''' unary plus (absolute value) '''
		_evalstk.append( abs(arg) )

	def _poly_not(arg):
		'''logical NOT'''
		_evalstk.append( not arg )

	def _bit_not(arg):
		''' bitwise NOT '''
		_evalstk.append( ~arg )

	def _bit_lsb(arg):
		''' least significant byte '''
		_evalstk.append( CG.getlsb(arg) )

	def _bit_msb(arg):
		''' most significant byte '''
		_evalstk.append( CG.getmsb(arg) )

	def _bit_msw(arg):
		''' most significant word '''
		_evalstk.append( CG.getmsw(arg) )

	def _pc_abs(arg):
		''' convert relative program counter to absolute '''
		_evalstk.append( PC.getabs(arg) )

	def _pc_sabs(arg):
		'''convert relative program counter to absolute as string'''
		_evalstk.append( str(PC.getabs(arg)) )

	def _sym_val(arg):
		''' look up symbol value '''
		if not SYM.exists(arg):
			# possible forward reference; try again later
			_pushback( [arg, 'SY*'] )
		else:
			val = SYM.lookup( arg )
			if not PC.isaddr(val):
				# an integer whose value we know now
				_evalstk.append( val )
			elif not PC.gotrel(val):
				# convert addr to an integer whose value we know now
				_evalstk.append( PC.getabs(val) )
			else:
				# save addr and convert on second pass
				_pushback( [val, '$PC**' if SYM.isstr(arg) else 'PC**'] )

	def _sym_isglobal(arg):
		''' verify symbol is global '''
		if SYM.isglobalnumeric(arg):
			_evalstk.append( SYM.normalize(arg) )
		else:
			_pushback( [arg, 'SYG'] )

	def _func_call(cnt):
		''' execute non-zero argument function call '''
		nonlocal _evalstk
		args = _evalstk[-cnt:]						# args in left-to-right order
		if any( _isoperator(arg) for arg in args ):
			_pushback( [cnt, 'B('] )				# rebuild expression on stack
			return
		_evalstk = _evalstk[:-cnt]					# remove args from the evaluation stack
		fnc = _evalstk.pop()						# function name
		ok, val = _fncDispatch[ fnc ][0](*args)		# call function with unpacked args
		if ok:
			_evalstk.append( val )					# push result
		elif val is None:
			# rebuild original function call for possible later re-evaluation
			# - note variable labels in such calls may yield unexpected results
			_pushback( [fnc] + args + [cnt, 'B('] )
		else:
			# an iterable
			_pushback( val )

	def _str_lit(val):
		'''convert string literal value'''
		_evalstk.append( STR.strlit(val) )

	def _rgx_lit(val):
		''' convert regex literal value'''
		ok, crgx = STR.rgxlit( val )
		if ok:
			_evalstk.append( crgx )
		else:
			_pushback( [val, '/U*'] )

	def _num2chr(val):
		''' convert number to Unicode char '''
		_evalstk.append( STR.unichr(val) )

	def _cmp_nul(val):
		'''compare to null string'''
		_evalstk.append( 1 if val != '' else 0 )

	def _log_lft_and(val):
		'''left branch of logical AND'''
		if val == 0:
			_evalstk.append( 0 )
			_set_skipping( 'C&&-', 'C&&+', False )

	def _log_lft_or(val):
		'''left branch of logical OR'''
		if val != 0:
			_evalstk.append( 1 )
			_set_skipping( 'C||-', 'C||+', False )

	def _log_right(val):
		'''right branch of logical AND and OR'''
		_evalstk.append( 1 if val != 0 else 0 )

	def _ter_cond(val):
		'''ternary condition'''
		if not val:
			_set_skipping( 'C:+', 'C?+', False)

	# technically these next two are nonary
	# - however we make them unary so that their dispatch
	# checks for incomplete evaluation of _ter_cond

	def _ter_true(val):
		'''end of ternary true branch'''
		_evalstk.append( val )
		_set_skipping( 'C:-', 'C:+', False )

	def _ter_false(val):
		'''end of ternary false branch'''
		_evalstk.append( val )

	# binary operators

	def _poly_multiply(rgt, lft):
		'''binary multiplication'''
		_evalstk.append( lft * rgt )

	def _arith_divide(rgt, lft):
		'''binary division'''
		if rgt != 0:
			_evalstk.append( lft // rgt )	# floored division so result is an integer
		else:								# rounded down to nearest integer
			_err_divzero( [lft, rgt, 'B/'] )

	def _arith_modulus(rgt, lft):
		'''binary modulus'''
		if rgt != 0:
			_evalstk.append( lft % rgt )	# result has sign of 'rgt'
		else:
			_err_divzero( [lft, rgt, 'B%'] )

	def _poly_add(rgt, lft):
		'''polymorhphic addition'''
		_evalstk.append( lft + rgt )

	def _arith_subtract(rgt, lft):
		'''binary subtraction'''
		_evalstk.append( lft - rgt )

	def _bit_leftshift(rgt, lft):
		''' bitwise left shift '''
		if UTIL.inrange(rgt, 0, CG.maxbits()):
			_evalstk.append( lft << rgt )
		else:
			_pushback( [lft, rgt, 'B>>'] )

	def _bit_rightshift(rgt, lft):
		''' bitwise right shift '''
		if UTIL.inrange(rgt, 0, CG.maxbits()):
			_evalstk.append( lft >> rgt )
		else:
			_pushback( [lft, rgt, 'B<<'] )

	def _poly_less(rgt, lft):
		'''polymorhphic logical less than '''
		_evalstk.append( 1 if lft < rgt else 0 )

	def _poly_more(rgt, lft):
		''' polymorphic logical greater than '''
		_evalstk.append( 1 if lft > rgt else 0 )

	def _poly_lessorequ(rgt, lft):
		''' polymorphic logical less than or equal '''
		_evalstk.append( 1 if lft <= rgt else 0 )

	def _poly_moreorequ(rgt, lft):
		''' polymorphic logical greater than or equal '''
		_evalstk.append( 1 if lft >= rgt else 0 )

	def _poly_equal(rgt, lft):
		'''polymorphic logical equality'''
		_evalstk.append( 1 if lft == rgt else 0 )

	def _poly_notequal(rgt, lft):
		'''polymorphic logical inequality'''
		_evalstk.append( 1 if lft != rgt else 0 )

	def _rgx_match(rgt, lft):
		'''regex match'''
		_evalstk.append( 0 if rgt.search(lft) is None else 1 )

	def _rgx_no_match(rgt, lft):
		_evalstk.append( 1 if rgt.search(lft) is None else 0 )

	def _bit_and(rgt, lft):
		''' bitwise AND '''
		_evalstk.append( lft & rgt )

	def _bit_xor(rgt, lft):
		''' bitwise XOR '''
		_evalstk.append( lft ^ rgt )

	def _bit_or(rgt, lft):
		''' bitwise OR '''
		_evalstk.append( lft | rgt )

	# initialize dispatch function calls

	_nonarydispatch = {
		'PC*': _pc_get,			# push current segment program counter value
		'Z()*': _func_zero,		# push result of a zero-argument function
	}

	_unarydispatch = {
		'U-': _arith_negate,	# negate top stack item; an integer
		'U+': _arith_plus,		# absolute value of top stack item; an integer
		'U!': _poly_not,		# logical negation of top stack item; type indifferent
		'U~': _bit_not,			# bitwise NOT of top stack item; an integer
		'U<': _bit_lsb,			# least significant byte of top stack item; an integer
		'U>': _bit_msb,			# most significant byte of top stack item; an integer
		'U^': _bit_msw,			# most signficant word of top stack item; an integer
		'PC**': _pc_abs,		# absolute program counter value of top stack item; a tuple; second pass only
		'$PC**':_pc_sabs,		# string absolute program counter value of top stack item; a tuple; second pass only
		'SY*': _sym_val,		# value of top stack item; a symbol
		'SYG': _sym_isglobal,	# check that top stack item is global; a symbol
		'B(': _func_call,		# push result of function with one or more arguments; mixed types allowed
		'$U*': _str_lit,		# convert string literal to internal form; a string
		'$CH*': _num2chr,		# convert a number to a Unicode character
		'$U!=': _cmp_nul,		# compare top stack item to the null string; a string
		'/U*': _rgx_lit,		# convert a regex literal to internal form; a compiled regex
		'C&&+': _log_lft_and,	# check left-hand side result of logical AND; an integer
		'C&&-': _log_right,		# check right-hand side result of logical AND; an integer
		'C||+': _log_lft_or,	# check left-hand side result of logical OR; an integer
		'C||-': _log_right,		# check right-hand side result of logical OR; an integer
		'C?+': _ter_cond,		# check ternary condition result; an integer
		'C:+': _ter_true,		# start of ternary TRUE branch; a marker
		'C:-': _ter_false,		# start of ternary FALSE branch; a marker
	}

	_binarydispatch = {
		'B*': _poly_multiply,	# integer multiplications and string duplication
		'B/': _arith_divide,	# integer division
		'B%': _arith_modulus,	# integer modulus
		'B+': _poly_add,		# integer addition and string concatenation
		'B-': _arith_subtract,	# integer subtraction
		'B<<': _bit_leftshift,	# integer left shift
		'B>>': _bit_rightshift,	# integer right shift
		'B<': _poly_less,		# integer and string less than
		'B>': _poly_more,		# integer and string more than
		'B<=': _poly_lessorequ,	# integer and string less than or equal to
		'B>=': _poly_moreorequ,	# integer and string more than or equal to
		'B==': _poly_equal,		# integer and string equal
		'B!=': _poly_notequal,	# integer and string NOT equal
		'B~':  _rgx_match,		# string matches regular expression
		'B!~': _rgx_no_match,	# string NOT matches regular expression
		'B&': _bit_and,			# integer bitwise AND
		'B^': _bit_xor,			# integer bitwise XOR
		'B|': _bit_or,			# integer bitwise OR
	}

	def _isoperator(this):
		return isinstance(this, str) and (this in _binarydispatch or this in _unarydispatch or this in _nonarydispatch)

	_evalstk = []
	_skiplevel = 0
	_downtoken = _uptoken = None
	_savetoken = False

	# main loop of '_eval()'
	for token in rpn:
		if _skiplevel > 0:
			if token == _downtoken:
				_skiplevel -= 1
			elif token == _uptoken:
				_skiplevel += 1
			if _savetoken:
				_evalstk.append( token )

		elif token in _binarydispatch:
			rgt = _evalstk.pop()
			lft = _evalstk.pop()
			if _isoperator(rgt) or _isoperator(lft):
				_pushback( [lft, rgt, token] )
			else:
				_binarydispatch[token]( rgt, lft )

		elif token in _unarydispatch:
			arg = _evalstk.pop()
			if _isoperator(arg):
				_pushback( [arg, token] )				# can't evaluate operator
				if token == "C&&+":						# left side of logical AND ?
					_set_skipping( 'C&&-', 'C&&+', True )
				elif token == "C||+":					# left side of logical OR ?
					_set_skipping( 'C||-', 'C||+', True )
				elif token == "C?+":					# ternary conditional ?
					_set_skipping( 'C:-', 'C?+', True )
				elif token == "C:+":					# ternary True branch ?
					_set_skipping( 'C:-', 'C:+', True )
			else:
				_unarydispatch[token]( arg )

		elif token in _nonarydispatch:
			_nonarydispatch[token]()

		else:
			_evalstk.append( token )
			
	# completely evaluated ?
	if len(_evalstk) == 1:
		return ( True, _evalstk.pop() )		# a scalar
	else:
		return( False, _evalstk )			# a list

# operators handled:
# - unary negation, plus
# - binary addition, subtraction, multiplication, division, modulus
# - logical negation, equality, inequality, less than, less or equal, greater than, greater or equal
# - bitwise NOT, AND, OR, XOR, left shift, right shift
# - regex pattern match, not match
# - short-circuit logical AND, OR, ternary conditional
# - function calls

# errors detected:
# - division by zero
# - unresolved program counter value
# - undefined label
# - label not global

# returns:

# - a one-element list of a single number or string (if successful)
# - a multi-element list of resolved and unresolved parts of the original RPN expression (if not)

def doeval(rpn, forwardok):
	'''evaluate Reverse Polish expression'''
	# cares if evaluation is complete or not

	# The main problem here is what to do with forward references.
	# Consider adding the values of a global and a variable label together:

	# global + ]variable

	# Suppose "global" is not yet known when this expression is evaluated
	# during the first pass. One option is to save the whole expression and
	# evaluate it again during the second pass. However this leads to a
	# problem with "]variable": on the second pass the evaluation will use
	# the last value assigned to "]variable", even if it had a different,
	# well-defined value at the time the expression was first encountered

	# What we'll do instead is evaluate as much as we can during the first
	# pass, and save only what we can't evaluate.

	# RPN expressions with no forward references are easy to evaluate:
	# - if an operand appears, push it on a stack
	# - if an operator appears, pull any operands needed off the stack,
	# perform the operation, and push the result back onto the stack
	# - after the expression has been processed, there is only one value
	# on the stack: the result

	# We're going to add a wrinkle: if the operator can't be executed,
	# push its operands (if any), then the operator, onto the operand stack.
	# If later we pull an operator from the stack instead of an operand,
	# we know a previous operator failed and the current operator must as well
	# (because it needs the operand the operator just pulled should have
	# created). So we'll have to push the current operator, along with its
	# operands, back onto the operand stack as well.

	# We can do this as often as necessary for any expression. Each time we
	# do, we are using an operator we couldn't execute to protect its
	# operands from being disturbed (since they are now below their operator,
	# and won't be pulled once that operator is discovered). The net result
	# will be that any operator which can be executed will be, and any which
	# can't will be saved for later

	# Using the previous expression as an example, and assuming
	# "global" is not known but "]variable" is, the process looks like this:

	# RPN expression:										 op stack:

	# 1) global _lookup* ]variable _lookup* _add*			 (empty)
	# - read "global"; is operand; push
	# 2) _lookup* ]variable _lookup* _add*					 global
	# - read "_lookup*"; is operator; pull "global"
	# - fails; push back "global" and "_lookup*"
	# 3) ]variable _lookup* _add*							  global _lookup*
	# - read "]variable"; is operand; push
	# 4) _lookup* _add*										global _lookup* ]variable
	# - read "_lookup*"; is operator; pull "]variable"
	# - success; push back "(value)" (of "]variable")
	# 5) _add*												 global _lookup* (value)
	# - read "_add*"; is operator; pull "(value)" and "_lookup*"
	# - fails; push back "(value)" and "_lookup*"
	# 6)													   global _lookup* (value) _add*

	# So all we've managed is to find the value of "]variable" - but this
	# is enough to make sure that the expression will evaluate correctly
	# during the second pass, when "global" is known as well

	# Note that the stack contents is exactly the RPN expression we need to evaluate
	# during the second pass

	# Also note we can even arrange to safely ignore certain sub-expressions
	# by skipping over them (even if forward reference is involved the skipped
	# sub-expressions won't make it into the second pass RPN expression because
	# they're not needed for correct resolution)

	# -------------------------------------------------------

	complete, result = _eval( rpn )

	# completely evaluated or can re-evaluate later ?
	if complete or forwardok:
		return ( True, result )

	# if we can't try again, report any unresolved reference problem
	# - because either (1) one or more unresolved forward reference(s) happened
	# or (2) an evaluation error happened
	# - if an error happened, we don't need to do anything
	# special since processing will stop at the end of the
	# current pass anyway
	# - so we just assume the reason is unresolved forward
	# reference and act on that assumption
	else:

		lasttoken = None

		# check every token in result
		for i, token in enumerate(result):
			match token:

				# failed to resolve program counter value ?
				case 'PC**':
					UM.error( "BadPC" )

				# failed to verify symbol is global numeric ?
				case 'SYG':
					UM.notglobal( result[i-2] if lasttoken == "SY*" else lasttoken )

				# a symbol we need to ask about ?
				case 'SY*':
					# uncalled function ?
					if isfunc(lasttoken):
						UM.error( "NeedCall", lasttoken )
					# other reserved symbol name ?
					elif SYM.isreserved( lasttoken ):
						UM.reserved( lasttoken )
					# not p - rest of comment was what ? got lost in editing !
					else:
						UM.undefined( lasttoken )

				# was the last token one of these functions ?
				case _:
					if lasttoken in ['SEGBEG', 'SEGEND', 'SEGLEN', 'SEGOFF']:
						UM.undefined( token )

			# possibly something we can use later
			lasttoken = str( token )

	return ( False, None )

# -----------------------------

def _parseandeval(this, want, forwardok=True):
	'''parse and evaluate expression'''
	ok, rpn = doparse( this, want )
	if ok:
		ok, val = doeval( rpn, forwardok )
	return ( ok, val if ok else None )

# -----------------------------

def getnum(this):
	''' get numeric value '''
	return _parseandeval( this, 'number', True )

def getconstnum(this):
	''' get constant numeric value '''
	# a string expression will be compared to null string
	return _parseandeval( this, 'number', False )

def getonlynum(this):
	'''get constant numeric value'''
	# a string expression is an error
	ok, val = _parseandeval( this, 'typnum', False )
	return ( ok, val if ok and isinstance(val, int) else None )

def getstr(this):
	''' get string value '''
	return _parseandeval( this, 'string', True )
	
def getconststr(this):
	''' get constant string value '''
	ok, val = _parseandeval( this, 'string', False )
	if ok and len(val) < 1:
		UM.oddval( this )
	return ( ok, val )

def getonlystr(this):
	'''get constant string; no conversion to number'''
	ok, val = _parseandeval( this, 'typstr', False )
	if ok:
		ok = isinstance( val, str )
	return ( ok, val if ok else None )

def getconstglb(this):
	''' collect constant global symbol '''
	ok, val = _parseandeval( this, 'global', False )
	return ( ok, val if ok else None )

def getaddr(this):
	'''get an address value'''
	return _parseandeval( this, 'typnum', True )

# -----------------------------

def resolved(this):
	'''resolved expression ?'''
	return not isinstance(this, list)

def resolve(this):
	''' resolve any forward references in expression '''
	# expression was not resolved on first pass ?
	if isinstance(this, list):
		# we know evaluation is incomplete (and not just failed)
		# - because otherwise second pass would not happen at all
		# - win or lose, this is last attempt
		ok, this = doeval( this, False )

	# expression resolved (or is None)
	return this

# -----------------------------

def _addequ(label, val):
	'''add resolved EQU value to symbol table'''
	SYM.add( label, val )
	# record for listing?
	if SYM.isglobal(label) or SRC.listequ():
		# value will show up in listing but not in object file
		CG.store( 'strequ' if SYM.isstr(label) else 'numequ', val )	

def _getequ(label, expr):
	'''collect constant value for EQU'''
	if SYM.isstr(label):
		return getonlystr( expr )
	else:
		return getonlynum( expr )

# -----------------------------
# psop: label EQU expr
# -----------------------------

def doequ(label, expr):
	''' handle EQU psop '''
	ok, val = _getequ( label, expr )
	if ok:
		_addequ( label, val )

# -----------------------------
# psop: label PLUSEQU expr
# -----------------------------

def doplusequ(label, expr):
	''' handle PLUSEQU psop '''
	# works on both numeric and string
	ok, label = SYM.verplusminus( label, expr, False )
	if ok:
		ok, val = _getequ( label, expr )
		if ok:
			_addequ( label, SYM.lookup(label) + val )

# -----------------------------
# psop: label MINUSEQU expr
# -----------------------------

def dominusequ(label, expr):
	''' handle MINUSEQU psop '''
	# works only on numeric
	ok, label = SYM.verplusminus( label, expr, True )
	if ok:
		ok, val = getonlynum( expr  )
		if ok:
			_addequ( label, SYM.lookup(label) - val )

# -----------------------------
# Utility
# -----------------------------

def getoptstr(this):
	''' return non-blank evaluated string expression or unevaluated raw string '''
	if isinstance(this, str):
		# starts with a string literal/label/function ?
		if re.match(strLiteral, this) or re.match(SYM.strLabel, this, flags=re.IGNORECASE):
			ok, val = getonlystr( this )
			# can't evaluate
			if not ok:
				return ( False, None )

		# take "as-is"
		else:
			val = this

		# make sure not all whitespace
		val = val.rstrip()
		if len(val) > 0:
			return( True, val )

	# not a string or null string
	UM.oddval( this )
	return ( False, None )

# -----------------------------
# get constant values
# -----------------------------

def getfname(this):
	'''get filename'''
	# backwards compatability w/prior versions of HXA
	# ...candidate for future removal ?
	if this.startswith('<') and this.endswith('>'):
		this = this[1:-1]

	ok, val = getoptstr( this )
	if ok:
		return ( True, val )

	# bad expression or all whitespace
	UM.error( "NeedFile", this )
	return ( False, None )

def getequate(this):
	''' collect left=right expression '''
	ok, val = getoptstr( this )
	return STR.splitequate( val )

def gethexstr(this):
	''' collect (possibly decorated) string of hex chars '''
	ok, str = getoptstr( this )
	if ok:
		# a hexadecimal "opt-str" ?
		# (1) optional radix indicator followed by an even number of hex char pairs, or
		# (2) an even number of hex char pairs followed by radix indicator
		# - we're cheating a bit here - radix indicators can actually be at both ends at once
		m = re.fullmatch( '(([$]|0?X)[ ]*)?([0-9A-F][0-9A-F][ ]*)+H?', str, flags=re.IGNORECASE )
		# 'str' has an even number of hex chars ?
		if m is not None:
			m = re.search( '([0-9A-F][0-9A-F][ ]*)+', str, flags=re.IGNORECASE )
			return ( True, bytearray.fromhex(m.group()) )

	# null, non-hex chars or odd count
	UM.error( "NeedHex", this )
	return ( False, None )

def getinrange(this, min, max):
	''' get and range check numeric value '''
	ok, val = getonlynum( this )
	if ok:
		ok = UTIL.inrange( val, min, max )
	return (ok, val if ok else None)

def getposnum(this):
	''' get positive numeric value  '''
	ok, val = getonlynum( this )

	# only a warning (else we'd use 'inrange()'
	if ok and val < 0:
		UM.warn( 'NeedPos', UTIL.iformat(val) )

	return ( ok, val )

