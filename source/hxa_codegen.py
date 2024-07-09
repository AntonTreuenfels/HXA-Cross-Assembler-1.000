# Hobby Cross-Assembler (HXA) V1.002 - Object Code Management

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

# first created: 03/22/03	(in Thompson AWK 4.0)
# last revision: 07/07/24

# preferred public function prefix: CG

# -----------------------------
import re
from importlib import import_module
# other HXA modules
import hxa_pseudo as PSOP
import hxa_usermesg as UM
import hxa_progctr as PC
import hxa_source as SRC
import hxa_symbol as SYM
import hxa_expressions as EXP
import hxa_file as OS
import hxa_strings as STR
import hxa_misc as UTIL
# -----------------------------

class CGvariables(object):

	def __init__(self):

		self.cpu = None					# the imported instruction handler module
		self.cpuname = None				# specific cpu name
		self.octets = None				# number of 8-bit octets in a "byte"

		# these next three are for the case where no CPU is ever specified
		# if not, no object code was saved and there is no need to list it
		# - however there may have been some NON-object code saved,
		# and we may need to list it
		# - so these are a mimimal "CPU" (which will be overwritten if one is specified)

		self.pcbits = 16				# number of bits in the program counter

		self.lsbfirst = False			# native byte order (default is MSB first)

		self.datasize = { "bit32": 4 }	# recognized data storage psops

		self.datasegs = None			# segments which contain object data
		self.datastore = {}				# (mostly) object code storage (intermediate form)
		self.objstore = None			# object code store (output form)

		self.objcount = 0				# number of items in object code (more or less)
		self.objsize  = 0				# size of object code (in "bytes")

		self.hexrecchar = None			# lead character of a hex record (if any)
		self.hexchunksize = 16			# number of data "bytes" per line in a hex output file
		self.hexstartaddr = None		# execution start address (if any)

		self.hexreccnt = None			# number of data records output
		self.bytesout = None			# number of 8-bit values output

		self.hexaddrtype = None
		self.hexextaddr = None			# Intel extended base address (most significant 16 bits)

		self.nodata = None				# for listing lines with no address and no data
		self.noaddr = None				# for listing lines with no address but do have data

		self.outputoverride = {}		# override default output

_CG = CGvariables()

# -----------------------------
# isolating pass-throughs
# -----------------------------

def init(handler):
	'''initialize the cpu(s) handled'''
	# - only need to change this handler to change CPU(s)
	# - otherwise we'd have to import this into every module that uses it
	# - dynamically loaded; handler name has the form 'cpu_hxa---.py'
	# - user only puts 'hxa---' on command-line
	# - this form mostly for consistency and ease of telling source files apart
	handler = f'cpu_{handler}'
	try:
		_CG.cpu = import_module( handler )
	except ImportError:
		UM.fatal( "NoFile", f'{handler}.py' )

	# initialize reserved symbols
	SYM.addreserve( _CG.cpu.reserved() )

def name():
	''' get generic or family instruction set name'''
	return _CG.cpu.name()

def isop(this):
	'''is this a cpu mnemonic ?'''
	return _CG.cpu.isop( this )

def doop(mnemonic, exprlist):
	'''process a mnemonic and any expression(s)'''
	# watch for empty list
	if exprlist[0] is None:
		return _CG.cpu.doop( mnemonic, 0, [] )
	else:
		return _CG.cpu.doop( mnemonic, len(exprlist), exprlist )

# -----------------------------

def cpu():
	''' get specific cpu name '''
	return _CG.cpuname if _CG.cpuname is not None else ""

def maxbits():
	''' maximum data item size '''
	return 32

def lsbfirst():
	'''big- or little-endian cpu?'''
	return _CG.lsbfirst

def objectdesc():
	'''coarse object description'''
	return _CG.objcount, _CG.objsize

# -----------------------------

def _badcpu(cause):
	''' cpu initialization error '''
	UM.warn( "BadCPU", cause )

# -----------------------------
# "byte" extraction "operators"
# -----------------------------

def getlsb(val):
	''' return least significant "byte" of "word" '''
	if _CG.octets == 1:			# 8 bit "byte"
		return val & 0x00FF

	elif _CG.octets == 2:		# 16-bit "byte"
		return val & 0xFFFF

	else:						# 32-bit "byte"
		return val

def getmsb(val):
	''' return most significant "byte" of "word" '''
	if _CG.octets == 1:			# 8 bit "byte"
		return (val >> 8) & 0X00FF

	elif _CG.octets == 2:		# 16-bit "byte"
		return (val >> 16) & 0XFFFF

	else:						# 32-bit "byte"
		return 0

def getmsw(val):
	''' return most significant "word" of "long" '''
	if _CG.octets == 1:			# 8-bit "byte"
		return (val >> 16) & 0XFFFF
	else:						# 16- and 32-bit "byte"
		return 0

# -----------------------------

def _setcpu(name):
	''' initialize cpu-independent data '''

	def _maketype(bytes, alias):
		''' make native and reversed psops of -BIT-- data types '''
		# for eight bit "bytes":							alias:

		# group 1	bit08,  ubit08,  sbit08,  rbit08		"byte"
		# group 2	bit08r, ubit08r, sbit08r, rbit08r		"revbyte" (same as "byte")
		# group 3	bit16,  ubit16,  sbit16,  rbit16		"word"
		# group 4	bit16r, ubit16r, sbit16r, rbit16r		"revword"
		# group 5	bit24,  ubit24,  sbit24,  rbit24
		# group 6	bit24r, ubit24r, sbit24r, rbit24r
		# group 7	bit32,  ubit32,  sbit32,  rbit32		"long"
		# group 8	bit32r, ubit32r, sbit32r, rbit32r		"revlong"

		# for 16 bit "bytes":

		# group 1	bit16,  ubit16,  sbit16,  rbit16		"byte"
		# group 2	bit16r, ubit16r, sbit16r, rbit16r		"revbyte"
		# group 3	bit32,  ubit32,  sbit32,  rbit32		"word"
		# group 4	bit32r, ubit32r, sbit32r, rbit32r		"revword"

		# for 32 bit "bytes":

		# group 1	bit32,  ubit32,  sbit32,  rbit32		"byte"
		# group 2	bit32r, ubit32r, sbit32r, rbit32r		"revbyte"

		# how many bits in a "byte" ?

		totalbits = _CG.octets * bytes * 8

		# we don't tangle with more than four octets (yet, anyway)

		if totalbits <= 32:

			# add base, unsigned, signed and relative forms to psops
			# - doing it this way prevents having to check for illegal forms later

			for prefix in [ '', 'u', 's', 'r' ]:
				bitop, bitopr = f'{prefix}bit{totalbits:02d}', f'{prefix}bit{totalbits:02d}r'
				_CG.datasize[ bitop ] = _CG.datasize[ bitopr ] = bytes
				PSOP.addbitop( bitop )
				PSOP.addbitop( bitopr )
				if alias is not None:
					PSOP.addalias( bitop, f'{prefix}{alias}' )
					PSOP.addalias( bitopr, f'{prefix}rev{alias}' )

	# check descriptor
	descrip = _CG.cpu.getdescriptor( name )
	m = re.fullmatch( 'T_[0-9][0-9]_[LM](08|16|32)?', descrip )
	if m is None:
		_badcpu( this )
		return False

	# how many bits in program counter ?
	bits = int( descrip[2:4] )
	if not PC.setwidth( bits ):
		_badcpu( descrip )
		return False

	_CG.pcbits = bits

	# LSB or MSB processor ?
	_CG.lsbfirst = descrip[5] == 'L'

	# how many octets in a "byte" ?
	_CG.octets = 4 if descrip.endswith('32') else 2 if descrip.endswith('16') else 1

	# create the '-bit--' data storage psops that will be available
	_maketype( 1, 'byte' )
	_maketype( 2, 'word' )
	_maketype( 3, None )
	_maketype( 4, 'long' )

	# all okay so far
	return True

# -----------------------------
# psop: CPU name
# -----------------------------

def docpu(label, expr):
	''' handle CPU psop '''
	name = expr.upper()

	# a known cpu ?
	if not _CG.cpu.iscpu( name ):
		_badcpu( name )

	# cpu already set ?
	elif _CG.cpuname is not None:
		UTIL.sameval( name, cpu() )

	# try to initialize cpu
	# - cpu-independent parts get set first so if cpu-dependent
	# parts want to make changes (eg., byte extraction order)
	# they can be better error-checked
	elif _setcpu(name) and _CG.cpu.setcpu(name):
		_CG.cpuname = name

# -----------------------------

def _bitwidth(ftype):
	'''convert filetype to bit width'''
	bits = { 'flat': 16, 'segmented': 20, 'linear': 32, 's19': 16, 's28': 24,  's37': 32 }
	if ftype in bits:
		return bits[ ftype ]
	else:
		UM.noway( ftype )

# -----------------------------
# psop: ASSUME flag[:=]val
# -----------------------------

def doassume(flag, arg):

	def _setoverride(flag, val):
		''' set an "override default output" flag '''
		if not flag in _CG.outputoverride:
			_CG.outputoverride[ flag ] = val
			return True
		else:
			UTIL.sameval( val, _CG.outputoverride[flag] )
			return False

	def _resetpcwidth(flag, arg):
		''' reset program counter width '''
		if _setoverride(flag, arg):
			PC.setwidth( _bitwidth(arg) )

	match flag:
		# Intel hex ?
		case 'hexfile':
			if arg in ['flat', 'segmented', 'linear']:
				_resetpcwidth( flag, arg )
			else:
				return False

		# Motorola hex ?
		case 'srecfile':
			if arg in [ 's19', 's28', 's37']:
				_resetpcwidth( flag, arg )
			elif arg in ['noheader', 'noname', 'nocount']:
				_setoverride( arg, True )
			else:
				return False

		# data bytes per output line ?
		case 'hexdatasize':
			ok, val = EXP.getinrange( arg, 8, 32 )
			if ok and _setoverride(flag, val):
				_CG.hexchunksize = val

		case _:
			# 'BIT--' or BIT--R' pseudo opcode ?
			if re.fullmatch('bit(08|16|24|32)r?', flag):
	
				# is there a matching CPU-specific data type ?
				if not (flag in _CG.datasize):
					UM.ignored( flag )

				# correct number of correct octet specifiers ?
				# - convert to set to make sure there are no duplicates
				elif ( re.fullmatch('[0-3]{1,4}', arg) is None 
					or len(set(arg)) != len(arg)
					or _CG.datasize[flag] * _CG.octets != len(arg)
				):
					UM.ignored( arg )

				# this family not already converted ?
				elif _setoverride(flag, arg):
					# set custom sequence for remaining members of family
					for prefix in [ 'r', 's', 'u' ]:
						_ = _setoverride( f'{prefix}{flag}', arg )

			# try CPU-specific assumption(s)
			else:
				return _CG.cpu.doassume( flag, arg )

	# was handled here (successful or not)
	return True

# -----------------------------
# first pass data storage
# -----------------------------

# store types:

# - 'datapsop', 32-bit value (all types)	object code and data
# - 'string', byte array
# - 'assert', 32-bit value				True if non-zero
# - 'ds', 32-bit value					size of 'DS' psop
# - 'bytes', byte array					result of 'FILL'
# - 'lblequ', 32-bit value				address value of label on a line by itself
# - 'numequ', 32-bit value				numeric result of 'EQU' psop
# - 'org', 32-bit origin				program counter start address
# - 'padding', None						'PADTO' or 'PADFROM' delay flag
# - 'start', 32-bit start address		code execution start address (if any)
# - 'strequ', byte array				string result of 'EQU' psop

# things we can put in '_CG.datastore' that are not associated with actual object code
# - numeric values can have an "address" actual object code cannot,
# namely one more than the maximum program counter value
# - technically we just need storage for a 32-bit numeric value, a byte array value,
# and any types that need special handling (so not as many as we have)

_nonObjData = [ 'assert', 'ds', 'numequ', 'numlbl', 'org', 'start', 'strequ', 'strlbl' ]

def store(type, data):
	''' save data in intermediate form '''
	# get source line and initialize if we haven't seen it before
	# - data storage is a dictionary of dictionaries of lists
	# - the form is { sourceline: {offset: [data [[,data]..]} {offset: [data [[,data]..]} ... }
	# - the idea being to later quickly determine if a given [sourceline][offset] generated any data
	# - one programmer source line can generate multiple [offsets] via macro / block expansions
	# - the cpu handler can generate multiple [data] entries for any given opcode
	srcline = SRC.getmaster()
	if srcline not in _CG.datastore:
		_CG.datastore[ srcline ] = {}

	# get offset and initialize if we haven't seen it before
	offset = SRC.getoffset()
	if offset not in _CG.datastore[srcline]:
		_CG.datastore[ srcline ][ offset ] = []

	# source line generated object code ?
	# - 'read()' fails if 'org' psop not previously used
	if type in _CG.datasize:
		addr = PC.read()
		PC.add( _CG.datasize[type] )

	elif type == 'string':
		addr = PC.read()
		# translate and encode
		data = STR.storable( data, True )
		# make sure last "byte" is filled
		partial = len(data) % _CG.octets
		if partial != 0:
			data += bytes( [0] * (_CG.octets - partial) )
		PC.add( len(data)//_CG.octets )

	elif type == 'bytes':
		addr = PC.read()
		# make sure last "byte" is filled
		partial = len(data) % _CG.octets
		if partial != 0:
			data += bytes( [0] * (_CG.octets - partial) )
		PC.add( len(data)//_CG.octets )

	# no associated object code ?
	elif type in _nonObjData:
		addr = None
		if type in ['ds', 'start']:
			# - 'fetch()' may return 'None' if 'org' psop never used
			addr = PC.fetch()
		elif type == 'strequ':
			# encoding but no translation, or flag null string
			data = STR.storable(data, False) if len(data) > 0 else None

	else:
		UM.noway( type )

	# store it
	_CG.datastore[ srcline ][ offset ].append( (addr, type, data) )

	# update stored object count
	_CG.objcount += 1

# -----------------------------
# psop: ASSERT expr
# -----------------------------

def _checkassert(val):
	''' check assertion '''
	if not val:
		UM.error( 'BadAssert' )

def doassert(label, val):
	''' handle ASSERT psop '''
	# saving is only necessary if not resolved during first pass,
	# but listing looks better if we always save
	store( 'assert', val )

	if EXP.resolved(val):				# resolved on first pass ?
		_checkassert( val )				# check it now

# -----------------------------
# psop: [label] STRING expr [[, expr]...]
# -----------------------------

def dostring(label, str):
	''' handle STRING psop '''
	if len(str) > 0:
		store( 'string', str )
	else:
		UM.warn( 'NoEffect' )

# -----------------------------
# psop: [label] STRINGR expr [[, expr]...]
# -----------------------------

def dostringr(label, str):
	'''handle STRINGR psop '''
	dostring( label, str[::-1] )

# -----------------------------

def fill(count, fillbytes=None):
	'''add octets to object storage'''
	if count > 0:
		if fillbytes is None:
			fillbytes = bytearray( '\x00'.encode('utf-8') )
		# adjust for "byte" size
		count *= _CG.octets
		while len(fillbytes) <= count//2:
			fillbytes.extend( fillbytes )
		if len(fillbytes) < count:
			fillbytes.extend( fillbytes[:count-len(fillbytes)] )
		store( 'bytes', fillbytes )

# -----------------------------
# psop: [label] HEX hex$
# -----------------------------

def dohex(label, bytes):
	'''handle HEX psop'''
	store( 'bytes', bytes )

# -----------------------------
# pass two
# -----------------------------

def _isrel(type):
	'''is this a relative data type?'''
	return type.startswith( 'r' )

def _abs2rel(addr, type, val):
	'''convert absolute address to relative offset'''
	# adjust based on address following this data
	return val - ( addr + _CG.datasize[type] )

def _rel2abs(addr, type, val):
	'''convert relative offset to absolute address'''
	return val + ( addr + _CG.datasize[type] )

def resolve():
	''' resolve and range-check data values '''

	# a blank string for listing lines which have no address or data
	_CG.nodata = ' ' * ( 17 if _CG.pcbits <= 16 else 20 if _CG.pcbits <= 24 else 22 )

	# a blank string for listing lines which have no address but do have data
	_CG.noaddr =' ' * ( 4 if _CG.pcbits <= 16 else 7 if _CG.pcbits <= 24 else 9 )

	# create range check values
	minval = {}
	maxval = {}

	for type in _CG.datasize:

		bits = 32 if '32' in type else 24 if '24' in type else 16 if '16' in type else 8

		if type.startswith(('r', 's')):
			minval[ type ] = -2**(bits-1)
			maxval[ type ] = 2**(bits-1) - 1

		elif type.startswith('u'):
			minval[ type ] = 0
			maxval[ type ] = 2**bits - 1

		# all unrestricted 'bit--' ops
		# - these silently truncate any oversize value
		# - we check now so we don't trigger a range error in Python's to_bytes() function
		else:
			minval[ type ] = -2**32		# -4294967296, -$1 0000 0000
			maxval[ type ] = 2**32 - 1	#  4294967295,   $ FFFF FFFF

	# we have to leave this at its current value
	masterline = SRC.getmaster()

	# resolve addresses and data
	for srcline in _CG.datastore:

		SRC.setmaster( srcline )			# for error-reporting

		for offset in _CG.datastore[srcline]:

			SRC.setoffset( offset )			# for error reporting

			resolved = []					# we're going to replace what's stored here

			for pc, type, data in _CG.datastore[srcline][offset]:

				# resolve address
				addr = PC.getabs( pc )
				# resolve data
				val = EXP.resolve( data )

				if val is not None:			# data valid ?

					# non-data generating ?
					if type in _nonObjData:
						if type == 'numlbl':
							val = PC.getabs( val )
						elif type == 'strlbl':
							val = STR.storable( str(PC.getabs(val)) )

						# if 'assert' was resolved on first pass,
						# checking it again won't hurt anything
						elif type == 'assert':
							_checkassert( val )

						# the value of 'start' won't actually be used unless
						# an ouput hex file that supports it is specified
						# - but we want to check for errors anyway
						elif type == 'start':
							if PC.valid(val):
								_CG.hexstartaddr = val
							else:
								UM.ignored( val )
								continue

					# a data-generating type ?
					elif type in _CG.datasize:

						# adjust any relative value
						if _isrel(type):
							# valid address to base offset on ?
							if PC.valid(val):
								val = _abs2rel( addr, type, val )
							else:
								continue

						# range check value
						if not UTIL.inrange( val, minval[type], maxval[type] ):
							continue

						_CG.objsize += _CG.datasize[ type ]

					# just update object size
					elif type in ['string', 'bytes']:
						_CG.objsize += len(val) // _CG.octets

					# oops!
					else:
						UM.noway( type )

				# finished with this piece of data
				resolved.append( (PC.getseg(pc), addr, type, val) )

			# replace
			_CG.datastore[ srcline ][ offset ] = resolved

	# restore
	SRC.setmaster( masterline )

# -----------------------------
# listing support
# -----------------------------

def hasdata(srcline, offset):
	'''do we have any stored data for this combination ?'''
	return srcline in _CG.datastore and offset in _CG.datastore[ srcline ] and len(_CG.datastore[srcline][offset]) > 0

def leadingblanks():
	'''a string of spaces the width of the address and data fields on listing'''
	return _CG.nodata

def fmtaddr(this):
	''' format absolute address value (MSB first) '''
	if this is None:
		return _CG.noaddr
	elif _CG.pcbits <= 16:
		return f'{this:04X}'
	elif _CG.pcbits <= 24:
		return f'{(this>>16) & 0xFF:02X}:{this & 0xFFFF:04X}'
	else:
		return f'{(this>>16) & 0xFFFF:04X}:{this & 0xFFFF:04X}'

def objectcode(srcline, offset):
	''' format any object code associated with a source/offset combination '''
	# format of first line:
	# addr  b0 b1 b2 b3				(max width=9+1+4*3=22, followed by text of source line)
	# format of any subsequent lines:
	# addr  b0 b1 b2 b3 ... b15		(max width=9+1+16*3=58, no source line text, so can use whole line)
			
	def _num2bytestr(type, num):
		''' convert 32-bit number to listing representation '''
		# get bytes, least significant first
		# - must specify signed in order to handle negative values
		# - but that makes $FFFFFFFF too big for four bytes...
		bytes = num.to_bytes( 5, byteorder='little', signed=True )

		# custom sequence ?

		if type in _CG.outputoverride:

			seq = _CG.outputoverride[ type ]
			ndx = [ int(ch) for ch in seq ]

			if '08' in type:
				return f' {bytes[ndx[0]]:02X}         '
			elif '16' in type:
				return f' {bytes[ndx[0]]:02X} {bytes[ndx[1]]:02X}      '
			elif '24' in type:
				return f' {bytes[ndx[0]]:02X} {bytes[ndx[1]]:02X} {bytes[ndx[2]]:02X}   '
			else:
				return f' {bytes[ndx[0]]:02X} {bytes[ndx[1]]:02X} {bytes[ndx[2]]:02X} {bytes[ndx[3]]:02X}'
			
		# default sequence

		rev = type.endswith( 'r' )
		
		# native LSB or reversed MSB

		# bits#      00-07  08-15  16-23  24-31
		# byte#        0      1      2      3
		
		if (_CG.lsbfirst and not rev) or (not _CG.lsbfirst and rev):

			if '08' in type:
				return f' {bytes[0]:02X}         '
			elif '16' in type:
				return f' {bytes[0]:02X} {bytes[1]:02X}      '
			elif '24' in type:
				return f' {bytes[0]:02X} {bytes[1]:02X} {bytes[2]:02X}   '
			else:
				return f' {bytes[0]:02X} {bytes[1]:02X} {bytes[2]:02X} {bytes[3]:02X}'
				
		# native MSB or reversed LSB

		# bits#     31-24  23-16  15-08  07-00
		# byte  #     3      2      1      0

		else:

			if '08' in type:
				return f' {bytes[0]:02X}         '
			elif '16' in type:
				return f' {bytes[1]:02X} {bytes[0]:02X}      '
			elif '24' in type:
				return f' {bytes[2]:02X} {bytes[1]:02X} {bytes[0]:02X}   '
			else:
				return f' {bytes[3]:02X} {bytes[2]:02X} {bytes[1]:02X} {bytes[0]:02X}'

	def _str2bytestr(ndx, bytes):
		''' convert all or part of string to listing representation '''
		# first call ?
		if ndx == 0:
			if len(bytes) == 1:
				return ( 1, f' {bytes[0]:02X}         ' )
			elif len(bytes) == 2:
				return ( 2, f' {bytes[0]:02X} {bytes[1]:02X}      ' )
			elif len(bytes) == 3:
				return ( 3, f' {bytes[0]:02X} {bytes[1]:02X} {bytes[2]:02X}   ' )
			else:
				return ( 4, f' {bytes[0]:02X} {bytes[1]:02X} {bytes[2]:02X} {bytes[3]:02X}' )
		# no, use more of the (presumed) width of the page for listing
		else:
			maxout = min(16, len(bytes) - ndx)
			retstr = ''.join( [f' {c:02X}' for c in bytes[ndx:ndx+maxout]] )
			# add spaces to increase readablility
			retstr = ' '.join( [retstr[i:i+12] for i in range(0, len(retstr), 12)] )
			return ( maxout, retstr )

	# main...

	objlst = []

	for seg, addr, type, data in _CG.datastore[srcline][offset]:

		# generated nothing ?
		if data is None:
			# just the address and a blank data field (1 + 12 + 1 spaces)
			objlst.append( f'{fmtaddr(addr)}             ' )

		# generated fixed size data ?
		elif type in _CG.datasize:
			objlst.append( f'{fmtaddr(addr)} {_num2bytestr(type, data)}' )
			if _isrel(type):
				objlst.append( f'  [ ={fmtaddr(_rel2abs(addr, type, data))} ]' )

		# generated variable size data ?
		elif type in ['string', 'strequ', 'strlbl', 'bytes']:
			ndx = 0
			while ndx < len(data):
				cnt, lst = _str2bytestr( ndx, data )
				objlst.append( f'{fmtaddr(addr)} {lst}' )
				if type not in ['strequ', 'strlbl']:
					addr += cnt//_CG.octets
				ndx += cnt

		# non-object data
		elif type in _nonObjData:
			# ...mostly because we already have a lot of tests that depend on this...
			# - it's the easiest solution and list-wise looks pretty good (which is why so many tests...)...
			if type == 'org':
				addr = data
			objlst.append( f'{fmtaddr(addr) } {_num2bytestr("bit32", data)}' )

		# oops !
		else:
			UM.noway( type )

	return objlst

# -----------------------------
# object file support
# -----------------------------

def _datacode(type, value):
	''' convert a data value to a byte array '''
	if value is None:
		return None

	def _num2bytes():
		''' convert a numeric value to byte array '''
		# custom sequence ?
		if type in _CG.outputoverride:
			# get bytes, least significant first
			# - must specify signed in order to handle negative values
			# - but that makes $FFFFFFFF too big for four bytes...
			bytes = value.to_bytes( 5, byteorder='little', signed=True )

			seq = _CG.outputoverride[ type ]
			ndx = [ int(ch) for ch in seq ]

			if '08' in type:
				return [ bytes[ndx[0]] ]
			elif '16' in type:
				return [ bytes[ndx[0]], bytes[ndx[1]] ]
			elif '24' in type:
				return [ bytes[ndx[0]], bytes[ndx[1]], bytes[ndx[2]] ]
			else:
				return [ bytes[ndx[0]], bytes[ndx[1]], bytes[ndx[2]], bytes[ndx[3]] ]

		# default sequence

		rev = type.endswith( 'r' )

		# native LSB or reversed MSB:

		# bits#      00-07  08-15  16-23  24-31
		# byte#        0      1      2      3
		if (_CG.lsbfirst and not rev) or (not _CG.lsbfirst and rev):
			bytes = value.to_bytes( 5, byteorder='little', signed=True )

			if '08' in type:
				return bytes[:1]
			elif '16' in type:
				return bytes[:2]
			elif '24' in type:
				return bytes[:3]
			else:
				return bytes[:4]

		# native MSB or reversed LSB:
		# bits#     31-24  23-16  15-08  07-00
		# byte#       3      2      1      0

		else:
			bytes = value.to_bytes( 5, byteorder='big', signed=True )

			if '08' in type:
				return bytes[4:]
			elif '16' in type:
				return bytes[3:]
			elif '24' in type:
				return bytes[2:]
			else:
				return bytes[1:]

	return _num2bytes() if type not in ['string', 'bytes'] else bytes(value)

def motorola_types():
	''' get Motorola record type and lead char '''
	# outside 'putobject()' because 'hxa_file.py' needs access
	if ( 'srecfile' in _CG.outputoverride ):
		pcwidth = _bitwidth( _CG.outputoverride['srecfile'] )
	else:
		pcwidth = PC.getwidth()

	rectype = 3 if pcwidth > 24 else 2 if pcwidth > 16 else 1
	rechar = 'U' if _CG.octets == 4 else 'T' if _CG.octets == 2 else 'S'
	return( rectype, rechar )

def _putobject(outtype):
	''' output all files associated with one file type '''

	def _closeblock(segndx, segnum):
		'''close "--BYBLK" output ?'''
		closeblock = ( segnum == _CG.datasegs[-1] )
		if not closeblock:
			thisname = PC.getsegname( segnum )
			nextname = PC.getsegname( _CG.datasegs[segndx+1] )
			closeblock = ( PC.getsegend(thisname) != PC.getsegbeg(nextname) )

		return closeblock

# ------- binary object

	def _putbinall(ftype, fouts):
		'''write a single binary file containing all segments'''
		if OS.openoutpfile(ftype, 1):
			for segobj in _CG.objstore:
				OS.asmoutwrite( segobj )
			OS.closeout()

	def _putbinbyseg(ftype, fouts):
		'''write a binary file for each segment'''
		for i, segnum in enumerate(_CG.datasegs):
			if OS.openoutpfile(ftype, segnum):
				OS.asmoutwrite( _CG.objstore[i] )
				OS.closeout()

	def _putbinbyblk(ftype, fouts):
		'''write a binary file for each block of consecutive segments'''
		newblock = True
		for i, segnum in enumerate(_CG.datasegs):
			# start new block of segments ?
			if newblock:
				# failure to open will just re-try for next segment
				if OS.openoutpfile(ftype, segnum):
					newblock = False
				else:
					continue

			# write current segment
			OS.asmoutwrite( _CG.objstore[i] )

			# close this block ?
			if _closeblock(i, segnum):
				OS.closeout()
				newblock = True

# -------

	def _puthex(prefix, rec):
		''' write one hex record to file '''
		# convert byte array to list of hex char pairs
		hexlst = [ f'{b:02X}' for b in rec ]
		OS.writeout( f'{prefix}{"".join(hexlst)}' )

# ------- raw hex object

	def _write_raw_data(addr, data):
		''' write one raw (undecorated) record '''
		_puthex( '', data )

# -------

	def _int2msb(count, value):
		''' convert integer to unsigned MSB-first byte string '''
		return value.to_bytes( count, byteorder='big', signed=False )

# ------- Intel hex object

	def _init_intel():
		''' initialize for writing Intel hex file '''
		if "hexfile" in _CG.outputoverride:
			_CG.hexaddrtype = { 'linear': 4, 'segmented': 2, 'flat': 0 }[ _CG.outputoverride["hexfile"] ]
		else:
			_CG.hexaddrtype = 4 if PC.getwidth() > 20 else 2 if PC.getwidth() > 16 else 0

#		_CG.hexrecchar = '<' if _CG.octets == 4 else ';' if _CG.octets == 2 else ':'
		_CG.hexrecchar = { 4: '<', 2: ';', 1: ':' }[ _CG.octets ]
		_CG.hexextaddr = 0
		_CG.bytesout = None

	def _write_intel_bof():
		'''write Intel "header record"'''
		# no such thing, really, but we can "jump start" extended address output
		_CG.bytesout = _CG.hexextaddr = 0x10000

# output one line in Intel hexadecimal object format (rev A, 01/06/1988)
# format: |recmark|reclen|loadoffset|rectyp|data|checksum|
# recmark	= 03AH (Ascii ':') (standard; 8-bit bytes)
#				= 03BH (Ascii ';') (extended; 16-bit bytes)
#				= 03CH (Ascii '<') (extended; 32-bit bytes)
# reclen	= length of data field in bytes
# loadoffset = load offset of data bytes (= zero if not data record)
# rectyp	= record type
#  0			= data (16-, 20- and 32-bit)
#  1			= end of file (16-, 20- and 32-bit)
#  2			= extended segment address (20- and 32-bit)
#  3			= start segment address (20- and 32-bit)
#  4			= extended linear address (32-bit)
#  5			= start linear address (32-bit)
# data		= data bytes of absolute memory image
# checksum	= -(reclen+loadoffset+rectype+data)&0FFH (so total sum = 0)

	def _write_intel_record(type, offset, data=None):
		''' write one Intel hex record '''
		# we'll build up the record in this
		rec = bytearray()

		def addrec(count, value):
			''' add value to record '''
			bytes = _int2msb( count, value )
			rec.extend( bytes )

		# all types but EOF contain data
		reclen = len(data) if type != 1 else 0
		addrec( 1, reclen )
		# only data records have a 16-bit load offset
		addrec( 2, offset if type == 0 else 0 )
		# all records have a type
		addrec( 1, type )
		# now the data
		if data is not None:
			rec.extend( data )
		# two's complement checksum
		chksum = 0
		for byte in rec:
			chksum += byte
		addrec( 1, -chksum & 0xFF )
		# write
		_puthex( _CG.hexrecchar, rec )

	def _write_intel_data(addr, data):
		''' write an Intel data record '''
		# we rely on earlier pass two to guarantee addresses
		# do not go out of range (if so, assembly already halted)
		if _CG.hexaddrtype == 0:
			_write_intel_record( 0, addr, data )

		# but extended addresses can cross a 64K boundary
		# - because the offset value of an address is 16 bits, we can only
		# write up to 64K before we *must* insert an extended address record
		# - apparently "64K" means 2^16 of the smallest addressable unit,
		# since that much of an offset from a base address is allowed
		# - in any case we only output about 32K "bytes" before inserting
		# a new extended address record
		# - we also test for "address jumps" up or down great enough
		# to require a new extended base address
		else:
			offset = addr - _CG.hexextaddr
			databytes = len( data ) / _CG.octets
			# do we need to output an extended address record ?
			if ( offset >= 0
				and offset + databytes <= 0x10000
				and _CG.bytesout is not None
				and _CG.bytesout + databytes <= 0x08000
			):	#no
				_CG.bytesout += databytes
			else: # yes
				_CG.bytesout = databytes
				# 20-bit ?
				if _CG.hexaddrtype == 2:
					_CG.hexextaddr = addr & 0xFFFF0
					places = 4
				# 32-bit ?
				else:
					_CG.hexextaddr = addr & 0xFFFF0000
					places = 16

				# write extended address record (most significant 16 bits of addr)
				_write_intel_record( _CG.hexaddrtype, 0, _int2msb(2, _CG.hexextaddr >> places) )
				# new offset
				offset = addr - _CG.hexextaddr

			# we know each data record contains at most 32 "bytes"
			# - so we know we only need to write one record and that it will fit within 64K offset
			_write_intel_record( 0, offset, data )

	def _write_intel_eof(segnum):
		''' write Intel start address and end of file records '''
		# last data seg and start address specified and extended or linear addressing ?
		if ( segnum == _CG.datasegs[-1]
			and _CG.hexstartaddr is not None
			and _CG.hexaddrtype != 0
			):

			# 20-bit segmented start address must be in CS:IP (16:16) format
			# - we use "huge" format, with the most significant 16 bits
			# in CS and only the least significant 4 bits in IP
			addr = _CG.hexstartaddr
			if _CG.hexaddrtype == 2:
				addr = (addr & 0xFFFF0) << 12 | (addr & 0x0000F)

			# write start address record (32-bit addresses unaltered)
			_write_intel_record( _CG.hexaddrtype+1, 0, _int2msb(4, addr) )

		# write EOF record
		_write_intel_record( 1, 0 )

# ------- Motorola hex object

	def _init_moto():
		''' initialize for writing Motorola hex file '''
		_CG.hexaddrtype, _CG.hexrecchar = motorola_types()

# output one line in Motorola hexadecimal object format
# format: |rectype|count|absaddr|data|checksum|
# rectyp	= record type
#  'S0'			= absaddr is arbitrary data (eg., filename, comment or 'HDR')
#  'S1'			= absaddr is 16-bit start load address
#  'S2'			= absaddr is 24-bit start load address
#  'S3'			= absaddr is 32-bit start load address
#  'S5'			= absaddr is 16-bit count of previous records of types S1-S3
#  'S6'			= absaddr is 24-bit count of previous records of types S1-S3
#  'S7'			= absaddr is 32-bit start execution address
#  'S8'			= absaddr is 24-bit start execution address
#  'S9'			= absaddr is 16-bit start execution address
# count		= #absaddr bytes + #data bytes + 1 (checksum byte)
# absaddr	= absolute address or record count
# data		= data bytes of absolute memory image (0-64 pairs)
# checksum	= one's complement of count+absaddr+data

# file format is: S0-S[123]-S[56]-S[987]
# - only S[123] records can appear more than once in an output file

	def _write_moto_record(type, addr, data=None):
		''' write Motorola hex record '''
		# size of address field
		count = [ 2, 2, 3, 4, 0, 2, 3, 4, 3, 2 ][ type ]

		# we'll build up the record in this
		rec = bytearray()

		def addrec(count, value):
			''' add value to record '''
			bytes = _int2msb( count, value )
			rec.extend( bytes )

		# start with address
		addrec( count, addr )

		# header record ?
		if type == 0:
			if not "noname" in _CG.outputoverride:
				rec.extend( data )
			# null terminate
			rec.append( 0 )

		# a data record ?
		elif type in [1,2,3]:
			_CG.hexreccnt += 1
			rec.extend( data )

		# one's complement checksum
		sum = len( rec ) + 1
		for byte in rec:
			sum += byte
		addrec( 1, 0xFF - (sum & 0xFF) )

		# make prefix for data
		prfx = f'{_CG.hexrecchar}{type:1d}{len(rec):02X}'
		_puthex( prfx, rec ) 

	def _write_moto_bof():
		''' write Motorola beginning of file record '''
		_CG.hexreccnt = 0
		if not "noheader" in _CG.outputoverride:
			# make sure name fits in one record
			hdrname = OS.rootfn()[:_CG.hexchunksize-1]
			_write_moto_record( 0, 0, STR.storable(hdrname) )

	def _write_moto_data(addr, data):
		''' write Motorola data record '''
		_write_moto_record( _CG.hexaddrtype, addr, data )

	def _write_moto_eof(segnum):
		''' write Motorola end of file record(s) '''
		# record count
		if "nocount" not in _CG.outputoverride:
			_write_moto_record( 5 if _CG.hexreccnt < 0x10000 else 6, _CG.hexreccnt )
		# start address (only for last segment written)
		addr = _CG.hexstartaddr if segnum == _CG.datasegs[-1] and _CG.hexstartaddr is not None else 0
		_write_moto_record( 10 - _CG.hexaddrtype, addr )

# -------

	def _puthexseg(objndx, segnum, writedata):
		''' write a single hex segment '''
		# addresses within a segment are continuous
		# - so if we know the first we can calculate the rest
		absaddr = PC.getsegorg( segnum )

		# set data octet count of an output line
		# - multiplication prevents a "byte" from being split across two lines
		# - max data octets = 32 * 4 = 128, max data chars = 32 * 4 * 2 = 256
		octets = _CG.hexchunksize * _CG.octets

		# write individual records from this segment (one line per record)
		for i in range(0, len(_CG.objstore[objndx]), octets):
			writedata( absaddr, _CG.objstore[objndx][i:i+octets] )
			absaddr += _CG.hexchunksize

	def _null(arg=None):
		'''dummy routine for handling unused output routines'''
		pass

	_outroutines = {
				# init(), bof(), write(), eof()
		'raw':	( _null, _null, _write_raw_data, _null ),
		'hex':	( _init_intel, _write_intel_bof, _write_intel_data, _write_intel_eof ),
		'srec':	( _init_moto, _write_moto_bof, _write_moto_data, _write_moto_eof ),
	}

	def _putall(ftype, fouts):
		''' write all data segments to a single text file'''
		init, bof, write, eof = _outroutines[ fouts ]

		init()
		if OS.openoutpfile(ftype, _CG.datasegs[0]):
			bof()
			for objndx, segnum in enumerate(_CG.datasegs):
				_puthexseg( objndx, segnum, write )
			eof( segnum )
			OS.closeout()

	def _putbyseg(ftype, fouts):
		'''write each data segment to a seperate text file'''
		init, bof, write, eof = _outroutines[ fouts ]

		init()
		for objndx, segnum in enumerate(_CG.datasegs):
			if OS.openoutpfile(ftype, segnum):
				bof()
				_puthexseg( objndx, segnum, write )
				eof( segnum )
				OS.closeout()

	def _putbyblk(ftype, fouts):
		'''write each block of consecutive data segments to a seperate text file'''
		init, bof, write, eof = _outroutines[ fouts ]

		init()
		newblock = True
		for i, segnum in enumerate(_CG.datasegs):
			# start new block of segments ?
			if newblock:
				# failure to open will just re-try for next segment
				if OS.openoutpfile(ftype, segnum):
					bof()
					newblock = False
				else:
					continue

			# write current segment
			_puthexseg( i, segnum, write )

			# close this block ?
			if _closeblock(i, segnum):
				eof( segnum )
				OS.closeout()
				newblock = True

# ------- main

	_asmout = {
		# single file output - only choice for monolithic
		'objfile': _putbinall,		# binary
		'rawfile': _putall,			# undecorated hex
		'hexfile': _putall,			# Intel hex
		'srecfile': _putall,		# Motorola hex

		# multiple file output - optional for segmented
		'objbyseg': _putbinbyseg,	# binary
		'rawbyseg': _putbyseg,		# undecorated hex
		'hexbyseg': _putbyseg,		# Intel hex
		'srecbyseg': _putbyseg,		# Motorola hex

		'objbyblk': _putbinbyblk,	# binary
		'rawbyblk': _putbyblk,		# undecorated hex
		'hexbyblk': _putbyblk,		# Intel hex
		'srecbyblk': _putbyblk,		# Motorola hex
	}

	# single file output (monolithic block) ?
	# "OBJFILE", "RAWFILE", "HEXFILE", "SRECFILE"
	ftype = f'{outtype}file'
	if OS.outputdefined(ftype):
		_asmout[ ftype ]( ftype, outtype )

	# multiple file output ?
	if PC.hassegs():
		# "OBJBYSEG", "RAWBYSEG", "HEXBYSEG", "SRECBYSEG"
		ftype = f'{outtype}byseg'
		if OS.outputdefined(ftype):
			_asmout[ ftype ]( ftype, outtype )
		# "OBJBYBLK", "RAWBYBLK", "HEXBYBLK", "SRECBYBLK"
		ftype = f'{outtype}byblk'
		if OS.outputdefined(ftype):
			_asmout[ ftype ]( ftype, outtype )

# -------

def _data2obj(datasegs):
	''' convert intermediate data store to binary object store '''

	def _segdata(segnum):
		''' generate all data from one segment '''
		for srcline in _CG.datastore:
			for offset in _CG.datastore[srcline]:
				for seg, addr, type, data in _CG.datastore[srcline][offset]:
					if segnum == seg and not type in _nonObjData:
						yield [ addr, type, data ]

	# convert to object form
	_CG.objstore = []
	for i in datasegs:
		segobj = bytearray()
		for addr, type, data in _segdata(i):
			segobj.extend( _datacode(type, data) )
		_CG.objstore.append( segobj )

# -------

def putobject():
	''' output finished assembly object (if any)'''
	# which segments actually contain object data ?
	_CG.datasegs = [ i for i in range(1, PC.getsegcnt()) if PC.seghasdata(i) ]

	# if there are any, output any and all file types specified
	if len(_CG.datasegs):
		_data2obj( _CG.datasegs )
		_putobject( "obj" )		# binary
		_putobject( "raw" )		# undecorated hex
		_putobject( "hex" )		# Intel hex
		_putobject( "srec" )	# Motorola hex
