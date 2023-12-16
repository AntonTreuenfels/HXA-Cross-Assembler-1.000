# Hobby Cross-Assembler (HXA) V1.00 - File Manipulation

# (c) 2021-2023 by Anton Treuenfels

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

# first created: 11/05/21
# last revision: 11/02/23

# preferred public function prefix: "OS"

# -----------------------------
import os
import re
from time import asctime
# other HXA modules
import hxa_usermesg as UM
import hxa_macro as MAC
import hxa_codegen as CG
import hxa_progctr as PC
import hxa_source as SRC
import hxa_misc as UTIL
import hxa_expressions as EXP
# -----------------------------

class OSvariables(object):

	def __init__(self):

		# filenames are complete dvc:\path\filename.ext strings

		self.absname = None				# command line source file

		self.currfile = None			# current file being processed

		self.srcobj = None				# current source file object

		self.filestack = []				# source file stack
		self.fileseq = []				# sequence of source files read

		self.readonce = []				# files tagged as 'read once'

		self.outobj = None				# output file object

		self.fnames = {
			# output file names, default filename extensions
			'errfile':	[None, 'err'],	# error log file
			'listfile':	[None, 'lst'],	# listing file
			'objfile':	[None, 'obj'],	# binary file
			'rawfile':	[None, 'raw'],	# undecorated hex file
			'hexfile':	[None, 'hex'],	# Intel hex file
			'srecfile':	[None, 's19'],	# Motorola hex file
			'objbyseg':	[None, 'obj'],	# binary files
			'rawbyseg':	[None, 'raw'],	# undecorated hex files
			'hexbyseg':	[None, 'hex'],	# Intel hex files
			'srecbyseg': [None, 's19'],	# Motorola hex files
			'objbyblk':	[None, 'obj'],	# binary files
			'rawbyblk':	[None, 'raw'],	# undecorated hex files
			'hexbyblk':	[None, 'hex'],	# Intel hex files
			'srecbyblk': [None, 's19'],	# Motorola hex files
		}

		self.errtext = []				# saved error messages

_OS = OSvariables()

# -----------------------------

def _normalize(fname):
	''' normalize case, slashes and path '''
	return os.path.normpath( os.path.normcase(fname) )

def _rootdir():
	''''return path of root file (should include mount point)'''
	return os.path.dirname( _OS.absname )

def rootfn():
	''' return base name of root file '''
	return os.path.basename( _OS.absname )

def currdir():
	'''return path of current file'''
	return os.path.dirname( _OS.currfile )

def currfn():
	''' return base name of current file '''
	return os.path.basename( _OS.currfile )

def _fullpath(fname):
	''' return full path to named file '''
	# don't change anything if:
	# - 'fname' is an absolute pathname (on any device)
	# - eg., "d:\path\file" or "\path\file"
	# - 'fname' is an explicit relative path (on any device)
	# - eg., "d:path\file" and not just "path\file"
	# - ATM we don't check for explicit relative paths (but we might)
	if not os.path.isabs(fname):
		fname = os.path.join( _rootdir(), fname )
	return _normalize( fname )

def init(name):
	''' complete initializing module '''
	# make absolute path of fname
	absname = _normalize( name )
	if not os.path.isabs(absname):
		absname = os.path.abspath( absname )
	_OS.absname = _OS.currfile = absname
	# base name of root file
	return _OS.absname

def _open(fname, mode):
	'''open a file for reading or writing'''
	# fname is assumed to be a full pathname starting from device root
	try:
		# UTF-8 encoding for reading text files, else use OS default encoding
		fobj = open( fname, mode, encoding='UTF-8' ) if mode == 'rt' else open( fname, mode )
	except FileNotFoundError:
		UM.error( "NoFile", fname )
	except Exception:
		UM.error( 'NotOpen', fname )
	else:
		_OS.currfile = fname
		UM.filestatus( 'Fread' if mode.startswith('r') else 'Fwrite', currfn() )
		return fobj

	# no file opened
	return None

# -----------------------------

def _exists(fname):
	''' check if file exists '''
	if os.path.isfile( fname ):
		return True
	else:
		UM.error( 'NoFile', fname )
		return False

def _closeread():
	''' close source file '''
	if _OS.srcobj is not None:
		_OS.srcobj.close()
		_OS.srcobj = None

def _openread(fname, mode, pos=0):
	''' try to open a file for reading '''
	# just in case
	_closeread()

	_OS.srcobj = _open( fname, mode )
	if not _OS.srcobj:
		return False

	# file pointer can be positioned for read files
	if pos > 0:
		_OS.srcobj.seek( pos )

	return True

def readln():
	''' read a line from text source file '''
	if _OS.srcobj is not None:
		line = _OS.srcobj.readline()
		if len(line) > 0:
			return ( True, line )
		else:
			_closeread()

	return ( False, None )

def _readbin(maxchunk):
	''' read a chunk from a binary source file '''
	if _OS.srcobj is not None:
		chunk = _OS.srcobj.read( min(1024, maxchunk) )
		if len(chunk) > 0:
			return ( True, chunk )
		else:
			_closeread()

	return( False, None )

# -----------------------------

def sourcefile(masterline):
	''' find the name of the source file associated with a masterline '''
	# 'fileseq': [ (master0, file0), (master1, file1), ... ]
	# - 'masterx' is alway one less than the actual first master line of the
	# associated file
	#  master0 = 0 and masterline > 0, so this search should always succeed

	# ...except if file named on command line not found...
	if len(_OS.fileseq) < 1:
		return ( 0, _OS.absname )

	# find the file the master line# belongs to
	fseq = _OS.fileseq.copy()
	while len(fseq):
		fname, firstline = fseq.pop()
		if masterline > firstline:
			soffset = masterline - firstline
			sname = fname
			break

	# if that was all there was to it, we'd be done
	# - but if this file appears multiple times because of nested inclusion,
	# then we may not have the correct offset within this file
	lastfirst = firstline
	while len(fseq):
		fname, firstline = fseq.pop()
		if fname == sname:
			soffset += lastfirst - firstline
		lastfirst = firstline

	return ( soffset, sname )

def sourcenocommon(masterline):
	'''find the name of a source file without common prefix with root file name'''
	foffset, fname = sourcefile( masterline )
	# this works even if 'fname' is the root file name
	common = os.path.commonprefix( [fname, _OS.fileseq[0][0]] )
	# directories may have a common prefix, eg, '\test' and '\testhelp'
	common, _ = os.path.split( common )
	return ( foffset, fname[len(common)+1:] )

# -----------------------------
# source file stacking
# -----------------------------

def _isrootfile():
	return len(_OS.filestack) < 1

def pushfile(name=None, line=0, pos=0):
	''' push source file on stack '''
	# HXA uses only one open source file at a time
	# - mostly so that running out of file descriptors is never a problem
	# - if we ARE pushing an open file, we came across an INCLUDE or INCBIN psop
	# - then we'll want to come back to this point, so we save it
	if _OS.srcobj is not None:
		pos = _OS.srcobj.tell()
		_closeread()

	SRC.setroot( _isrootfile() )

	if name is None:	# stack current file (always a text file)
		_OS.filestack.append( (_OS.currfile, SRC.getmaster(), pos) )
	else:				# stack given file
		_OS.filestack.append( (name, line, pos) )
	MAC.newscope( MAC._incBlk )						# new local scope

def popfile(readmode='rt'):
	''' pop source file from stack and open for reading'''

	def popone(mode):
		'''pop and open top file on file stack'''
		if len(_OS.filestack) < 1 or not MAC.topblock(MAC._incBlk):
			return False

		MAC.oldscope()								# old local scope
		name, line, pos = _OS.filestack.pop()		# unstack file
		fname = _fullpath( name )
		if not _exists(fname):						# does it exist ?
			return False
		if _isrootfile():							# back to command-line file ?
			SRC.setroot( True )

		if _openread(fname, mode, pos):
			_OS.fileseq.append( (_OS.currfile, SRC.getmaster()) )
			return True
		else:
			return False

	# if can't open top include file, revert to the file that included it
	return popone(readmode) or popone('rt')

# -----------------------------
# psop: READONCE
# -----------------------------

def doreadonce(label, expr):
	'''handle READONCE psop'''
	if not _OS.currfile in _OS.readonce:
		_OS.readonce.append( _OS.currfile )

		# circular inclusions of the current file and
		# previous inclusions by the current file
		# do not necessarily lead to errors
		# - but they can, so we'll warn about them
		# - making them errors instead needs to be very careful
		# about preventing cascade errors

		# is the current file also on the open file stack ?
		if _OS.currfile in [fstk[0] for fstk in _OS.filestack]:
			UM.warn( "CircInc", _OS.currfile )

		# has the current file been INCLUDED before now ?
		currseq = [fseq[0] for fseq in _OS.fileseq]
		# last file in sequence is current file, so we don't look at that one
		currseq.pop()
		if _OS.currfile in currseq:
			UM.warn( "PrevInc", _OS.currfile )

# -----------------------------
# psop: INCLUDE name
# -----------------------------

# we do this in a way that lets us take advantage of another
# function's error-handling during source file switching

def doinclude(label, name):
	''' handle INCLUDE psop '''
	fname = _fullpath( name )
	# can't do this while expanding a block (out-of-sequence reads)
	if MAC.expanding():
		UM.error( "BadInExp" )

	# silent check if this file should not be read again
	elif not fname in _OS.readonce:
		# check for duplicate filenames (including path and device)
		if fname in [fseq[0] for fseq in _OS.fileseq]:
			UM.warn( "DupName", fname )

		# stack current file
		pushfile()
		# stack include file
		pushfile( fname, 0 )
		# "restore" include file
		_ = popfile()

# -----------------------------
# psop: INCBIN name
# -----------------------------

def doincbin(label, name, offset, count):
	''' handle INCBIN psop '''
	# test if file exists
	fname = _fullpath( name )
	if not _exists(fname):
		return

	# how big is it ?
	fsize = os.path.getsize( fname )
	# default is to start at beginning of file
	if offset is None:
		offset = 0
	# if less than zero, offset from end of file
	elif offset < 0:
		offset += fsize
	# is the start point within the file ?
	if not UTIL.inrange(offset, 0, fsize-1):
		return

	# how many 8-bit bytes are we supposed to read ?
	# - less than one just means "take everything to end-of-file"
	if count is None or count < 1:
		count = fsize - offset

	# how many can we actually read ?
	elif offset + count > fsize:
		count = fsize - offset
		UM.warn( "BinTrunc", count )

	# stack current file
	pushfile()

	# read binary file
	if _openread(fname, 'rb', offset):
		while True:
			ok, bindata = _readbin( count )
			if ok:
				count -= len( bindata )
				CG.store( 'bytes', bindata )
			else:
				break

	# restore current file
	_ = popfile()

# -----------------------------
# output file handling
# -----------------------------

# -----------------------------
# psop: ERRFILE  [name]
# psop: LISTFILE [name]
# psop: OBJFILE	 [name]
# psop: RAWFILE [name]
# psop: HEXFILE [name]
# psop: SRECFILE [name]
# psop: OBJBYSEG [name]
# psop: RAWBYSEG [name]
# psop: HEXBYSEG [name]
# psop: SRECBYSEG [name]
# psop: OBJBYBLK [name]
# psop: RAWBYBLK [name]
# psop: HEXBYBLK [name]
# psop: SRECBYBLK [name]
# -----------------------------

def dofile(psop, name):
	'''handle ---FILE psops'''
	# what do we have already for this output file type ?
	# - fname.ext (if any) and default extension
	outname, dfltext = _OS.fnames[ psop ]

	# derive default name from first source file name
	pname, _ = os.path.splitext( _OS.absname )
	dfltname = f'{pname}.{dfltext}'

	# no name specified ?
	if name is None:
		fname = dfltname

	# annoyingly enough, 'os.path.normpath()' changes "dir\" to "dir"
	# and then 'os.path.split()' considers "dir" a filename
	# - so we will add a default filename to any path ending in a directory
	elif os.path.isdir(name):
		fname = os.path.join( name, dfltname )

	# do we need to add a default extension ?
	else:
		fname, fext = os.path.splitext( name )
		if len(fext) < 1 or fext == '.':
			fname = f'{name}.{dfltext}'
		else:
			fname = name

	# if not absolute, put file in same directory as root file
	fname = _fullpath( fname )

	# this file type already set to be output ?
	if outname is not None:
		_ = UTIL.samename( fname, outname )
		return

	# we're going to check these
	path, pname = os.path.split( fname )

	# do we need to check for proper template ?
	if not '#' in fname:
		validchars = r'[-._0-9A-Za-z\xA1-\xFF]{1,32}'

	else:
		validchars = r'[-._#0-9A-Za-z\xA1-\xFF]{1,32}'
		# any use like this an error , even if filesystem permits it
		if '#'in path or pname.startswith('#') or re.search(r'#[^#]+#', pname):
			UM.error( "BadSegTmplt", pname if '#' in pname else fname )
			return

	# check for (superficially) valid filename
	# - basically just checks to see if it consists 8-bit characters valid in most filesystems
	# - does not check that the path is valid in either characters or total length
	if not re.fullmatch(validchars, pname):
		UM.odduse( pname )

	# set this name as the output filename for this psop
	_OS.fnames[ psop ][ 0 ] = fname

def outputdefined(ftype):
	'''should we output a particular file type ?'''
	return _OS.fnames[ ftype ][ 0 ] is not None

# -----------------------------

def getasctime():
	# here so it can be used by other modules
	return asctime()

def headerline(this):
	return f'{UM.expandtext("OutPfx")} {this}'

def makeheader(type):
	'''create text file header'''

	def _add(this):
		header.append( headerline(this) )

	header = []
	_, rootfile = sourcefile( 1 )
	_add( f'{UM.expandtext("Version")} {UM.expandtext(type)}' )
	_add( f'{UM.expandtext("InsSet")}: {UM.expandtext("InsAny") if CG.cpu() is None else CG.cpu()}' )
	_add( f'{UM.expandtext("Source")}: {os.path.basename(rootfile)}' )
	_add( f'{UM.expandtext("PrgType")}: {UM.expandtext("IsSeg" if PC.hassegs() else "IsMono")}' )
	_add( getasctime() )

	return header

# -----------------------------

def closeout():
	'''close output file'''
	if _OS.outobj is not None:
		_OS.outobj.close()
		_OS.outobj = None

def _openout(ftype, segnum=1):
	'''try to open a file for writing'''
	# since we only need one output file at at time,
	# an open file here is a mistake (we silently fix it)
	closeout()

	# final check of filename
	outname, dext = _OS.fnames[ ftype ]

	# Motorola ?
	fname, fext = os.path.splitext( outname )
	if fext == '.s19':
		rectype, recchar = CG.motorola_types()
		dext = f'{recchar}{str(rectype)}{str(10-rectype)}'
		outname = f'{fname}.{dext}'

	# a template name ?
	if '#' in outname:
		# replace '#' chars with segment number
		minwid = outname.rfind('#') - outname.find('#') + 1
		template = re.sub( '#+', f'{{:0{minwid}d}}', outname )
		outname = template.format( segnum )

	# derive name from rootfile name and segment name ?
	elif 'by'in ftype:
		dname, _ = os.path.splitext( rootfn() )
		outname = f'{fname}_{PC.getsegname(segnum)}.{dext}'

	fname = _normalize( outname )
	wtype = 'wb' if ftype.startswith('obj') else 'wt'

	_OS.outobj = _open( fname, wtype )

	return True if _OS.outobj is not None else False

def writeout(this):
	'''write a line to text output file'''
	_OS.outobj.write( f'{this}\n' )

# -----------------------------
# error file
# -----------------------------

def errwrite(this):
	''' save error text for later writing to error file (if any) '''
	_OS.errtext.append( this )

def writeerr():
	'''write error file (if any)'''
	# no errors if only two "pass#" messages
	if len(_OS.errtext) > 2 and _openout('errfile'):
		hdr = makeheader( 'ErrFile' )
		for line in hdr:
			writeout( line )
		writeout( '' )
		for line in _OS.errtext:
			writeout( line )

# -----------------------------
# listing file
# -----------------------------

def openlist():
	''' open listing file (if any) '''
	return _openout('listfile')

# -----------------------------
# assembly output files
# -----------------------------

def openoutpfile(ftype, segnum):
	''' open a file for assembly output'''
	return False if PC.isnodata(segnum) else _openout( ftype, segnum )

def asmoutwrite(this):
	''' write byte array to output file '''
	_OS.outobj.write( this )

# ------------------------------
# psop: [label] END [startaddr]			monolithic; root file
# psop: [label] END						monolithic; include file
# psop: END [startaddr]					segmented; root file
# psop: END								segmented; include file
# ------------------------------

def doend(label, addr):
	''' handle END psop '''
	if MAC.openblock():
		UM.warn( 'OddUse' )

	# can't set start adress within include file
	if not _isrootfile() and addr is not None:
		UM.ignored( addr )

	# 'addr' may not be resolved yet if program is segmented
	else:
		CG.store( 'start', addr )

	# kill any macro expansions
	MAC.endsource()

	# note that if 'DEBUGOFF' is in effect,
	# 'UM.debug()' will not show any output during second pass

	# close current file to stop reading from it
	_closeread()
