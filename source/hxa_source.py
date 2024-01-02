# Hobby Cross-Assembler (HXA) V1.00 - Source Text Management

# (c) 2004-2022 by Anton Treuenfels

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

# first created: 05/16/03		(in Thompson AWK 4.0)
# last revision: 12/30/23

# preferred public function prefix: "SRC"

# -----------------------------
import re
# other HXA modules
import hxa_usermesg as UM
import hxa_macro as MAC
import hxa_codegen as CG
import hxa_progctr as PC
import hxa_symbol as SYM
import hxa_file as OS
import hxa_strings as STR
import hxa_misc as UTIL
# -----------------------------

# module constants

# listing options (user to internal form)

_listOpt = {

	'OBJECT':	'OBJ',
	'SOURCE':	'SRC',
	'INCLUDES':	'INC',
	'MACROS':	'EXP',
	'UNTAKEN':	'UTK', 

	'LABELS':	'LBL',
	'LBLVAL':	'LBV',
	'AUTOS':	'AUT',
	'MACNAMES':	'MAC',

	'ALLEQU':	'EQU',

	'XREF':		'XRF',
	'XMACROS':	'XMC',
	'XGLOBALS':	'XGL',

	'SEGMENTS':	'SEG',
	'PADDING':	'PAD',

	'STATS':	'STS',

	'LINENUMS':	'NUM',
	'LINEWRAP':	'WRP',

	'ALL':		'ALL',
}

# module variables

class SRCvariables(object):

	def __init__(self):
	
		self.masterline = 0			# total number of lines read from all files
		self.mastermax = 0			# maximum value of 'masterline' (for listing)

		self.putbacktext = None		# source line pushed back on input (if any)

		self.offset = 0				# offset of expansion line from from source line
		self.explines = 0			# total number of non-comment expansion lines (macros, whiles, repeats)

		self.textsave = {}			# source text store (for listing, expansions and error reporting)

		self.list = {				# default listing flags (keys are also keys in user message table)
			'OBJ': True,			# source and expansion lines which produced object code (master)
			'SRC': True,			# source lines which produced no object code
			'INC': True,			# include files
			'EXP': False,			# expansion lines which produced no object code
			'UTK': False,			# untaken conditional branches

			'LBL': True,			# global numeric and string symbols (master)
			'LBV': False,			# global numeric symbols by value
			'AUT': False,			# variable, local and anonymous symbols
			'MAC': True,			# macro names

			'EQU': False,			# EQU psop assignments (non-global labels)

			'XRF': False,			# macro /global label cross reference (master)
			'XGL': False,			# global cross ref
			'XMC': False,			# macro cross ref

			'SEG': True,			# segment map (master; only if program is segmented)
			'PAD': True,			# data of pad segments (after END)

			'STS': False,			# stats (master)

			'NUM': False,			# number listing lines ?
			'WRP': True,			# wrap listing lines > textWid ? 

		}

		self.taken = True			# start off in TRUE branch of imagined enclosing IF..ENDIF block
		self.condbranch = {}		# track conditional branches
		self.liston = {}			# track listing option flags turned on
		self.listoff = {}			# track listing option flags turned off
		self.rootflag = {}			# lines which mark include file nesting start/end

		self.pageMax = 256			# maximum height, width of page (if specified by user)
		self.pageWid = [False, 0]	# page width (zero = no upper limit)
		self.pageLen = [False, 0]	# page height (zero = no upper limit)

		self.topMrg = [False, 0]	# page top margin
		self.lftMrg = [False, 0]	# page left margin
		self.botMrg = [False, 0]	# page bottom margin
		self.rgtMrg = [False, 0]	# page right margin

		self.lineSpc = [False, 1]	# line spacing

		self.title = [False, None]	# user-specified listing header

		self.textWid = None			# printable width (for pages with limits)
		self.textLen = None			# printable length (for pages with limits)

		self.pageLine = 0			# current printing line on page
		self.lineNum  = None		# current line#	(if printing line numbers)

		self.formfeed  = []			# page lines on which to formfeed (if any)

		self.xrefevtln = {}			# cross-reference event record (source line)
		self.xreflstln = {}			# cross-reference listing line

_SRC = SRCvariables()

# -----------------------------
# set/get module variables
# -----------------------------

def getmaster():
	return _SRC.masterline

def setmaster(this):
	_SRC.masterline = this

def getoffset():
	return _SRC.offset

def setoffset(this):
	_SRC.offset = this

def _getlinekey():
	return ( _SRC.masterline, _SRC.offset )

# -----------------------------

def _getlist(flag):
	'''get state of a list flag'''
	return _SRC.list[ flag ]

def listequ():
	'''get state of 'EQU' flag'''
	return _getlist( 'EQU' )

def setlist(flags, state):
	for flag in flags:
		_SRC.list[ flag ] = state

# -----------------------------
# psop: LISTON  [[option] [[,option]..]]
# psop: LISTOFF [[option] [[,option]..]]
# -----------------------------

def dolist(psop, option):
	'''handle LIST-- psops'''
	# do we recognize this flag ?
	if option is None:
		option = 'OBJECT'
	option = option.upper()
	if not option in _listOpt:
		UM.ignored( option )
		return

	state = True if psop == 'liston' else False
	# convert option to internal form
	ndx = _listOpt[ option ]
	# set flag now so any master flags are in effect at start of listing
	_SRC.list[ ndx ] = state
	# record for listing
	key = _getlinekey()

	# turn option on ?
	if psop == 'liston':
		if not key in _SRC.liston:
			_SRC.liston[ key ] = []
		_SRC.liston[ key ].append( ndx )

	# turn off
	else:
		if not key in _SRC.listoff:
			_SRC.listoff[ key ] = []
		_SRC.listoff[ key ].append( ndx )

# -----------------------------

def setcond(state):
	''' set conditional branch flag (for listing) '''
	# try to minimize how often this toggles
	if state != _SRC.taken:
		_SRC.condbranch[ _getlinekey() ] = _SRC.taken = state

def setroot(state):
	''' set include file flag (for listing) '''
	_SRC.rootflag[ _getlinekey() ] = state

# -----------------------------

def recall(masterline):
	'''return all saved lines associated with a given master line'''
	return _SRC.textsave[masterline].copy()

# -----------------------------

def stripcomment(text):
	'''remove any comment starting somewhere after first non-whitespace char '''
	# only '*' is not a legal comment marker now
	# - we will still require '#' to be surrounded by whitespace
	m = re.search( '[^ \t]([ \t]+)(;|#([^a-zA-Z]|$)|//)', text )
	return text if m is None else text[:m.start(1)]

def ignore(text):
	''' test if source line should be completely ignored'''
	# - ignore if null
	# - comment if very first char is ';', '#', '*' or '//'
	# - comment if the first non-whitespace char is '*' or '#'
	#   followed by whitespace
	# - comment if the first non-whitespace char is ';' or '//'
	return (
		not len(text)
		or text.startswith( (';', '#', '*', '//') )
		or text.lstrip().startswith( (';', '# ', '#\t', '* ', '*\t', '//') )
		)

def fetch(linenum):
	'''retrieve next non-comment source line from saved text'''
	# guaranteed to be from file, so guaranteed to find it
	while ignore(_SRC.textsave[linenum][0]):
		linenum += 1
	return ( linenum, _SRC.textsave[linenum][0] )

# -----------------------------
# psop: PUTBACK  exprfield
# psop: PUTBACKS expr$
# -----------------------------

def doputback(label, putback):
	''' push text back on input '''
	if MAC.inexpansion():
		_SRC.putbacktext = putback
		_SRC.putback += 1
		UTIL.checkmax( 'maxputback', _SRC.putback )

# -----------------------------

def nextline():
	''' read next source line '''

	# read from macro expansion ?
	if MAC.expanding():

		# was a line pushed back on source ?
		# - either zero or one such line
		if _SRC.putbacktext is None:
			text = _SRC.textsave[ MAC.getreadndx() ][0]
		else:
			text = _SRC.putbacktext
			_SRC.putbacktext = None

		# retrieve next non-comment source line
		# - if loop is entered, guaranteed to be from file
		# - so guaranteed to find it
		while ignore(text):
			text = _SRC.textsave[ MAC.getreadndx() ][0]

		text = MAC.subactualargs( text )

		# save it in the same list with the line from a source file that
		# started this expansion
		_SRC.textsave[ _SRC.masterline ].append( text )

		# - mark its offset in data storage (for listing and error reporting)
		# - check for too many expansion lines
		_SRC.offset += 1

	# read from file
	else:

		while True:

			ok, text = OS.readln()

			# end of file ?
			if not ok:
				_SRC.mastermax = getmaster()		# for listing (in case this is last file)
				return ( False, None )

			# strip off trailing whitespace
			# - result is null string if blank line
			text = text.rstrip()

			# save all text read from files
			_SRC.masterline += 1
			_SRC.textsave[ _SRC.masterline ] = [ text ]

			# non-comment line ?
			if not ignore(text):
				break

		_SRC.explines += _SRC.offset
		_SRC.offset = _SRC.putback = 0					# reset

	text = stripcomment( text )

	# replace tabs with spaces (tabs are not significant after this)
	return ( True, text.lstrip().replace('\t', ' ') )

def pseudoline(text = ''):
	'''insert a "line" after last actual source line'''
	# this can only happen during pass one
	# - so 'mastermax' is last actual source line, 'masterline' is last total source line
	_SRC.masterline += 1
	_SRC.textsave[ _SRC.masterline ] = [ text ]

# -----------------------------
# Listing File Support
# -----------------------------

# possible listing line formats:

# <- lftMrg -><- linenum  -><linetype><-  object  -><- text -><- rgtMrg-->

# <- lftMrg -><- linenum  -><linetype><-  spaces  -><- text -><- rgtMrg ->

# <- lftMrg -><linetype><-  object  -><-       text         -><- rgtMrg ->

# <- lftMrg -><linetype><-  spaces  -><-       text         -><- rgtMrg ->
#             |                                               |
#         left margin                                    right margin
#              <-            text width                      ->
# <-                         page width                                 ->

def makeformats():
	'''create derived listing values'''
	errs = UM.geterr()

	# page character width is limited ?
	# - text width doesn't matter if page width unlimited
	if _SRC.pageWid[1] > 0:
		_SRC.textWid = _SRC.pageWid[1] - (_SRC.lftMrg[1] + _SRC.rgtMrg[1])
		# print line numbers ?
		if _getlist('NUM'):
			# account for 4-digit line number + space
			_SRC.textWid -= 5
		if not UTIL.inrange(_SRC.textWid, 1, _SRC.pageWid[1]):
			UM.error( "BadPagFmt" )

	# page line length is limited ?
	# - text height doesn't matter if page length unlimited
	if _SRC.pageLen[1] > 0:
		_SRC.textBot = _SRC.pageLen[1] - _SRC.botMrg[1]
		if not UTIL.inrange(_SRC.textBot, 1, _SRC.pageLen[1]):
			UM.error( "BadPagFmt" )

	return errs == UM.geterr()

# A page:

#       +---pagWid-----------------------------------+
#       |                     |                      |
#       |    Margin Area   topMrg                    |
#    pagLen                   |                      |
#       |          +---txtWid-------------+          |
#       |          |                      |          |
#       |          |    Printable Area    |          |
#       |       txtLen                    |          |
#       |          |                      |          |
#       |--lftMrg--|                      |--rgtMrg--|
#       |          |                      |          |
#       |          |                      |          |
#       |          |                      |          |
#       |          |                      |          |
#       |          |                      |          |
#       |          +----------------------+          |
#       |                     |                      |
#       |                  botMrg                    |
#       |                     |                      |
#       +--------------------------------------------+

def setformat(dflt, new, minval=0):
	'''check page format value'''
	# 'new' is valid ?
	if new is not None and UTIL.inrange(new, minval, _SRC.pageMax-1):

		isset, old = dflt
		# already set ?
		if isset:
			UTIL.sameval( new, old )
		# new value
		elif makeformats():
			return [ True, new ]

	return dflt

# -----------------------------
# psop: TITLE [string]
# -----------------------------

def dotitle(label, new):
	'''handle TITLE psop'''
	isset, old = _SRC.title
	if isset:
		UTIL.sameval( new, old )
	else:
		_SRC.title = [True, new]

# -----------------------------
# psop: PAGESIZE width [,length]
# -----------------------------

def dopagesize(label, pwid, plen):
	'''handle PAGESIZE psop'''
	_SRC.pageWid = setformat( _SRC.pageWid, pwid )
	_SRC.pageLen = setformat( _SRC.pageLen, plen )

# -----------------------------
# psop: MARGINS top, lft [, bot [, rgt]]
# -----------------------------

def domargins(label, mtop, mlft, mbot, mrgt):
	'''handle MARGINS psop'''
	_SRC.topMrg = setformat( _SRC.topMrg, mtop )
	_SRC.lftMrg = setformat( _SRC.lftMrg, mlft )
	_SRC.botMrg = setformat( _SRC.botMrg, mbot )
	_SRC.rgtMrg = setformat( _SRC.rgtMrg, mrgt )

# -----------------------------
# psop: LINESPACE count
# -----------------------------

def dolinespace(label, count):
	'''handle LINESPACE psop'''
	_SRC.lineSpc = setformat( _SRC.lineSpc, count, 1 )

# -----------------------------
# psop: PAGE
# -----------------------------

def dopage(label, arg):
	'''handle PAGE psop'''
	_SRC.formfeed.append( _getlinekey() )

# -----------------------------
# Cross-Reference Support
# -----------------------------

def _xrefon():
	return _getlist('XRF') or _getlist('XGL') or _getlist('XMC')

def _xrefevent(name, event):
	'''record cross-reference event'''
	if _xrefon():
		if name not in _SRC.xrefevtln:
			_SRC.xrefevtln[ name ] = []
		_SRC.xrefevtln[name].append( [_SRC.masterline, _SRC.offset, event] )
		_SRC.xreflstln[ _getlinekey() ] = 0

# record macro name event
def macdefine(name):
	_xrefevent( name, 'Def' )
def macexpand(name):
	_xrefevent( name, 'Exp' )
def macundef(name):
	_xrefevent( name, 'Und' )

# record global name event
def glbequate(name):
	_xrefevent( name, 'Equ' )
def glbreference(name):
	_xrefevent( name, 'Ref' )

# record listing line a cross-reference appears on (if any)
def _xreflistline(master, offset):
	key = ( master, offset )
	if key in _SRC.xreflstln:
		_SRC.xreflstln[ key ] = _SRC.lineNum

# -----------------------------

def list():

	def _exp(key):
		return UM.expandtext(key)

	def _initlist():
		''' initialize listing'''
		# change format variables to integers for easier handling
		_SRC.pageWid = _SRC.pageWid[ 1 ]
		_SRC.pageLen = _SRC.pageLen[ 1 ]

		_SRC.topMrg = _SRC.topMrg[ 1 ]
		_SRC.lftMrg = _SRC.lftMrg[ 1 ]
		_SRC.botMrg = _SRC.botMrg[ 1 ]
#		_SRC.rgtMrg = _SRC.rgtMrg[ 1 ]

		_SRC.lineSpc = _SRC.lineSpc[1]

		# line numbering on? (could double as flag)
		_SRC.lineNum = 1 if _getlist('NUM') else 0

		# any cross-reference ?
		if _getlist('XRF'):
			setlist( ['XGL', 'XMC'], True )
		else:
			_SRC.list[ 'XRF' ] = _xrefon()

		# any segment map ?
		_SRC.list[ 'SEG' ] &= PC.hassegs()

	def _skipline(count):
		'''print a blank listing line'''
		while count > 0:
			OS.writeout( '' )
			count -= 1

	def _formfeed():
		'''skip to next page'''
		if _SRC.pageLen > 0:
			_skipline( _SRC.pageLen - _SRC.pageLine + 1 )
			_SRC.pageLine = 0

	def _writeline(text):
		''' write one line to listing file'''

		# is there a top margin ?
		if _SRC.pageLen > 0 and (_SRC.pageLine == 0 or _SRC.pageLine > _SRC.textBot):
			_skipline( _SRC.topMrg )
			_SRC.pageLine = _SRC.topMrg + 1

		# number lines ?
		if _getlist('NUM'):
			text = f'{_SRC.lineNum:04d} {text}'
			_SRC.lineNum += 1

		# is there a left margin ?
		if _SRC.lftMrg:
			text = f'{" " * _SRC.lftMrg}{text}'

		# write the line
		OS.writeout( STR.printable(text) )

		# not paginating ?
		if _SRC.pageLen == 0:
			_skipline( _SRC.lineSpc - 1 )

		# paginating
		else:
			_skipline( min(_SRC.lineSpc - 1, _SRC.textBot - _SRC.pageLine) )
			_SRC.pageLine += _SRC.lineSpc
			if _SRC.pageLine > _SRC.textBot:
				_skipline( _SRC.botMrg )

	def _newline(tag=''):
		'''write a newline to listing file'''
		_writeline( tag )

	def _listline(text, tag=None):
		''' list one line, breaking up long lines if necessary '''

		def breakpoint(text, skipover):
			'''find a place to break a long line'''
			rcom = text.rfind( ',', 0, _SRC.textWid ) + 1
			rspc = text.rfind( ' ', skipover, _SRC.textWid ) + 1

			return rcom if rcom > rspc else rspc if rspc > 0 else _SRC.textWid

		pline = text if tag is None else f'{tag}{text}'
		# output text is wider than text width ?
		while _SRC.pageWid > 0 and len(pline) > _SRC.textWid:
			# wrap excess to successive lines ?
			if _getlist('WRP'):
				spaces = '  ' if tag is None else CG.leadingblanks()
				# don't forget to account for additional chars besides spaces
				breakat = breakpoint( pline, len(spaces) + 3 )
				_writeline( pline[:breakat] )
				pline = f'{"" if tag is None else tag}{spaces}  {pline[breakat:]}'
			# truncate (also breaks loop)
			# - truncated line will have _SRC.textWid chars (numbered [0, _SRC.textWid-1])
			else:
				pline = pline[:_SRC.textWid]

		# last (or only) line
		_writeline( pline )

	def _listnoprefix(key):
		'''write info line without prefix'''
		_listline( _exp(key) )
		_newline()

	def _listprefix(key):
		'''write info line with prefex'''
		_listline( f'{_exp("OutPfx")} {_exp(key)}' )
		_newline()

	def _listnorecord():
		'''list section has no data'''
		_listnoprefix( 'NoRecord' )

	def _showsection(section):
		'''show section header'''
		if _SRC.list[section]:
			_listprefix( section )
			return True

		return False

	def _listheader():
		'''write listing header'''
		# user title ?
		isset, title = _SRC.title
		if isset:
			if title is None:
				return
			else:
				hdr = [ OS.headerline(title) ]
		else:
			hdr = OS.makeheader( "ListFile" )
		# print from here so formatting works properly
		for line in hdr:
			_listline( line )
		_newline()

	def _listobject():
		''' list source and any object code '''

		# anything to list ?
		if _SRC.mastermax < 1:
			_listnorecord()
			return

		# at start we are always in a true branch of the root file
		isroot = listbranch = True

		# go through each line, listing padded segments after last 'real' source line
		for srcline in range(1, getmaster()+1 if _getlist('PAD') else _SRC.mastermax+1):

			# go through every piece of source text associated with this line
			for offset, srctext in enumerate(_SRC.textsave[srcline]):

				# state change key (should match any getline() result stored earlier)
				key = ( srcline, offset )

				# process TRUE special flags in source line record
				# - set here so lines which set them are shown
				if key in _SRC.condbranch and _SRC.condbranch[key]:
					listbranch = True
				elif key in _SRC.liston:
					setlist( _SRC.liston[key], True )

				# is the master list flag enabled ?
				if _getlist('OBJ'):

						issource = (offset < 1)
						if issource:
							tag = ' ' if isroot else '+'
						else:
							tag = '^' if isroot else '>'

						# always list if data was generated...
						if CG.hasdata(srcline, offset):
							object = CG.objectcode( srcline, offset )
							_xreflistline( srcline, offset )
							_listline( f'{object.pop(0)}  {srctext}', tag )
							while len(object) > 0:
								_listline( object.pop(0), tag )

						# ...else try to list non-data generating line
						# - flags checked in descending order of priority
						elif ( _getlist('SRC')					# source listing enabled ?
							and ( isroot or _getlist('INC') )	# include listing enabled ?
							and ( issource or _getlist('EXP') )	# expansion listing enabled ?
							and listbranch						# conditional listing enabled ?
						):
							if len(srctext) > 0:				# non-blank line ?
								_xreflistline( srcline, offset )
								_listline( f'{CG.leadingblanks()}  {srctext}', tag )
								if key in _SRC.formfeed:		# never a data-generating line
									_formfeed()
							else:
								_newline( tag )

				# process FALSE special flags in source line record
				# - set here so lines which set them are shown
				if key in _SRC.condbranch and not _SRC.condbranch[key]:
					listbranch = _getlist( 'UTK' )
				elif key in _SRC.listoff:
					setlist( _SRC.listoff[key], False )

				# rootfile flag set here so it takes effect on *next* line
				if key in _SRC.rootflag:
					isroot = _SRC.rootflag[ key ]

		_newline()

	def _fmtname(this):
		return this[:18]

	def _fmtcnt(cnt):
		return str(cnt) if cnt > 0 else ' '

	def _listlabels():
		'''list user labels'''

		def _listnum(template, name, val, refcnt):
			'''list numeric label'''
			_listline( template.format(_fmtname(name), _fmtcnt(refcnt), f'{val:02X}', val) )

		def _liststr(template, name, val, refcnt):
			''' list string label'''
			_listline( template.format(_fmtname(name), _fmtcnt(refcnt), STR.printable(val)) )

		def _listmac(template, name, refcnt):
			'''list macro name'''
			_listline( template.format(_fmtname(name), _fmtcnt(refcnt)) )

		def _listsyms(fetch, heading, format, output):
			'''list symbols of specified type and order'''
			# fetch the symbols and counts we want to output
			lbls = fetch()
			# header line describing the symbols
			_listnoprefix( heading )
			# do we actually have any symbols ?
			if not len(lbls):
				_listnorecord()
			else:
				# get the specified output format
				template = _exp( format )
				for lbl in lbls:
					# send each symbol and count to the specified output function
					output( template, *lbl )
				_newline()

		# global numeric and string
		_listprefix('Glbl')
		_listsyms(SYM.getnumalpha, 'NumAlpha', 'NAformat', _listnum)		# numeric by name
		if _getlist('LBV'):
			_listsyms( SYM.getnumvalue, 'NumValue', 'NAformat', _listnum )	# numeric by value
		_listsyms( SYM.getstralpha, 'StrAlpha', 'SAformat', _liststr )		# string by name

		# local, variable and anonymous by name (internal name, if replaced)
		if _getlist('AUT'):
			_listprefix('Auto')
			_listsyms( SYM.getnumauto, 'NumAlpha', 'NAformat', _listnum )	# numeric by name
			_listsyms( SYM.getstrauto, 'StrAlpha', 'SAformat', _liststr )	# string by name

		# macro names
		if _getlist('MAC'):
			_listprefix('Mac')
			_listsyms( MAC.getmacros, 'MacAlpha', 'MacFormat', _listmac )		# by name

	def _showhistory(name, events):
		'''show cross-reference history'''
		_listline( _fmtname(name) )
		for event in events:
			sourceln, soffset, type = event
			foffset, fname = OS.sourcenocommon( sourceln )
			txt = f' {type}    '
			lstln = _SRC.xreflstln.get( (sourceln, soffset), 0 )
			txt += f'{lstln:04d}' if lstln > 0 else '    '
			txt += f'    {foffset:04d}'
			if fname != OS.rootfn():
				txt += f'    {fname}'
			_listline( txt )

		_newline()

	def _collectxref(names, type, tag, events):
		if _getlist(type):
			# build history of names with specified event (in order of events)
			xrefs = {}
			for name in names:
				history = [ event for event in _SRC.xrefevtln[name] if event[2] in events ]
				if len(history):
					xrefs[ name ] = history
			# display history
			_listprefix( tag )
			if not len(xrefs):
				_listnorecord()
			else:
				_listnoprefix( 'XrefAlpha' )
				for name in xrefs:
					_showhistory( name, xrefs[name] )

	def _listxref():
		names = sorted( _SRC.xrefevtln )
		_collectxref( names, 'XGL', 'Glbl', ['Equ', 'Ref'] )
		_collectxref( names, 'XMC', 'Mac', ['Def', 'Exp', 'Und'] )

	def _listsegmap():
		'''list segment map'''
		_listnoprefix( 'SegCols' )
		for i in range(1, PC.getsegcnt()):
			segdesc = PC.listseg( i )
			for text in segdesc:
				_listline( text )
			_newline()

	def _liststats():
		'''list internal statistics'''
		def _showequ(key, val, crlf=True):
			_writeline( UM.eqformat(_exp(key), val) )
			if crlf:
				_newline()

		def _showtime(key, psecs):
			_showequ( key, UTIL.elapsedtime(psecs) )

		def _showrate(key, val, nsecs):
			secs = nsecs / 1e9
			_showequ( key, f'{val/secs if secs > 0 else val*100:.1f}' )

		def _passtime(num):
			pname, psecs = UTIL.getpasstime(num)
			_showtime( pname, psecs )
			return psecs

		p1time = _passtime( 'One' )

		_showequ( 'SrcLines', _SRC.mastermax, False )
		_showequ( 'ExpLines', _SRC.explines, False )
		_showequ( 'TotLines', _SRC.mastermax + _SRC.explines )
		_showrate( 'LinesSec', _SRC.mastermax + _SRC.explines, p1time )

		p2time = _passtime( 'Two' )

		objcount, objsize = CG.objectdesc()
		_showequ( 'DataVals', objcount )
		_showrate( 'ValsSec', objcount, p2time )

		_showequ( 'TotTime', UTIL.elapsedtime(p1time + p2time) )

		_showequ( 'ObjSize', objsize )


	# main logic

	# do we have a listing file ?

#	if not makeformats():
#		UM.error( "BadPagFmt" )

	if makeformats() and OS.openlist():

		_initlist()

		_listheader()

		if _showsection('OBJ'):
			_listobject()

		if _showsection('LBL'):
			_listlabels()

		if _showsection('XRF'):
			_listxref()

		if _showsection('SEG'):
			_listsegmap()

		if _showsection('STS'):
			_liststats()

		OS.closeout()
