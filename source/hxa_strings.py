# Hobby Cross-Assembler (HXA) V1.00 - String Helper Functions

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

# first created: 11/01/21
# last revision: 12/28/23

# preferred public function prefix: "STR"

# -----------------------------
import re
# other HXA modules
import hxa_usermesg as UM
import hxa_codegen as CG
import hxa_misc as UTIL
# -----------------------------

# module variables

class STRvariables(object):

	def __init__(self):

		self.strprint = 'utf-8'				# strings sent to console/list/error file
		self.strstore = 'utf-8'				# strings sent to object code

		self.xlatetable = {}				# translation table

_STR = STRvariables()

# -----------------------------
# psop: ASSUME flag|flag[:=]val
# -----------------------------

def doassume(flag, arg):
	'''check if ASSUME refers to strings'''
	# for output to screen and listing and error files
	if flag == 'printable' and arg in ['ascii', 'latin-1', 'utf-8']:
		_STR.strprint = arg

	# for output to object files
	elif flag == 'objstr':
		if arg in ['utf-16', 'utf-32']:
			_STR.strstore = f'{arg}le' if CG.lsbfirst() else f'{arg}be'
		elif arg in ['ascii', 'latin-1', 'utf-8', 'utf-16be', 'utf-16le', 'utf-32be', 'utf-32le']:
			_STR.strstore = arg

	# not handled here
	else:
		return False

	# handled here
	return True

def storable(this, xlate=True):
	'''return a byte array for output to object files '''
	xstr = this.translate(_STR.xlatetable) if xlate else this
	return xstr.encode( _STR.strstore, errors='backslashreplace' )

def printable(this):
	'''return a string for output to console, listing and error files'''
	if this is None:
		return ''
	else:
		this = this.replace( '\t', '    ' )
		# we take advantage of Python's UTF-8 aware regex matching
		# - there doesn't seem to be an easier way to do this consistently for all encodings
		# - any method that involves string concatenation doesn't work (a Python thing)
		# - any method that lets a codepoint > 255 through doesn't work (a Windows thing)
		# - (so though in theory UTF-8 and Latin-1 should differ, in practice they don't)
		filter = r'[^\x20-\x7f]' if _STR.strprint == 'ascii' else r'[^\x20-\x7f\xa0-\xff]'
		return re.sub(filter, lambda m: f'\\x{ord(m.group()):02X}', this )

def unichr(val):
	''' Unicode char of codepoint val '''
	return chr(val) if 0 <= val <= 0x10FFFF else '?' 

# recognized mnemonic escape sequences

_mnemonEsc = {
	'0': '\x00',
	'b': '\b',
	'f': '\f',
	'n': '\n',
	'r': '\r',
	's': ' ',
	't': '\t',
	'v': '\v',
}

# all recognized escape patterns
# - searching all at once allows one-pass replacement
# - (which also avoids 'created' escape sequence problems)
# - mnemonic escape last to minimize Perl-style 'first match wins' behavior

_allEscapes = r'\\(([$]|0?[xX])([0-9a-fA-F]{2})|([0-9][0-9a-fA-F]|0[0-9a-fA-F]{2})[hH]|u([0-9a-fA-F]{4})|U([0-9a-fA-F]{8})|(.))'

# groups:         (1->                                                                                        )'
# groups:          (2->       )(3->           ) (4->             )      (5->           )  (6->          )  (7)'

def replaceescapes(this):
	''' replace any escape sequences in a string '''

	def _replace(matchobj):
		# found an escape ?
		for i in [3, 4, 5, 6, 7]:
			txt = matchobj.group( i )
			if txt is not None:
				# two, four or eight hex chars ?
				if i < 7:
 					return unichr( int(txt, 16) )
				# mnemonic escape ?
				elif txt in _mnemonEsc:
					return _mnemonEsc[ txt ]
				# return char unchanged 
				else:
					return txt

	return re.sub( _allEscapes, _replace, this )

def strlit(this, delim='"'):
	''' convert string literal to string '''
	if this is None:
		return this

	elif len(this) > 2 and this.startswith(delim) and this.endswith(delim):
		return replaceescapes(this[1:-1])

	else:
		return ''

def chrlit(this):
	'''convert character literal to number'''
	val = strlit( this, "'" )
	if isinstance( val, int ):
		return val
	elif len(val) == 1:
		return ord( val )
	else:
		UM.error( "NeedChr", this )		# malformed or unrecognized escape
		return 0

def rgxlit(this):
	'''convert regex to pattern'''
	# if 'this' is a literal, these tests are unnecessary
	# - but it may be from a string variable
	if this.endswith('/i'):
		regex = this[:-1]
		flag = re.IGNORECASE
	else:
		regex = this
		flag = re.NOFLAG

	regex = strlit( regex, '/' )
	if len(regex):
		try:
			crgx = re.compile( regex, flag )
		except Exception as e:
			this = f'{this}, {e}'
			regex = ''

	if len(regex):
		return ( True, crgx )
	else:
		UM.error( "NeedRegex", this )
		return ( False, None )

# -----------------------------
# psop: XLATE a=b [[, ?=? ]..]
#		XLATE a-b=c [[, ?=?]..]
#		XLATE a=b-c  [[, ?=?]..]
#		XLATE a-b=c-d [[, ?=?]..]
# -----------------------------

def doxlate(label, fields):
	'''handle XLATE psop'''

	def _setxlate(key, val):
		if key != val:
			_STR.xlatetable[ key ] = val
		# if no entry, translate() returns char unchanged
		elif key in _STR.xlatetable:
			del _STR.xlatetable[ key ]

	def _getrange(this):
		'''get character range for translation'''
		if this is not None:
			rng = replaceescapes( this )	# round one if unquoted, round two if quoted
		else:
			rng = "xxxx"					# can't match following

		match len(rng):
			case 1:						# single char ?
				return (ord(rng), ord(rng) )
			case 3 if rng[1] == '-':	# a character range ?
				beg = ord( rng[0] )
				end = ord( rng[2] )
				if beg <= end:
					return ( beg, end )
				else:
					UM.noeffect( this )
			case _:
				UM.error( "NeedXlt", this )

		return ( 0, -1 )

	rplndx, rplend = _getrange( fields[0] )
	wthval, wthend = _getrange( fields[1] )

	# "a-b=c-d" form
	# - until replace range has only one entry left or with range exhausted
	while rplndx < rplend and wthval < wthend:
		_setxlate( rplndx, wthval )
		rplndx += 1
		wthval += 1

	# "a=b", "a-b=c" and "a=b-c" forms
	# - also completes "a-b=c-d" form, repeating "d" as often as needed
	while rplndx <= rplend and wthval <= wthend:
		_setxlate( rplndx, wthval )
		rplndx += 1

def xlate(this):
	'''run value through translation table'''
	return _STR.xlatetable[this] if this in _STR.xlatetable else this

_skipTo = {
	',': "\"'/(,",
	'=': "\"'=",
	':': "\"':",
	}

def splitfield(this, delim=','):
	''' split input string into one or more individual expressions '''
	# - returns a list with at least one element

	# "fast" checks
	# - if no split char in 'this', no further action is necessary
	if this is None or delim not in this:
		return ( True, [this] )

	this = printable( this )
	# even if split char is present:
	# - it may be escaped or within a char, string, regex literal or function call argument list
	# - regex literals are hard because regex delimiter looks like arithmetic divide
	# - so we will ignore those here - any field delimiter in them has to be escaped
	skipping = skipesc = False

	# keep track of where each field starts, parenthesis nesting level
	start = skipparen = 0

	# which characters are important to watch for ?
	important = _skipTo[ delim ]

	fields = []

	for i, ch in enumerate( this ):

		if skipesc:
			skipesc = False					# escapes are unconditional for one character
			continue

		elif ch == '\\':					# escapes can happen inside char, string and regex literals
			skipesc = True
			continue

		elif ch not in important:			# is this a character we need to pay attention to ?
			continue						# no ...

		# if we are skipping, can we stop ?
		if skipping:
			if important == '()':
				skipparen += -1 if ch == ')' else 1
				if skipparen > 0:
					continue

			# '"', "'" and '/' are always the closing match of a pair
			skipping = False
			important = _skipTo[ delim ]

		elif ch == delim:
			fields.append( this[start:i].strip() )
			start = i + 1							# update to start of next field

		# we've found the start of a possible skip section
		# - we look for the existence of a possible close skip section
		# - if we don't find one, this is probably an input mistake
		# - but for the regex delimiter '/', it might not be if the division operator is meant
		# - test can fail if an input line contains two division operators in separate expressions
		else:
			skipping = this.find( ')' if ch == '(' else ch, i+1 ) >= 0
			if skipping:
				important = '()' if ch == '(' else ch
				skipparen = 1					# no effect if important != '()'

	errcnt = UM.geterr()
	# unterminated skip ?
	if skipesc or skipping:
		UM.error( 'BadEOE', this[start:] )
	else:

		# unconditionally take everything left (the last or only field)
		fields.append( this[start:].strip() )

		# check for blank fields caused by:
		# - split char being first or last char of 'this'
		# - two consecutive split chars separated only by zero or more spaces
		err = False
		for i, field in enumerate(fields):
			# is there at least one error ?
			if not len(field):
				fields[i] = '### '
				err = True

		if err:
			UM.error( 'BadField', ', '.join(fields) )

	# done
	return (True, fields) if errcnt == UM.geterr() else (False, None)

def splitequate(this):
	''' split string if it contains an 'equate' pattern '''
	if this is not None and len(this):
		ok, fields = splitfield( this, '=' if '=' in this else ':' )
		if ok and len(fields) > 1:
			return ( True, UTIL.maxfields(fields, 2) )

	UM.error( "NeedEqu", this )
	return ( False, None )
