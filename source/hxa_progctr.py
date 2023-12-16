# Hobby Cross-Assembler (HXA) V1.00 - Program Counter Management

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

# first created: 03/11/03	(in Thompson AWK 4.0)
# last revision: 08/18/23

# preferred public function prefix: PC

# -----------------------------
import re
# other HXA modules
import hxa_macro as MAC
import hxa_codegen as CG
import hxa_source as SRC
import hxa_symbol as SYM
import hxa_usermesg as UM
import hxa_misc as UTIL
# -----------------------------

# module variables

class PCvariables:

	def __init__(self):

# 		self.min = 0				# minimum legal pc value
		self.max = 0				# maximum legal pc value
		self.maxone = 0				# maximum legal pc value plus one

		self.width = None			# effective pc bit width

		self.nextaddr = -1			# actual next address
		self.pendingorg = None		# next origin

		self.explicitsegs = None	# flag: segments are explicit
		self.segcnt = 0				# total number of segments (0 is a flag in monolithic programs)
		self.currseg = None			# current segment number
		self.segments = {}			# segment descriptors
		self.segnames = {}			# segname to segnumber dictionary
		self.segstk = []			# segment nesting

_PC = PCvariables()

# ----------------------------------

# a class for describing segements

class segment:

	def __init__(self, segnum, segname):

		self.num = segnum		# segment number
		self.type = None		# eventually one of ['absorg', 'relorg', 'absend', 'relend']
		self.name = segname		# segment name

		self.offset = 0			# offset from absolute origin (aka segment program counter)
		self.maxoffset = 0		# max offset (always increases except for 'common' segments)
		self.objoffset = 0		# offset of absolute start address in object code

		self.absorg = None		# absolute start address
		self.absend = None		# absolute end address

		self.padbound = None	# padding boundary
		self.padbytes = None	# value(s) to pad with

		self.isabs	= False		# flag: segment is absolute
		self.isnodata = False	# flag: segment cannot store data
		self.iscommon = False	# flag: all segment fragments overlap

# ----------------------------------

def _showsegment(i):
	UM.debug(
		("number", _PC.segments[i].num), ("type", _PC.segments[i].type), ("name", _PC.segments[i].name),
		("offset", _PC.segments[i].offset), ("maxoffset", _PC.segments[i].maxoffset), ("objoffset", _PC.segments[i].objoffset),
		("absorg", _PC.segments[i].absorg), ("absend", _PC.segments[i].absend),
		("padbound", _PC.segments[i].padbound), ("padbytes", _PC.segments[i].padbytes),
		("isabs", _PC.segments[i].isabs), ("isnodata", _PC.segments[i].isnodata), ("iscommon", _PC.segments[i].iscommon)
	)

def _showsegments(pos=None):

	if pos is not None:
		UM.debug( (pos, None) )
	if _PC.segcnt < 1:
		UM.debug( ("No segments exist yet", None) )
	else:
		for i in _PC.segments:
			_showsegment( i )

# ----------------------------------
# make a new segment
# ----------------------------------

def _newsegment(name):
	# create new segment
	_PC.segcnt += 1
	UTIL.checkmax( 'maxseg', _PC.segcnt )
	newseg = segment( _PC.segcnt, f'{UM.expandtext("SegDfltName")}{_PC.segcnt}' if name is None else name )
	_PC.segments[ newseg.num ] = newseg
	# segname to segnumber dictionary
	_PC.segnames[ newseg.name ] = newseg.num
	# current segment is the one we just created
	_PC.currseg = _PC.segcnt

def _setsegabsorg(addr):
	# set current segment to absolute origin
	_PC.segments[ _PC.currseg ].type = 'absorg'
	_PC.segments[ _PC.currseg ].offset = addr
	_PC.segments[ _PC.currseg ].absorg = addr

def _newsegabsorg(addr):
	_newsegment( None )
	_setsegabsorg( addr )
#	_showsegment( _PC.currseg )

# ----------------------------------

def getsegcnt():
	''' get final segment count '''
	# add one so we can use range)(1, getsegcnt())
	return _PC.segcnt + 1

# ----------------------------------

def _segerr(ndx, seg=None):
	'''report segment error'''
	if seg is None:
		seg = _PC.currseg
	UM.error( ndx, _PC.segments[seg].name )

def _segfatal(ndx, seg=None):
	if seg is None:
		seg = _PC.currseg
	UM.fatal( ndx, _PC.segments[seg].name )

# ----------------------------------
# program counter(s) validity checks
# ----------------------------------

def _pcinvalid():
	''' invalid pc value is fatal '''
	# bad, bad program counter ! what did you do ?

	# CPU set ?
	if _PC.width is None:
		UM.error( 'NoCPU' )

	# program counter underflow / overflow
	if _PC.currseg is not None:
		_segfatal( 'BadPC' )
	# between segments ?
	elif _PC.explicitsegs:
		UM.error( 'BadSegOut' )

	UM.fatal( 'BadPC' )

def _pcvalid(seg, addr):
	''' check if a segment pc value is valid (to have) '''
	if not UTIL.inrange( addr, 0, _PC.maxone ):
		_PC.currseg = seg
		_pcinvalid()

# ----------------------------------
# segment validity checks
# ----------------------------------

def _segvalid():
	''' fatal error if not currently in a valid segment '''
	# within a segment ?
	if _PC.currseg is None:
		_pcinvalid()

# ----------------------------------

def _pcget():
	''' get offset value of current segment '''
	_segvalid()
	# do we need a new absolute segment (monolithic only) ?
	if _PC.pendingorg is not None and _PC.pendingorg != _PC.nextaddr:
		_newsegabsorg( _PC.pendingorg )
	# always...
	_PC.pendingorg = None

	return _PC.segments[ _PC.currseg ].offset

def _pcset(addr):
	''' set offset value of current segment '''
	_segvalid()
	# if type not yet set, this segment defaults to relative origin
	if _PC.segments[_PC.currseg].type is None:
		_PC.segments[_PC.currseg].type = 'relorg'
	_PC.segments[ _PC.currseg ].offset = addr

# ----------------------------------

def _pclegal():
	'''test if program counter is legal (to have)'''
	addr = _pcget()
	if UTIL.inrange(addr, 0, _PC.maxone):
		return addr
	else:
		_pcinvalid()		# fatal error

def valid(addr):
	''' check if address is legal (to store data) '''
	# used for second pass resolved values
	if _PC.width is not None:
		return UTIL.inrange( addr, 0, _PC.max )
	else:
		_pcinvalid()

# -----------------------------

def add(val):
	''' add value to program counter '''
	# only the code generator module calls this after saving data
	_pcset( _pcget() + val )
	# this is the next consecutive pc value
	_PC.nextaddr = _pclegal()

# -----------------------------


def getwidth():
	''' get program counter width '''
	return _PC.width

def setwidth(bits):
	''' set program counter default limits '''
	# can be called by "CPU" or "ASSUME" psops in either order

	def _setmax(bits):
		''' set fundamental pc limits '''
		# - 'maxone' is the value immediately after the last legal byte location
		# - we need it because storing a value in the last legal location causes
		# the pc to advance to an illegal location
		# - this is ok as long it's only one byte and we don't try to store anything there
		_PC.width = bits
		_PC.maxone = 2 ** bits
		_PC.max = _PC.maxone - 1

	# sanity check
	if not UTIL.inrange(bits, 8, 32):
		return False

	# initial set or set narrower ?
	# - could be from "CPU" or "ASSUME" psop
	if getwidth() is None:
		_setmax( bits )

	# set narrower ?
	# - setting larger has essentially no effect; lower limits remain in place
	elif bits < getwidth():
		_setmax( bits )

		# check that all segments "fit"
		# - this can happen only once, since only one re-size is permitted
		for i in _PC.segments:
			_pcvalid( i, _PC.segments[i].offset )

	return True

# -----------------------------

# all HXA programs are segmented, either implicitly or explicitly
# - the difference is whether or not the 'segment' psop is used
# - each segment has its own program counter, which is actually
# just the offset from the start address (absolute origin) of the
# segment it is associated with

# if implicit segments ('org' appears before 'segment' or 'usesegments')
# - the program is monolithic (one block)
# - if there are multiple segments, they originated in multiple
# uses of the 'org' pseudo op or expressions which changed the
# program counter in a discontinuous fashion
# - all such segments are absolute origin
# - the physical arrangment of the object code is the same as the
# order of the source code

# if explicit segments ('segment' or 'usesegments' appears before 'org')
# - 'org' only appears within segment fragments
# - the program may contain multiple blocks (segements)
# - segments may be absolute origin, absolute end, relative origin or
# relative end
# - the physical arrangement of the object code may be different from the
# arrangement of the source code

def _hastype(badtypes):
	'''check for incompatible segment types'''
	# must currently be in a segment
	if not _PC.explicitsegs:
		UM.fatal( 'BadSegOut' )
	_segvalid()

	# check for incompatible combinations

	seg = _PC.segments[ _PC.currseg ]
	if "CO" in badtypes and seg.iscommon:
		err = "SegIsCO"
	elif "ND" in badtypes and seg.isnodata:
		err = "SegIsND"
	elif seg.type is None:
		return False
	elif "AO" in badtypes and seg.type == 'absorg':
		err = "SegIsAO"
	elif "AE" in badtypes and seg.type == 'absend':
		err = "SegIsAE"
	elif "RO" in badtypes and seg.type == 'relorg':
		err = "SegIsRO"
	elif "RE" in badtypes and seg.type == 'relend':
		err = "SegIsRE"
	elif "PT" in badtypes and seg.type == 'padto':
		err = "SegIsPT"
	elif "PF" in badtypes and seg.type == 'padfrom':
		err = "SegIsPF"
	else:
		return False

	_segerr( err )
	return True

# -----------------------------

def plausible(pcval):
	''' check if proposed program counter value is plausible '''
	# if not already set, set segmented program flag to false
	# - so program will be monolithic
	if _PC.explicitsegs is None:
		_PC.explicitsegs = False

	if ( _PC.width is None								# CPU not set ?
		or not UTIL.inrange(pcval, 0, _PC.maxone)		# pc out of range ?
		or (_PC.explicitsegs and _PC.currseg is None)	# between segments ?
	):
		_pcinvalid()

# -----------------------------
# psop: FILL count [, hex$]
# -----------------------------

def dofill(label, count, fillbytes):
	'''handle FILL psop'''
	plausible( count )
	CG.fill( count, fillbytes )

def padfill(segnum, count, tag):
	''' fill a padding segment at fixup time'''
	if count > 0:
		# set relative address for CG.store()
		_PC.currseg = segnum
		_pcset( 0 )
		SRC.pseudoline()
		SRC.pseudoline( f'{_PC.segments[segnum].name}' )
		SRC.pseudoline( f'    {tag}  {UTIL.iformat(_PC.segments[segnum].padbound)}' )
		dofill( None, count, _PC.segments[segnum].padbytes )

	return count

# -----------------------------

def _padtocount(boundary, startfrom):
	'''get count of bytes to pad to next boundary'''
	if boundary > 0:
		# how many bytes from previous boundary are we ?
		# ex1: startfrom = 1, boundary = 4, then bytes = 1
		# ex2: startfrom = $801, boundary = $200, then bytes = 1
		bytes = startfrom % boundary
		# if zero, we are sitting on a boundary now...
		if bytes > 0:
			# ex1: bytes = 1, boundary = 4, then bytes = 3 (to next boundary)
			# ex2: bytes = 1, boundary = $200, then bytes = $1ff (to next boundary)
			return boundary - bytes
	# no effect
	return 0

def _execsegpadto(segnum, startat):
	'''fill a PADTO segment at absolute fixup time'''
	bound = _PC.segments[segnum].padbound
	return startat + padfill( segnum, _padtocount(bound, startat), '.padto' )

def _execsegpadfrom(segnum, endat):
	'''fill a PADFROM segment at absolute fixup time'''
	bound = _PC.segments[segnum].padbound
	# how many bytes from previous boundary are we ?
	# ex1: endat = 1, boundary = 2, then bytes = 1
	# ex2: endat = $801, boundary = $200, then bytes = 1

	return endat - padfill( segnum, endat % bound if bound > 0 else 0, '.padfrom' )

def _setsegpad(incompatible, type, boundary, padbytes=None):
	'''set segment delayed padding'''
	plausible( boundary )

	# default fill value
	if padbytes is None:
		padbytes = bytearray( '\x00'.encode('utf-8') )

	incompatible.extend(['AO', 'RO', 'AE', 'RE', 'CO', 'ND'])
	if not _hastype(incompatible):
		if _PC.segments[_PC.currseg].type is None:
			_PC.segments[_PC.currseg].type = type
			_PC.segments[_PC.currseg].padbound = boundary
			_PC.segments[_PC.currseg].padbytes = padbytes
		else:
			UTIL.sameval( boundary, _PC.segments[_PC.currseg].padbound )
			UTIL.sameval( padbytes, _PC.segments[_PC.currseg].padbytes )

# -----------------------------
# psop: PADTO boundary [, hex$]
# -----------------------------

def dopadto(label, boundary, padbytes):
	'''handle PADTO psop'''
	if _PC.explicitsegs:
		_setsegpad( ['PF'], 'padto', boundary, padbytes )
	else:
		dofill( None, _padtocount(boundary, _pcget()), padbytes )

# -------------------------------
# psop: PADFROM boundary [, hex$]
# -------------------------------

def dopadfrom(label, boundary, padbytes):
	'''handle PADFROM psop'''
	_segvalid()
	if _PC.explicitsegs:
		_setsegpad( ['PT'], 'padfrom', boundary, padbytes )
	else:
		UM.error( "IsMono" )

# -----------------------------

def segorigin(i):
	'''get segment origin'''
	return _PC.segments[i].absorg if _PC.segments[i].type == 'absorg' else 0

# -----------------------------
# psop: UNINITIALIZED
# -----------------------------

def douninitialized(_label=None, _expr=None):
	'''handle UNINITIALIZED psop'''
	_segvalid()
	if not isnodata(_PC.currseg):
		# not compatible with padded segments
		if not _hastype(['PT', 'PF']):
			# program counter must not have changed
			if _pcget() == segorigin(_PC.currseg):
				_PC.segments[ _PC.currseg ].isnodata = True
			else:
				_segerr( "SegIsID" )

	return _PC.segments[ _PC.currseg ].isnodata

# -----------------------------
# psop: COMMON
# -----------------------------

def docommon(_label=None, _expr=None):
	'''handle COMMON psop'''
	if douninitialized():
		_PC.segments[ _PC.currseg ].iscommon = True

def clearcurrseg():
	'''clear current segment'''
	if _PC.currseg is not None:
		# note maximum "segment" program counter value
		# this only matters for COMMON segments (but doesn't hurt anything if we always do it)
		_PC.segments[ _PC.currseg ].maxoffset = max( _PC.segments[_PC.currseg].offset, _PC.segments[_PC.currseg].maxoffset )

		# callers may assume 'currseg' is None after call returns
		_PC.currseg = None

# -----------------------------
# psop: USESEGMENTS
# -----------------------------

def dousesegments(_label=None, _expr=None):
	''' handle USESEGMENTS psop '''
	#  not essential to be explicit but helps clarify intent
	if _PC.explicitsegs is None:	# 'org' not used yet ?
		_PC.explicitsegs = True
	elif not _PC.explicitsegs:		# already monolithic ?
		UM.fatal( 'BadSegUse' )

def hassegs():
	'''explicit segments used?'''
	# if program counter never moved, we have to watch for None value
	return True if _PC.explicitsegs else False

# -----------------------------
# psop: SEGMENT name
# -----------------------------

def dosegment(label, name):
	'''handle SEGMENT psop'''
	# implicitly declare (if not already known)
	dousesegments()

	# 'None' if not a nested segment
	_PC.segstk.append( _PC.currseg )

	# clear current segment
	clearcurrseg()

	# an existing segment ?
	name = name.upper()
	if name in _PC.segnames:
		_PC.currseg = _PC.segnames[ name ]
		if _PC.segments[_PC.currseg].iscommon:
			_PC.segments[_PC.currseg].offset = segorigin( _PC.currseg )

	# if does not exist, create a new segment
	else:
		_newsegment( name )

	# isolate segment locals
	MAC.newscope( MAC._segBlk )

# -----------------------------
# psop: ENDSEGMENT [name]
# -----------------------------

def doendsegment(label, name):
	'''handle ENDSEGMENT psop'''
	# top open block is segment block and names match ?
	if MAC.topblock(MAC._segBlk) and UTIL.samename(name, _PC.segments[_PC.currseg].name):
		# lose segment locals
		MAC.oldscope()
		# clear segment
		clearcurrseg()
		# parent if nested segment, else 'None'
		_PC.currseg = _PC.segstk.pop()

# -----------------------------

def _isabsseg(i):
	return i in _PC.segments and _PC.segments[i].isabs

def getsegorg(i):
	return _PC.segments[i].absorg

def _getsegend(i):
	return _PC.segments[i].absend

def _getseglen(i):
	return _getsegend(i) - getsegorg(i)

def _getsegoff(i):
	return _PC.segments[i].objoffset if _isabsseg(i) and not _PC.segments[i].isnodata else None

def isnodata(i):
	'''is this segment 'nodata'?'''
	return i in _PC.segments and _PC.segments[i].isnodata

def seghasdata(i):
	'''does this segment contain data (to output)?'''
	return not isnodata(i) and _isabsseg(i) and _getseglen(i) > 0

def getsegname(i):
	'''get segment name'''
	return _PC.segments[i].name

# -----------------------------

def _getsegval(name, _getvalfrom):
	'''get a segment value given its name'''
	# common method for SEG---() functions
	if name in _PC.segnames:
		segnum = _PC.segnames[ name ]
		if _isabsseg(segnum):
			val =_getvalfrom( segnum )
			if val is not None:
				return ( True, val )

	return ( False, None )

def getsegbeg(name):
	'''get segment absolute start address'''
	return _getsegval( name, getsegorg )

def getsegend(name):
	'''get segment absolute end address'''
	return _getsegval( name, _getsegend )

def getseglen(name):
	'''get segment byte length'''
	return _getsegval( name, _getseglen )

def getsegoff(name):
	'''get byte offset of segment in object code'''
	return _getsegval( name, _getsegoff )

# -----------------------------

def makeabsolute():
	'''resolve absolute start and absolute end addresses of each segment'''
	totalresolved = 0
	while totalresolved < _PC.segcnt:
		resolved = 0
		# check each segment
		for i in _PC.segments:

			# already resolved ?
			if _PC.segments[i].isabs:
				continue

			# nothing ever changed the segment program counter ?
			if _PC.segments[i].type is None:
				_PC.segments[i].type = 'relorg'

			havetype = _PC.segments[i].type
			# monolithic programs never change 'maxoffset'
			maxoffset = max( _PC.segments[i].offset, _PC.segments[i].maxoffset )

			# absolute origin ?
			if havetype == 'absorg':
				_PC.segments[i].absend = maxoffset
				_PC.segments[i].isabs = True
				resolved += 1

			# relative origin ?
			elif havetype == 'relorg':
				# first segment cannot be relative origin
				if i > 1 and _PC.segments[i-1].isabs:
					_PC.segments[i].absorg = _PC.segments[i-1].absend
					_PC.segments[i].absend = _PC.segments[i].absorg + maxoffset
					_PC.segments[i].isabs = True
					resolved += 1

			# absolute end ?
			elif havetype == 'absend':
				_PC.segments[i].absorg = _PC.segments[i].absend - maxoffset
				_PC.segments[i].isabs = True
				resolved += 1

			# relative end ?
			elif havetype == 'relend':
				# last segment cannot be relative end
				if i < _PC.segcnt and _PC.segments[i+1].isabs:
					_PC.segments[i].absend = getsegorg( i+1 )
					_PC.segments[i].absorg = _PC.segments[i].absend - maxoffset
					_PC.segments[i].isabs = True
					resolved += 1

			# pad to a boundary ?
			elif havetype == 'padto':
				# first segment cannot be pad to
				if i > 1 and _PC.segments[i-1].isabs:
					absorg = _PC.segments[i-1].absend
					_PC.segments[i].absorg = absorg
					_PC.segments[i].absend = _execsegpadto( i, absorg )
					_PC.segments[i].isabs = True
					resolved += 1

			# pad from a boundary ?
			elif havetype == 'padfrom':
				# last segment cannot be pad from
				if i < _PC.segcnt and _PC.segments[i+1].isabs:
					absend = _PC.segments[i+1].absorg
					_PC.segments[i].absend = absend
					_PC.segments[i].absorg = _execsegpadfrom( i, absend )
					_PC.segments[i].isabs = True
					resolved += 1

			# unknown...
			else:
				UM.noway( _PC.segments[i].name )

		# at least one new resolution ?
		if resolved > 0:
			totalresolved += resolved
		# we're stuck...
		else:
			break

	# complete checking
	errs = UM.geterr()
	for i in _PC.segments:
		if _PC.segments[i].isabs:
			_pcvalid( i, _PC.segments[i].absorg )	# fatal error
			_pcvalid( i, _PC.segments[i].absend )	# fatal error
		else:
			_segerr( "BadSegAbs", i )

	# all segments absolute ?
	if errs != UM.geterr():
		return False

	# determine object offsets
	offset = 0
	for i in _PC.segments:
		if not isnodata(i):
			seglen = _getseglen( i )
			if seglen > 0:
				_PC.segments[i].objoffset = offset
				offset += seglen
			else:
				_PC.segments[i].isnodata = True

	return True

# -----------------------------
# read "program counter" value
# -----------------------------

def get():
	''' read program counter (for symbol value and expression evaluation) '''
	# a  relative ( segnum, offset ) tuple
	tuple = ( _PC.currseg, _pclegal() ) if _PC.pendingorg is None else ( 0, _PC.pendingorg )
	return tuple

def read():
	''' get program counter (for data storage) '''
	if isnodata(_PC.currseg):
		if _PC.explicitsegs:
			# cannot store data in uninitialized segment
			_segfatal( "SegIsND" )
		else:
			_newsegabsorg( _pcget() )

	# is data storage valid here ?
	addr = _pcget()
	if UTIL.inrange(addr, 0, _PC.max):
		return ( _PC.currseg, addr )
	else:
		_pcinvalid()

def fetch():
	''' unconditionally read progam counter '''
	return get() if _PC.currseg is not None else None

def isaddr(data):
	''' check if data represents an address '''
	return isinstance(data, tuple)

def gotrel(addr):
	''' check if addr is absolute or relative '''
	segnum, offset = addr
	return segnum > 0 and _PC.segments[ segnum ].type != 'absorg' 

def getabs(this):
	''' convert relative address to absolute '''
	if isaddr(this):
		segnum, offset = this
		return offset if segnum == 0 or _PC.segments[segnum].type == 'absorg' else _PC.segments[segnum].absorg + offset
	else:
		return this

def getseg(addr):
	''' get segment part of address '''
	return 0 if addr is None else addr[0]

# -----------------------------
# psop: [label] ABSORG addr
# -----------------------------

def doabsorg(label, addr):
	''' handle ABSORG psop '''
	plausible( addr )

	# segmented ?
	if _PC.explicitsegs:
		# current segment has no type ?
		if _PC.segments[_PC.currseg].type is None:
			# this segment is absolute origin (of course)
			_setsegabsorg( addr )

		# already incompatible type or different address ?
		elif ( _hastype(['AE','RE','RO', 'PT', 'PF'])
			or not UTIL.sameval(addr, _PC.segments[_PC.currseg].absorg)
		):
			return

	# monolithic
	elif _PC.segcnt == 0:
		_newsegabsorg( addr )
	else:
		# watch for needing a new implicit segment
		_PC.pendingorg = addr

	# this keeps the value associated with the right line in listing
	CG.store( 'org', addr )
	# if segmented, this is always the current segment absolute origin value,
	# and not the current segment pc value (wherever it occurs in the fragment)
	SYM.add( label, addr )

# -----------------------------
# psop: RELORG
# -----------------------------

def dorelorg(label, expr):
	'''handle RELORG psop'''
	# check for incompatible type
	if not _hastype(['AO','AE', 'RE', 'PT', 'PF']):
		_PC.segments[_PC.currseg].type = 'relorg'

# -----------------------------
# psop: [label] ABSEND addr
# -----------------------------

def doabsend(label, addr):
	'''handle ABSEND psop'''
	# check for bad address and incompatible type and bad address
	plausible( addr )
	if _hastype(['AO','RE','RO', 'PT', 'PF']):
		return

	# current segment has no type ?
	if _PC.segments[_PC.currseg].type is None:
		# this value is fixed for this segment
		_PC.segments[_PC.currseg].type = 'absend'
		_PC.segments[_PC.currseg].absend = addr

	# not same addresss ?
	elif not UTIL.sameval(addr, _PC.segments[_PC.currseg].absend):
		return

	# this can happen multiple times without complaint
	CG.store( 'org', addr )
	SYM.add( label, addr )

# -----------------------------
# psop: RELEND
# -----------------------------

def dorelend(label, expr):
	'''handle RELEND psop'''
	# check for incompatible type
	if not _hastype(['AO','AE', 'RO', 'PT', 'PF']):
		_PC.segments[_PC.currseg].type = 'relend'

# -----------------------------
# psop: [label] DS size
# -----------------------------

def dods(label, size):
	''' handle DS psop '''
	plausible( size )				# negative size (or too large) ?
	plausible( _pcget() + size )	# too large ?

	# segmented ?
	if _PC.explicitsegs:
		# rule out data containing segments
		if not douninitialized():
			return

	# monolithic (therefore also absolute)
	elif not isnodata(_PC.currseg):
		# this is just for 'ds' immediately following 'org'
		# - eliminates any zero-length segment
		if _PC.segments[_PC.currseg].absorg != _PC.segments[_PC.currseg].offset:
			_newsegabsorg( _pcget() )
		_PC.segments[ _PC.currseg ].isnodata = True

	# for both
	CG.store( 'ds', size )
	add( size )

# -----------------------------
# Listing support
# -----------------------------

# a dictionary to convert segment types to message indices
# - we could use the messages indices themselves as the segment types (or vice-versa),
# if we wanted to save a little time and space

_type2ndx = {
	'absorg': "SegIsAO", 'absend': "SegIsAE",
	'relorg': "SegIsRO", 'relend': "SegIsRE",
	'padto': "SegIsPT", 'padfrom': "SegIsPF",
	}

def listseg(num):
	'''create listing description of one segment'''

	def _addval(key, val):
		text = UM.expandtext( key ).format( f'{val:02X}', f'{val}' )
		desc.append( text )

	def _addstr(key, val):
		text = UM.expandtext( key ).format( f'{CG.fmtaddr(val)}', f'{val}' )
		desc.append ( text )

	seg = _PC.segments[ num ]
	desc = []
	desc.append( UM.expandtext('SegNumNam').format(seg.num, seg.name) )
	desc.append( UM.expandtext(_type2ndx[seg.type]) )

	# no data ?
	if seg.isnodata:
		desc.append( UM.expandtext("SegIsND") )
		if seg.iscommon:
			desc.append( UM.expandtext("SegIsCO") )

	# has data (hence also a byte offset in object code)
	else:
		_addval( "SegOff", _getsegoff(num) )

	# both
	_addstr( "SegBeg", getsegorg(num) )
	_addval( "SegLen", _getseglen(num) )
	_addstr( "SegEnd", _getsegend(num) )

	return desc
