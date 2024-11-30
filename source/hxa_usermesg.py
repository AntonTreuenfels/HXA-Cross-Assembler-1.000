# Hobby Cross-Assembler (HXA) V1.200 - User Messages (Error and Informational)

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

# first created: 01/18/03	(in Thompson AWK 4.0)
# last revision: 10/14/24

# preferred public function prefix: "UM"

# -----------------------------
import sys
import inspect
# import traceback
# other HXA modules
import hxa_pseudo as PSOP
import hxa_macro as MAC
import hxa_codegen as CG
import hxa_file as OS
import hxa_source as SRC
import hxa_symbol as SYM
import hxa_strings as STR
import hxa_misc as UTIL
# -----------------------------

# default message texts

_mesgText = {

	# internal HXA error/debug messages

	'BadMsg':	"Expanded text not found",
	'NoWay':	"Can't happen",
	'Debug':	"Debug called by",

	# general status messages

	'Fread':	"Reading",
	'Fwrite':	"Writing",
	'BegOne':	"Pass One started",
	'EndOne':	"Pass One ended",
	'BegTwo':	"Pass Two started",
	'EndTwo':	"Pass Two ended",
	'Quit':		"Assembly halted",

	# warning/error/fatal messages

	'ErrFile':	"Error file",
	'Warn':		"Warning in",
	'Error':	"Error in",
	'Fatal':	"Fatal error in",
	'Fault':	"Detail",
	'NoFault':	"No detail",
	'HaveWarn':	"Warnings detected",
	'HaveErr':	"Errors detected",
	'HaveFatal':	"Fatal error detected",
	'BadOp':	"While processing CPU mnemonic",
	'BadMacro':	"While processing macro",
	'BadPsop':	"While processing pseudo opcode",
	'BadLabel':	"While processing label",
	'BadLine':	"While processing line",
	'BadAssert':	"Assertion failed",
	'BadAssume':	"Unrecognized assumption",

	# file messages

	'NoFile':	"File not found",
	'NotOpen':	"Can't open file",
	'CircInc':	"Current file still being read",
	'PrevInc':	"Current file already included",
	'BinTrunc':	"Binary bytes actually read",

	# token messages

	'Ignored':	"Unexpected token(s) ignored",
	'BadToken':	"Unexpected token",
	'BadField':	"Expecting expression",

	# expected token not found messages

	'NeedToken':	"Expecting label or opcode",
	'NeedOpcode':	"Expecting opcode",
	'NeedChr':		"Expecting character value",
	'NeedCond':		"Expecting conditional expression",
	'NeedFile':		"Expecting filename",
	'NeedGlobal':	"Expecting global name",
	'NeedHex':		"Expecting hex character pairs",
	'NeedLabel':	"Expecting label",
	'NeedVarble':	"Expecting variable name",
	'NeedNum':		"Expecting numeric expression",
	'NeedNumNam':	"Expecting numeric name",
	'NeedNumVal':	"Expecting constant numeric expression",
	'NeedStr':		"Expecting string expression",
	'NeedStrNam':	"Expecting string name",
	'NeedRegex':	"Expecting regular expression pattern",
	'NeedEqu':		"Expecting equate pattern",
	'NeedXlt':		"Expecting translate pattern",
	'NeedPos':		"Expecting positive value",
	'NeedCond':		"Expecting conditional expression",
	'NeedFloat':	"Expecting decimal literal",

	# expression parse and evaluation messages

	'BadEOE':		"Unexpected end of expression",
	'BadRgtPar':	"Unmatched right parenthesis",
	'BadLftPar':	"Unmatched left parenthesis",
	'NeedOperand':	"Expecting operand",
	'NeedOperator':	"Expecting operator",
	'NeedFunction':	"Expecting function name",
	'NeedCall':		"Expecting function call",
	'BadFunction':	"Unknown function name",
	'BadFncEval':	"Incomplete evaluation",
	'BadArgCnt':	"Unexpected argument count",
	'BadArgSep':	"Unexpected comma",
	'BadType':		"Unexpected type", 
	'DivZero':		"Divide by zero",
	'BadTrnry1':	"Unmatched '?' operator",
	'BadTrnry2':	"Unmatched ':' operator",
	'BadValStr':	"Expecting non-null string",

	# cpu/instruction set messages

	'BadCPU':	"CPU not recognized",
	'NoCPU':	"CPU type not set",
	'BadMode':	"Unrecognized address mode",

	# segment / program counter messages

	'BadPC': 		"Invalid program counter",
	'SegIsAO':		"Segment is absolute origin",
	'SegIsRO':		"Segment is relative origin",
	'SegIsAE':		"Segment is absolute end",
	'SegIsRE':		"Segment is relative end",
	'SegIsID':		"Segment is initialized",
	'SegIsND': 		"Segment is uninitialized",
	'SegIsPT':		"Segment is pad to",
	'SegIsPF':		"Segment is pad from",
	'SegIsCO':		"Segment is common",
	'SegDfltName':	"Segment #",
	'BadSegUse': 	"Program cannot be both monolithic and segmented",
	'BadSegOut': 	"Legal only inside segment fragment",
	'BadSegAbs':	"Cannot make segment absolute",
	'BadSegTmplt':	"Invalid filename template",

	# symbol table messages

	'RsrvName':	"Reserved name",
	'UndefName':	"Name not found",
	'DupName':	"Duplicate name",

	# block processing messages

	'NeedMacName':	"Expecting macro name",
	'NeedArgDflt':	"Expecting default argument value",
	'NeedArgName':	"Expecting formal argument name",
	'NeedMatch':	"Name does not match",
	'NeedArgVal':	"Expecting actual argument value",
	'BadDef':		"Definition ignored",
	'BadBlock':		"Matching block structure not found",
	'BadOpenBlk':	"Unclosed open block structure",
	'BadNestBlk':	"Unclosed nested block within block expansion",
	'BadOutExp': 	"Allowed only within block expansion",
	'BadInExp':		"Not allowed within block expansion",

	# listing messages

	'ListFile':	"Listing File",
	'InsSet':	"Instruction Set",
	'InsAny':	"Unspecified",
	'Source':	"Source file",
	'PrgType':	"Program Type",
	'IsSeg':	"Segmented",
	'IsMono':	"Monolithic",
	'NoRecord':	"   (No data recorded)",
	'OBJ':		"Object Code Listing",
	'LBL':		"Symbol Table Listing",
	'XRF':		"Cross-Reference Listing",
	'SEG':		"Segment Map Listing",
	'STS':		"Assembly Statistics Listing",
	'Glbl':		"Global Labels",
	'Auto':		"Local, Variable and Anonymous Labels",
	'NumAlpha':	"Numeric Name     Ref Cnt    Hex Value    Dec Value",
	'NumValue':	"Numeric Value    Ref Cnt    Hex Value    Dec Value",
	'NAformat':	" {:<18} {:^4s}   ${:>9s} {:>12d}",
	'StrAlpha':	"String Name      Ref Cnt   Value",
	'SAformat':	' {:<18} {:^4s}   "{}"',	# single quotes protect double quotes
	'Mac':		"Macros",
	'MacAlpha':	"Name            Exp Cnt",
	'MacFormat':	" {:<18} {:>3s}",
	'XrefAlpha':	"Event Listing# Source#  File",
	'SegCols':		"Num - Name       Hex Value    Dec Value",
	'SegNumNam':	"{:03} - {}",
	'SegOff':	" Object Offset  ${:>9s}  {:>11s}",
	'SegBeg':	" Start Address  ${:>9s}  {:>11s}",
	'SegLen':	"   Byte Length..${:>9s}  {:>11s}",
	'SegEnd':	"   End Address..${:>9s}  {:>11s}",
	'BadPagFmt':	"Invalid Page Format",
	'__PassOne':	"Pass One time",
	'__PassTwo':	"Pass Two time",
	'SrcLines':	"    Source Lines",
	'ExpLines':	" Expansion Lines",
	'TotLines':	"     Total Lines",
	'LinesSec':	"Lines per second",
	'DataVals':	"    Data values stored",
	'ValsSec':	"Resolutions per second",
	'ObjSize':	"Object Bytes",

	# range errors

	'BadRngLo':	"Value less than minimum",
	'BadRngHi':	"Value greater than maximum",
	'BadRange':	"Value is out of range",

	# over internal limit messages

	'maxwarn':		"Warning count",
	'maxerr':		"Error count",
	'maxloop':		"Loop body count",
	'maxdepth':		"Block nesting depth",
	'maxputback':	"Putback line count",
	'maxseg':		"Segment count",
	'maxstack':		"User stack depth",

	# output line prefixes

	'OutPfx':	"; ***",
	'ErrPfx':	"; >>>>>",
	'ErrPfx2':	"; -",
	'ErrPfx3':	";",
	'ErrPfx4':	"; >>> In",
	'InfoPfx':	"*****",
	'EquIfx':	"=",
	'InIfx':	"in",

	# miscellaneous messages

	'UniqVal':		"Value already set",
	'OddVal':		"Unusual value",
	'OddUse': 		"Unusual use",
	'NoEffect':		"No effect",
	'TimerReset':	"Timer reset to zero",
	'StkEmpty':		"User stack empty",
	'StkNotEmpty':	"User stack not empty",
	'TotTime':		"Total Time"

}

# -----------------------------

# module variables

class UMvariables(object):

	def __init__(self):

		self.errcnt = 0
		self.warncnt = 0
		self.warntot = 0
		self.fatalcnt = 0

		self.verbose = True
		self.showwarn = True
		self.debug = True

_UM = UMvariables()
		
def init(vernum, verstr):
	''' complete initializing module '''

	_mesgText[ 'VerNum' ] = vernum
	_mesgText[ 'VerStr' ] = verstr
	_mesgText[ 'Version' ] = f'{CG.name()} {verstr}'

# -----------------------------

def _flag(this):
	''' decorate text so it stands out '''
	if this is None or this == '':
		return ''
	else:
		return f': < {this} >'

def expandtext(key):
	'''get message text associated with key (if key exists)'''
	if key in _mesgText:
		return _mesgText[key]
	else:
		return f'{_mesgText["BadMsg"]} {_flag(key)}'

def _expandcause(key, cause):
	''' get expanaded error message text with flagged cause (if any) '''
	return f'{expandtext(key)}{_flag(cause)}'

def eqformat(tag, val):
	'''format name/value pair for display'''
	return f' {tag} {expandtext("EquIfx")} {val}'

# -----------------------------
# write text
# -----------------------------

def _stdout(text):
	''' write message to standard output '''
	if _UM.verbose:
		print( STR.printable(text) )

def newline():
	_stdout( None )

def firestop(key, cause=None):
	''' write errror message to standard output only '''
	newline()
	_stdout( f'{expandtext("ErrPfx")} {_expandcause(key, cause)}' )

def _msgout(this):
	''' write message to standard output and error file (if any) '''
	_stdout( this )
	OS.errwrite( STR.printable(this) )

def _msgoutnl(this):
	_msgout( this )
	_msgout( '' )     # essentially a newline

# -----------------------------
# status/informational messages
# -----------------------------

def _caller():
	'''find name of function that called this function's caller'''
	f1 = inspect.stack()
	frame, filename, lineno, function, code_context, index = f1[2]
	foffset, fname = OS.sourcefile( SRC.getmaster() )
	return f'{function}(): {expandtext("BadLine")}: {foffset} {expandtext("InIfx")} {expandtext("Source")}: {OS.currfn()}'

def debug(*lookat):
	''' internal debugging'''
	if _UM.debug:
		firestop( 'Debug', _caller() )
		for name, val in lookat:
			_stdout( f'{type(val)}  {eqformat(name, val)}' )
		newline()

def useage():
	''' show useage message '''
	# make sure this message goes to console
	quiet( False )
	newline()
	_stdout( 'useage: python hxa.py [drive:][path]filename -cpuhandler [-h] [-q]' )
	newline()
	_stdout( '[drive:][path]filename    source file to assemble' )
	newline()
	_stdout( '-cpuhandler               cpu-specific handler file' )
	newline()
	_stdout( '-h, --help, /?            show this message and exit' )
	_stdout( '-q, --quiet               disable console output' )

def info(key):
	''' print general informational message '''
	text = f'{expandtext("InfoPfx")} {expandtext(key)}'
	_stdout( text )
	return text

def filestatus(key, fname):
	''' print file status message '''
	_stdout( f'{expandtext(key)}: {fname}' )

# -----------------------------
# error message display
# -----------------------------
	
def _showstumble(type, key, cause=None):
	''' show error message and the source code that triggerd it '''

	def circumstance(text):
		''' what kind of source line is this ? '''
		tokens = SRC.stripcomment(text).split()
		token0 = tokens.pop(0) if len(tokens) > 0 else text
		token1 = tokens.pop(0) if len(tokens) > 0 else None

		if PSOP.ispseudo(token0):
			return ( 'BadPsop', token0 )
		elif MAC.ismacro(token0):
			return ( 'BadMacro', token0 )
		elif CG.isop(token0):
			return ( 'BadOp', token0 )
		elif SYM.islabel(token0):
			if token1 is None:				# no second token ?
				return ( 'BadLabel', token0 )
			elif PSOP.ispseudo(token1):
				return ( 'BadPsop', token1 )
			elif MAC.ismacro(token1):
				return ( 'BadMacro', token1 )
			elif CG.isop(token1):
				return ( 'BadOp', token1 )
			else:
				return ( 'BadToken', token1 )
		else:
			return ('BadToken', token0)

	def _showsource(offset, text):
		''' show the source of a line involved in an error'''
		# what does HXA think is happening ?
		# - it may not be the same what the user thinks !
		stumble, token = circumstance( text )

		# line# displayed is:
		# - offset from file start if text came from file
		# - offset from last text that came from a file if text came from expansion
		# - we don't worry about perversities such as the same file being read twice
		_msgout( f'{expandtext("ErrPfx2")} {_expandcause(stumble, token.upper())}' )
		_msgout( f'{expandtext("ErrPfx3")} {offset}: {text}' )

	# <-- main -->

	errline = SRC.getmaster()

	# no valid current source line (ie., no pass active) ?
	if not errline:
		firestop( key, cause )

	else:

		# get the filename and offset within file of error line
		foffset, fname = OS.sourcefile( errline )

		# show the file the error line either came from or was expanded within
		_msgout( f'{expandtext("ErrPfx")} {expandtext(type)} {fname}' )

		# show all currently open blocks
		# - 'sline' is absolute, 'soffset' is relative to 'sline'
		# - last line shown is the one that actually triggered the error
		for sline, soffset in MAC.getblockstarts(errline):
			# 'foffset' is relative to file start
			foffset, currname = OS.sourcefile( sline )
			source = SRC.recall( sline )
			if currname != fname:
				fname = currname
				_msgout( f'{expandtext("ErrPfx4")} {fname}' )
			_showsource( f'^{soffset:03d}' if soffset > 0 else f'{foffset:04d}', source[soffset] )

		# (finally) show what HXA doesn't like about the error line
		_msgoutnl( f'{expandtext("ErrPfx2")} {_expandcause(key, cause)}' )

# -----------------------------

def geterr():
	''' return current error count '''
	return _UM.errcnt

def geterrcode():
	'''get errcode'''
	# errcode is bit-mapped (SET= TRUE, CLEAR= FALSE)
	# - bit 0 : warning(s) happened  (but assembly continued)
	# - bit 1 : error(s) happened	(assembly stopped after current pass complete)
	# - bit 2 : fatal error happened (assembly stopped immediately)
	errcode = 1 if _UM.warncnt or _UM.warntot else 0
	errcode |= 2 if _UM.errcnt else 0
	errcode |= 4 if _UM.fatalcnt else 0
	return errcode

def showerrcnt():
	'''show warning/error/fatal counts'''

	def _showerrcnt(type, count):
		''' show error count (if any) '''
		if count > 0:
			_msgout( f'{count} {expandtext(type)}' )

	_showerrcnt( 'HaveWarn',  _UM.warncnt - _UM.warntot )
	_showerrcnt( 'HaveErr',   _UM.errcnt )
	_showerrcnt( 'HaveFatal', _UM.fatalcnt )

	# save total warn count through this pass
	# - next pass will show only warn count from that pass
	_UM.warntot += _UM.warncnt

def quitonerr():
	'''quit on anything but a warning'''
	showerrcnt()
	if geterrcode() > 1:
		info( 'Quit' )
		OS.writeerr()
		sys.exit( geterrcode() )

# -----------------------------
# fatal error
# -----------------------------

def fatal(key, cause=None):
	''' report fatal error and terminate assembly '''
	_showstumble('Fatal', key, cause)
	_UM.fatalcnt = 1
	quitonerr()

def noway(cause=None):
	''' fatal internal error '''
	fatal( 'NoWay', f'{_caller()}: {cause}' if cause is not None else _caller() )

# -----------------------------
# non-fatal error
# -----------------------------

def error(key, cause=None):
	''' report non-fatal error '''
	_showstumble( 'Error', key, cause )
	_UM.errcnt += 1
	UTIL.checkmax( 'maxerr', _UM.errcnt )

def errlabel(key, label=None):
	if label is not None:
		error( key, SYM.unmakeauto(str(label)).upper() )
	else:
		noway( key )

def nofile(name):
	errlabel( 'NoFile', name )

def reserved(name):
	errlabel( 'RsrvName', name )

def undefined(name):
	errlabel( 'UndefName', name )

def duplicate(name):
	errlabel( 'DupName', name )

def notglobal(name):
	# need global numeric
	errlabel( 'NeedGlobal', name )
	if SYM.isstr(name):
		errlabel( 'NeedNumNam', name )

# -----------------------------
# non-fatal warning
# -----------------------------

def warn(key, cause=None):
	''' show warning message '''
	_showstumble( 'Warn', key, cause )
	_UM.warncnt += 1
	UTIL.checkmax( 'maxwarn', _UM.warncnt )

def ignored(cause):
	warn( 'Ignored', cause )

def odduse(cause):
	warn( 'OddUse', cause.upper() )

def oddval(cause):
	warn( 'OddVal', cause )

def unique(cause):
	warn( 'UniqVal', cause )

def noeffect(cause):
	warn( 'NoEffect', cause )

# -----------------------------
# pseudo ops
# -----------------------------

def userfault(handler, cause):
	'''dispatch user fault handler'''
	if cause is not None and len(cause) > 0:
		handler( 'Fault', cause )
	else:
		handler( 'NoFault' )

# ECHO [opt-string]

def doecho(label, text):
	''' handle ECHO psop '''
	_msgoutnl( text )

# WARN [opt-string]

def dowarn(label, cause):
	''' handle WARN psop '''
	userfault( warn, cause )

# ERROR [opt-string]
	
def doerror(label, cause):
	''' handle ERROR psop '''
	userfault( error, cause )

# FATAL [opt-string]

def dofatal(label, cause):
	''' handle FATAL psop '''
	userfault( fatal, cause )

# MESGTEXT key=text [[, key=text]...]

def domesgtext(label, equate):
	''' handle MESGTEXT psop '''
	key, text = equate
	if key in _mesgText:
		_mesgText[ key ] = STR.replaceescapes( text )
	else:
		undefined( key )

# -----------------------------

def quiet(default=True):
	'''disable output to stdout'''
	_UM.verbose = False if default else True

# WARN[ON|OFF]

def dowarnstate(psop, expr):
	'''handle WARNxx psops'''
	_UM.showwarn = (psop == 'warnon')

# DEBUG[ON|OFF] 

def dodebug(psop, expr):
	'''handle DEBUGxx psops'''
	_UM.debug = (psop == 'debugon')





