# Hobby Cross-Assembler (HXA) V1.000 - Instruction Set (65xx Version)

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

# ---------------------------------

# by Anton Treuenfels

# 5248 Horizon Dr
# Fridley, MN 55421

# e-mail: atreuenfels@earthlink.net

# source language: Python 3.11.4

# first created: 01/18/03 (in Thompson AWK 4.0)
# last revision: 06/14/24

# preferred public function prefix: 'CPU'

# ----------------------------
# other HXA modules
import hxa_usermesg as UM
import hxa_codegen as CG
import hxa_expressions as EXP
# ----------------------------

# Address modes:

#								6502	65C02	R65C02  W65C02S W65C816S

# ab	- Absolute				X		X		X		X		X
# abi	- Absolute Indirect		X		X		X		X		X
# abx	- Absolute X			X		X		X		X		X
# abxi  - Absolute X Indirect			X		X		X		X
# aby	- Absolute Y			X		X		X		X		X
# acc	- Accumulator			X		X		X		X		X
# bmv	- Block Move											X
# imm	- Immediate				X		X		X		X		X
# imp	- Implied				X		X		X		X		X
# lab	- Long Absolute											X
# labi  - Long Absolute Indirect								X
# labx  - Long Absolute X										X
# lpcr  - Long PC Relative										X
# lzpi  - Long Zero Page Indirect								X
# lzpiy - Long Zero Page Indirect Y								X
# pcr	- PC Relative			X		X		X		X		X
# sr	- Stack Relative										X
# sriy  - Stack Relative Indirect Y								X
# zp	- Zero Page				X		X		X		X		X
# zpi	- Zero Page Indirect			X		X		X		X
# zpiy  - Zero Page Indirect Y	X		X		X		X		X
# zptr  - Zero Page Test Relative				X		X
# zpx	- Zero Page X			X		X		X		X		X
# zpxi  - Zero Page X Indirect	X		X		X		X		X
# zpy	- Zero Page Y			X		X		X		X		X

# Notes:
# - the above address modes do not always correspond to official WDC
# literature in either name or number, but
# - (a) they do cover everything we need, and 
# - (b) we can do anything we want if it makes our lives easier
# (and is kept completely internal to this file) !
# - ex: 'labi' is not an official mode and exists simply so that 'abi'
# can be easily forced to long with a minimum of fuss

# Expression processing by address mode:

# mode		adjustment		storage

# ab*		(none)			UBIT16
# abi		discard ()		UBIT16
# abx*		(none)			UBIT16
# abxi		discard (,x)	UBIT16
# aby*		(none)			UBIT16
# acc		(none)			(none)
# bmv		add ^			UBIT08, UBIT08
# imm		discard #		BIT08
# imp		(none)			(none)
# lab*		(none)			UBIT24
# labi		discard ()		BIT16
# labx*		(none)			UBIT24
# lpcr		(none)			RBIT16
# lzpi		discard []		UBIT08
# lzpiy		discard []		UBIT08
# pcr		(none)			RBIT08
# sr		(none)			UBIT08
# sriy		discard (,s)	UBIT08
# zp*		(none)			UBIT08
# zpi		discard ()		UBIT08
# zpiy		discard ()		UBIT08
# zptr		(none)			UBIT08, RBIT08
# zpx*		(none)			UBIT08
# zpxi		discard (,x)	UBIT08
# zpy*		(none)			UBIT08

# *= can be part of multiple possible modes:
# ab|zp|lab
# ab|lab
# ab|zp
# aby|zpy
# abx|zpx|labx
# abx|zpx

# -----------------------------

# NMOS 6502 instruction set

# Notes:
# - the ROR instruction available after June 1976
# - this is the base instruction set for all 65xx variants

_ins6502 = [
 'ADC': [ ('ab', 0x6D), ('abx', 0x7D), ('aby', 0x79), ('imm', 0x69), ('zp', 0x65), ('zpiy', 0x71), ('zpx', 0x75), ('zpxi', 0x61) ],
 'AND': [ ('ab', 0x2D), ('abx', 0x3D), ('aby', 0x39), ('imm', 0x29), ('zp', 0x25), ('zpiy', 0x31), ('zpx', 0x35), ('zpxi', 0x21) ],
 'ASL': [ ('ab', 0x0E), ('abx', 0x1E), ('acc', 0x0A), ('zp', 0x06), ('zpx', 0x16) ],
 'BCC': [ ('pcr', 0x90) ],
 'BCS': [ ('pcr', 0xB0) ],
 'BEQ': [ ('pcr', 0xF0) ],
 'BGE': [ ('pcr', 0xB0) ],
 'BIT': [ ('ab', 0x2C), ('zp', 0x24) ],
 'BLT': [ ('pcr', 0x90) ],
 'BMI': [ ('pcr', 0x30) ],
 'BNE': [ ('pcr', 0xD0) ],
 'BPL': [ ('pcr', 0x10) ],
 'BRK': [ ('imm', 0x00), ('imp', 0x00), ('zp', 0x00) ],
 'BVC': [ ('pcr', 0x50) ],
 'BVS': [ ('pcr', 0x70) ],
 'CLC': [ ('imp', 0x18) ],
 'CLD': [ ('imp', 0xD8) ],
 'CLI': [ ('imp', 0x58) ],
 'CLV': [ ('imp', 0xB8) ],
 'CMP': [ ('ab', 0xCD), ('abx', 0xDD), ('aby', 0xD9), ('imm', 0xC9), ('zp', 0xC5), ('zpiy', 0xD1), ('zpx', 0xD5), ('zpxi', 0xC1) ],
 'CPX': [ ('ab', 0xEC), ('imm', 0xE0), ('zp', 0xE4) ],
 'CPY': [ ('ab', 0xCC), ('imm', 0xC0), ('zp', 0xC4) ],
 'DEC': [ ('ab', 0xCE), ('abx', 0xDE), ('zp', 0xC6), ('zpx', 0xD6) ],
 'DEX': [ ('imp', 0xCA) ],
 'DEY': [ ('imp', 0x88) ],
 'EOR': [ ('ab', 0x4D), ('abx', 0x5D), ('aby', 0x59), ('imm', 0x49), ('zp', 0x45), ('zpiy', 0x51), ('zpx', 0x55), ('zpxi', 0x41) ],
 'INC': [ ('ab', 0xEE), ('abx', 0xFE), ('zp', 0xE6), ('zpx', 0xF6) ],
 'INX': [ ('imp', 0xE8) ],
 'INY': [ ('imp', 0xC8) ],
 'JMP': [ ('ab', 0x4C), ('abi', 0x6C) ],
 'JSR': [ ('ab', 0x20) ],
 'LDA': [ ('ab', 0xAD), ('abx', 0xBD), ('aby', 0xB9), ('imm', 0xA9), ('zp', 0xA5), ('zpiy', 0xB1), ('zpx', 0xB5), ('zpxi', 0xA1) ],
 'LDX': [ ('ab', 0xAE), ('aby', 0xBE), ('imm', 0xA2), ('zp', 0xA6), ('zpy', 0xB6) ],
 'LDY': [ ('ab', 0xAC), ('abx', 0xBC), ('imm', 0xA0), ('zp', 0xA4), ('zpx', 0xB4) ],
 'LSR': [ ('ab', 0x4E), ('abx', 0x5E), ('acc', 0x4A), ('zp', 0x46), ('zpx', 0x56) ],
 'NOP': [ ('imp', 0xEA) ],
 'ORA': [ ('ab', 0x0D), ('abx', 0x1D), ('aby', 0x19), ('imm', 0x09), ('zp', 0x05), ('zpiy', 0x11), ('zpx', 0x15), ('zpxi', 0x01) ],
 'PHA': [ ('imp', 0x48) ],
 'PHP': [ ('imp', 0x08) ],
 'PLA': [ ('imp', 0x68) ],
 'PLP': [ ('imp', 0x28) ],
 'ROL': [ ('ab', 0x2E), ('abx', 0x3E), ('acc', 0x2A), ('zp', 0x26), ('zpx', 0x36) ],
 'ROR': [ ('ab', 0x6E), ('abx', 0x7E), ('acc', 0x6A), ('zp', 0x66), ('zpx', 0x76) ],
 'RTI': [ ('imp', 0x40) ],
 'RTS': [ ('imp', 0x60) ],
 'SBC': [ ('ab', 0xED), ('abx', 0xFD), ('aby', 0xF9), ('imm', 0xE9), ('zp', 0x0E5), ('zpiy', 0xF1), ('zpx', 0xF5), ('zpxi', 0xE1) ],
 'SEC': [ ('imp', 0x38) ],
 'SED': [ ('imp', 0xF8) ],
 'SEI': [ ('imp', 0x78) ],
 'STA': [ ('ab', 0x8D), ('abx', 0x9D), ('aby', 0x99), ('zp', 0x085), ('zpiy', 0x91), ('zpx', 0x95), ('zpxi', 0x81) ],
 'STX': [ ('ab', 0x8E), ('zp', 0x86), ('zpy', 0x96) ],
 'STY': [ ('ab', 0x8C), ('zp', 0x84), ('zpx', 0x94) ],
 'TAX': [ ('imp', 0xAA) ],
 'TAY': [ ('imp', 0xA8) ],
 'TSX': [ ('imp', 0xBA) ],
 'TXA': [ ('imp', 0x8A) ],
 'TXS': [ ('imp', 0x9A) ],
 'TYA': [ ('imp', 0x98) ],
}

# CMOS 65C02 instruction set (additions to NMOS 6502 only)

_ins65C02 = {
 'ADC': [ ('zpi', 0x72) ],
 'AND': [ ('zpi', 0x32) ],
 'BIT': [ ('abx', 0x3C), ('imm', 0x89), ('zpx', 0x34) ],
 'BRA': [ ('pcr', 0x80) ],
 'CMP': [ ('zpi', 0xD2) ],
 'DEA': [ ('imp', 0x3A) ],
 'DEC': [ ('acc', 0x3A) ],
 'EOR': [ ('zpi', 0x52) ],
 'INA': [ ('imp', 0x1A) ],
 'INC': [ ('acc', 0x1A) ],
 'JMP': [ ('abxi', 0x7C) ],
 'LDA': [ ('zpi', 0xB2) ],
 'ORA': [ ('zpi', 0x12) ],
 'PHX': [ ('imp', 0xDA) ],
 'PHY': [ ('imp', 0x5A) ],
 'PLX': [ ('imp', 0xFA) ],
 'PLY': [ ('imp', 0x7A) ],
 'SBC': [ ('zpi', 0xF2) ],
 'STA': [ ('zpi', 0x92) ],
 'STZ': [ ('ab', 0x9C), ('abx', 0x9E), ('zp', 0x64), ('zpx', 0x74) ],
 'TRB': [ ('ab', 0x1C), ('zp', 0x14) ],
 'TSB': [ ('ab', 0x0C), ('zp', 0x04) ],
}

# Rockwell R65C02 instruction set (additions to CMOS 65C02 only)

_insR65C02 = {
 'BBR0': [ ('zptr', 0x0F) ], 'BBR1': [ ('zptr', 0x1F) ], 'BBR2': [ ('zptr', 0x2F) ], 'BBR3': [ ('zptr', 0x3F) ],
 'BBR4': [ ('zptr', 0x4F) ], 'BBR5': [ ('zptr', 0x5F) ], 'BBR6': [ ('zptr', 0x6F) ], 'BBR7': [ ('zptr', 0x7F) ],
 'BBS0': [ ('zptr', 0x8F) ], 'BBS1': [ ('zptr', 0x9F) ], 'BBS2': [ ('zptr', 0xAF) ], 'BBS3': [ ('zptr', 0xBF) ],
 'BBS4': [ ('zptr', 0xCF) ], 'BBS5': [ ('zptr', 0xDF) ], 'BBS6': [ ('zptr', 0xEF) ], 'BBS7': [ ('zptr', 0xFF) ],
 'RMB0': [ ('zp', 0x07) ], 'RMB1': [ ('zp', 0x17) ], 'RMB2': [ ('zp', 0x27) ], 'RMB3': [ ('zp', 0x37) ],
 'RMB4': [ ('zp', 0x47) ], 'RMB5': [ ('zp', 0x57) ], 'RMB6': [ ('zp', 0x67) ], 'RMB7': [ ('zp', 0x77) ],
 'SMB0': [ ('zp', 0x87) ], 'SMB1': [ ('zp', 0x97) ], 'SMB2': [ ('zp', 0xA7) ], 'SMB3': [ ('zp', 0xB7) ],
 'SMB4': [ ('zp', 0xC7) ], 'SMB5': [ ('zp', 0xD7) ], 'SMB6': [ ('zp', 0xE7) ], 'SMB7': [ ('zp', 0xF7) ],
}

# WDC W65C02S instruction set (additions to R65C02 only)

_insW65C02S = {
	'STP' : [ ('imp', 0xDB) ],
	'WAI' : [ ('imp', 0xCB) ],
}

# WDC W65C816S instruction set (additions to 65C02 and W65C02S only)

_insW65C816S = {
 'ADC': [ ('lab', 0x6F), ('labx', 0x7F), ('sr', 0x63), ('sriy', 0x73), ('lzpi', 0x67), ('lzpiy', 0x77) ],
 'AND': [ ('lab', 0x2F), ('labx', 0x3F), ('sr', 0x23), ('sriy', 0x33), ('lzpi', 0x27), ('lzpiy', 0x37) ],
 'BRL': [ ('lpcr', 0x82) ],
 'CMP': [ ('lab', 0xCF), ('labx', 0xDF), ('sr', 0xC3), ('sriy', 0xD3), ('lzpi', 0xC7), ('lzpiy', 0xD7) ],
 'COP': [ ('imm', 0x02), ('zp', 0x02) ], # add modes
 'EOR': [ ('lab', 0x4F), ('labx', 0x5F), ('sr', 0x43), ('sriy', 0x53), ('lzpi', 0x47), ('lzpiy', 0x57) ],
 'JML': [ ('abi', 0xDC), ('lab', 0x5C), ('labi', 0xDC) ], # add modes
 'JMP': [ ('lab', 0x5C), ('labi', 0xDC) ],
 'JSL': [ ('lab', 0x22) ],
 'JSR': [ ('abxi', 0xFC), ('lab', 0x22) ], # add modes
 'LDA': [ ('lab', 0xAF), ('labx', 0xBF), ('sr', 0xA3), ('sriy', 0xB3), ('lzpi', 0xA7), ('lzpiy', 0xB7) ],
 'MVN': [ ('bmv', 0x54) ],
 'MVP': [ ('bmv', 0x44) ],
 'ORA': [ ('lab', 0x0F), ('labx', 0x1F), ('sr', 0x03), ('sriy', 0x13), ('lzpi', 0x07), ('lzpiy', 0x17) ],
 'PEA': [ ('ab', 0xF4), ('imm', 0xF4) ], # add modes
 'PEI': [ ('zp', 0xD4), ('zpi', 0xD4) ], # add modes
 'PER': [ ('lpcr', 0x62) ],
 'PHB': [ ('imp', 0x8B) ],
 'PHD': [ ('imp', 0x0B) ],
 'PHK': [ ('imp', 0x4B) ],
 'PLB': [ ('imp', 0xAB) ],
 'PLD': [ ('imp', 0x2B) ],
 'REP': [ ('imm', 0xC2) ],
 'RTL': [ ('imp', 0x6B) ],
 'SBC': [ ('lab', 0xEF), ('labx', 0xFF), ('sr', 0xE3), ('sriy', 0xF3), ('lzpi', 0xE7), ('lzpiy', 0xF7) ],
 'SEP': [ ('imm', 0xE2) ],
 'STA': [ ('lab', 0x8F), ('labx', 0x9F), ('sr', 0x63), ('sriy', 0x93), ('lzpi', 0x87), ('lzpiy', 0x97) ],
 'SWP': [ ('imp', 0xEB) ], # alias XBA
 'TAD': [ ('imp', 0x5B) ], # alias TCD
 'TAS': [ ('imp', 0x1B) ], # alias TCS
 'TCD': [ ('imp', 0x5B) ],
 'TCS': [ ('imp', 0x1B) ],
 'TDA': [ ('imp', 0x7B) ], # alias TDC
 'TDC': [ ('imp', 0x7B) ],
 'TSA': [ ('imp', 0x3B) ], # alias TSC
 'TSC': [ ('imp', 0x3B) ],
 'TXA': [ ('imp', 0x9B) ],
 'TYX': [ ('imp', 0xBB) ],
 'WDM': [ ('imm', 0x42), ('imp', 0x42), ('zp', 0x42) ], # add modes
 'XBA': [ ('imp', 0xEB) ],
 'XCE': [ ('imp', 0xFB) ],
}

# -----------------------------

class CPUvariables(object):

	def __init__(self):

		# 16-bit processor 

		self.cpu16bit = False	# cpu is 16-bit ?
		self.acc16bit = False	# accumulator is 16-bit
		self.ndx16bit = False	# index registers are 16-bit
		self.directpage = 0		# default direct page
		self.databank   = 0		# default databank

		self.forcemode = None	# forced address mode flag

		self.mnemonics = set()	# recognized menmonics
		self.opcodes = dict()	# opcodes of mnemonics

_CPU = CPUvariables()

# -----------------------------

# required method
def name():
	''' return generic or family variant name '''
	return 'HXA65'

# required method
def reserved():
	'''HXA65 reserved symbols'''
	return [ ('__HXA65__', True),
		('A', True), ('X', True), ('Y', True),
		('S', True), ('P', True), ('PC', True),
		# for W65C816S only ( may be overkill, but no real harm! )
		('B', True), ('C', True),
		('DP', True), ('SP', True), ('DB', True), ('PB', True)
		]

# required method
def iscpu(this):
	'''is token a recognized CPU ?'''
	return this in [ '6502', '65C02', 'R65C02', 'W65C02S', 'W65C816S' ]

# required method
def getdescriptor(this):
	'''return cpu descriptor'''
	return 'T_24_L' if this == 'W65C816S' else 'T_16_L'

# required method
def setcpu(this):
	''' setup specific cpu for use '''

	def addins(this):
		'''add opcodes to current instruction set'''
		for mnemonic in this.keys():
			if not mnemonic in _CPU.mnemonics:
				_CPU.mnemonics.add( mnemonic )					# for faster lookup
				_CPU.opcodes[ mnemonic ] = dict()				# initialize directory
			_CPU.opcodes[ mnemonic ].update( this[mnemonic] )	# add addrmode, opcode pairs

	# default values
	_CPU.cpu16bit = False
	_CPU.acc16bit = _CPU.ndx16bit = False
	_CPU.directpage = _CPU.databank = 0

	# all processors get the base instruction set
	addins( _ins6502 )
	# other processors add instructions
	match this:
		case '65C02':
			addins( _ins65C02 )
		case 'R65C02':
			addins( _ins65C02 )
			addins( _insR65C02 )
		case 'W65C02S':
			addins( _ins65C02 )
			addins( _insR65C02 )
			addins( _insW65C02S )
		case 'W65C816S':
			_CPU.cpu16bit = True
			addins( _ins65C02 )
			addins( _insW65C02S )
			addins( _insW65C816S )

	return True

# required method
def isop(this):
	'''is token in current instruction set'''
	return this.upper() in _CPU.mnemonics

# -----------------------------

def save_opcode(mnemonic, addrmode):
	'''save a 65xx opcode'''
	CG.store( 'bit08', _CPU.opcodes[mnemonic][addrmode] )

def save_data(type, expr):
	'''evaluate and save 8-, 16- or 24-bit data'''
	# evalution may be incomplete after first pass
	ok, val = EXP.getnum( expr )
	CG.store( type, val if ok else 0 )

# -------------------------------

def save_mnemonic_expr(mnemonic, addrmode, bitop, expr):
	'''save mode if unforced, else save if forced mode is legal'''
	if _CPU.forcemode:
		# not a mode that can be forced ?
		if not addrmode.startswith(('ab', 'zp', 'lab', 'lzp')):
			return False

		match _CPU.forcemode:
			case 'zp':
				bitop = 'bit08'
				if addrmode.startswith('ab'):
					addrmode = 'zp' + addrmode[2:]
				elif addrmode.startswith('lab'):
					addrmode = 'zp' + addrmode[3:]
			case 'ab':
				bitop = 'bit16'
				if addrmode.startswith('zp'):
					addrmode = 'ab' + addrmode[2:]
				elif addrmode.startswith(('lab', 'lzp')):
					addrmode = 'ab' + addrmode[3:]
			case 'l':
				bitop = 'bit24'
				if addrmode.startswith(('ab', 'zp')):
					addrmode = 'l' + addrmode
			case _:
				UM.noway( addrmode )

		# a legal mode ?
		if addrmode not in _CPU.opcodes[mnemonic]:
			return False

	# save opcode and data
	save_opcode( mnemonic, addrmode )
	save_data( bitop, expr )
	return True

def save08(mnemonic, addrmode, expr):
	'''save opcode and 8-bit data'''
	return save_mnemonic_expr( mnemonic, addrmode, 'ubit08', expr )

def save16(mnemonic, addrmode, expr):
	'''save opcode and 16-bit data'''
	return save_mnemonic_expr( mnemonic, addrmode, 'ubit16', expr )

# -----------------------------

def save00(mnemonic, addrmode):
	'''save opcode with no data'''
	if not _CPU.forcemode:
		save_opcode( mnemonic, addrmode )
		return True
	else:	# these modes can't be forced
		return False

# -------------------------------

def zero_expr(mnemonic, allowed):
	'''handle mnemonic with no following expression'''
	# - all: acc (implicit), imp
	if 'acc' in allowed:
		return save00( mnemonic, 'acc' )
	elif 'imp' in allowed:
		return save00( mnemonic, 'imp' )
	else:
		return False

# -----------------------------

def resolve(mnemonic, abmode, zpmode, lmode, expr):
	'''try to resolve multiple possible address modes'''
	# 'abmode' is default (as per WDC standard)
	mode = abmode
	bitop = 'ubit16'

	# do we already have a hint ?
	# - 'abmode' can be forced to any legal mode, and
	# is guaranteed to be non-null (unlike the other two)
	if _CPU.forcemode:
		return save_mnemonic_expr( mnemonic, mode, bitop, expr )

	# try to evaluate expression
	ok, val = EXP.getnum( expr )

	# if resolved, we can select most appropriate size...
	if ok and EXP.resolved(val):
		# if there is a zero page mode and value is within zero page...
		if zpmode is not None and (val >= _CPU.directpage and val < _CPU.directpage + 256):
			mode = zpmode
			bitop = 'ubit08'
			val -= _CPU.directpage
		# if there is a long mode...
		elif lmode is not None:
			# if value is within the data bank use absolute addressing...
			if (val & 0xFFFF0000) == _CPU.databank:
				val -= _CPU.databank
			# ...otherwise use long addressing
			else:
				mode = lmode
				bitop = 'ubit24'

	# store (we already tried to evaluate expr)
	save_opcode( mnemonic, mode )
	CG.store( bitop, val )
	return True

def isindirect(expr):
	'''check for pre-indexed indirection'''
	# - to be true indirection indicator, initial open parenthesis
	# can be balanced only by terminal close parenthesis

	# leading and trailing parentheses -> possible indirection
	# - we can imagine '(expr1) + (expr2)', which would not be indirection
	if expr.startswith('(') and expr.endswith(')'):
		inparen = 0
		for i, ch in enumerate(expr):
			if ch == '(':
				inparen += 1
			elif ch == ')':
				inparen -= 1
				# if balance is reached only at end of expression, then indirect
				if not inparen:
					return len(expr) == i + 1

	# can't be indirect or is malformed (so not truly balanced, eh ?)
	return False

def islongindirect(expr):
	'''check for long indirect addressing'''
	return expr.startswith('[') and expr.endswith(']')

def isindexed(expr, indexch):
	'''check for address mode pre-indexed indirection'''
	# without using regular expressions !
	comma = expr.find( ',' )
	# pre-indexed indirect ?
	if comma > 0:
		tail = expr[comma+1:].upper()
		target = indexch
		while len(tail):
			tail = tail.lstrip()
			if tail.startswith(target):
				tail = tail[1:]
				target = ')' if target == indexch else 'EOE'
			else:
				break		# illegal char

		# found the target index char ?
		if target == 'EOE':
			return ( True, expr[1:comma] )

	# not pre-indexed indirect or malformed
	return ( False, expr[1:-1] )

# -------------------------------

def saveimm(mnemonic, expr):
	'''save immediate opcode and 8- or 16-bit data'''

	def imm16():
		'''determine if 8- or 16-bit immediate value is to be used'''
		nonlocal mnemonic
		if _CPU.cpu16bit:
			if _CPU.ndx16bit and mnemonic.endswith(('X', 'Y')):
				return True
			if mnemonic == 'PEA':
				return True
			if mnemonic in 'BRK|COP|REP|SEP|WDM':
				return False
			if _CPU.acc16bit and not mnemonic.endswith(('X', 'Y')):
				return True

	# 8-bit registers or tests above fell through
	if not _CPU.forcemode:
		save_opcode( mnemonic, 'imm' )
		save_data( 'bit16' if imm16() else 'bit08', expr[1:] )
		return True
	else:	# this mode can't be forced
		return False

# -------------------------------

def single_expr(mnemonic, allowed, expr):
	'''handle mnemonic with one following expression'''
	# - 6502:  ab, abi, acc (explicit), imm, pcr, zp, zpxi
	# - 65c02, r65c02, w65c02s: abxi, zpi
	# - w65c816s: lab, lpcr, lzpi

	# immediate ?
	if expr.startswith('#'):
		return saveimm(mnemonic, expr) if 'imm' in allowed else False

	# accumulator (explicit) ?
	if expr.upper() == 'A':
		return save00(mnemonic, 'acc') if 'acc' in allowed else False

	# absolute indirect or zero page indirect ?
	if isindirect(expr):
		# x-indexed indirect ?
		yes, nexpr = isindexed( expr, 'X' )
		if yes:
			if 'abxi' in allowed:
				return save16( mnemonic, 'abxi', nexpr )
			elif 'zpxi' in allowed:
				return save08( mnemonic, 'zpxi', nexpr )
			else:
				return False

		# indirect
		if 'abi' in allowed:
			return save16( mnemonic, 'abi', nexpr )
		elif 'zpi' in allowed:
			return save08( mnemonic, 'zpi', nexpr )
		else:
			return False

	# possibly long ?
	if _CPU.cpu16bit:

		# long indirect ?
		if islongindirect(expr):
			if 'lzpi' in allowed:
				return save08( mnemonic, 'lzpi', expr[1:-1] )
			else:
				return False

		# long pc relative ?
		if 'lpcr' in allowed:
			return save_mnemonic_expr( mnemonic, 'lpcr', 'rbit16', expr )

		# long absolute ?
		if 'lab' in allowed:
			# 'ab' and 'zp' and 'lab' are not mutually exclusive
			if  'zp' in allowed:
				return resolve( mnemonic, 'ab', 'zp', 'lab', expr )
			elif 'ab' in allowed:
				return resolve( mnemonic, 'ab', None, 'lab', expr )
			else:
				return save_mnemonic_expr( mnemonic, 'lab', 'ubit24', expr )

	# pc relative ?
	if 'pcr' in allowed:
		return( save_mnemonic_expr(mnemonic, 'pcr', 'rbit08', expr) )

	# absolute ?
	if 'ab' in allowed:
		# 'ab' and 'zp' are not mutually exclusive
		if 'zp' in allowed:
			return resolve( mnemonic, 'ab', 'zp', None, expr )
		else:
			return save16( mnemonic, 'ab', expr )

	# zero page ?
	if 'zp' in allowed:
		return save08( mnemonic, 'zp', expr )

	# no matching address mode
	return False

# -------------------------------

def double_expr(mnemonic, allowed, expr1, expr2):
	'''handle mnemonic with two following expressions'''
	# - 6502, 65c02: abx, aby, zpx, zpiy, zpy 
	# - r65c02, w65c02s: zptr
	# - w65c816s: bmv, labx, lzpiy, sr, sriy

	# what about that second expression ?
	match expr2.upper():
		# Y-indexed ?
		case 'Y':

			# zero page indirect or stack relative indirect ?
			if isindirect(expr1):

				# stack-relative indirect ?
				yes, nexpr = isindexed( expr1, 'S' )
				if yes:
					if 'sriy' in allowed:
						return save08( mnemonic, 'sriy', nexpr )

				# zero-page indirect ?
				elif 'zpiy' in allowed:
					return save08( mnemonic, 'zpiy', nexpr )

				# illegal indirect
				return False

			# possibly long ?
			if _CPU.cpu16bit:

				# long indirect ?
				if islongindirect(expr1):
					if 'lzpiy' in allowed:
						return save08( mnemonic, 'lzpiy', expr1[1:-1] )
					else:
						return False

			# absolute ?
			if 'aby' in allowed:
				# 'aby' and 'zpy' are not mutually exclusive
				if 'zpy' in allowed:
					return resolve( mnemonic, 'aby', 'zpy', None, expr1 )
				else:
					return save16( mnemonic, 'aby', expr1 )

			# zero page ?
			if 'zpy' in allowed:
				return save08( mnemonic, 'zpy', expr1 )

			# illegal
			return False

		# X-indexed ?
		case 'X':

			if 'labx' in allowed:
				return resolve( mnemonic, 'abx', 'zpx', 'labx', expr1 )
			elif 'abx' in allowed:
				return resolve( mnemonic, 'abx', 'zpx', None, expr1 )
			elif 'zpx' in allowed:
				return save08( mnemonic, 'zpx', expr1 )
			else:
				return False

		# stack relative ?
		case 'S':

			if 'sr' in allowed:
				return save08( mnemonic, 'sr', expr1 )
			else:
				return False

		# everything else
		case _:

			# block move ?
			if 'bmv' in allowed:
				if save_mnemonic_expr(mnemonic, 'bmv', 'ubit08', f'^{expr2}'):
					save_data( 'ubit08', f'^{expr1}' )
					return True

			# zero page test relative ?
			elif 'zptr' in allowed:
				if save_mnemonic_expr(mnemonic, 'zptr', 'ubit08', expr1):
					save_data( 'rbit08', expr2 )
					return True 

			# not legal or save failed
			return False

# -------------------------------

# required method
def doop(mnemonic, exprcnt, exprlist):
	''' process cpu-specific mnemonic and any associated expression(s)'''
	mnemonic = mnemonic.upper()
	allowed = _CPU.opcodes[ mnemonic ]

	# how many expression fields are there ?
	# - break them down into easier to handle subtypes
	match exprcnt:
		case 0:
			legalmode = zero_expr( mnemonic, allowed )
		case 1:
			legalmode = single_expr( mnemonic, allowed, exprlist[0] )
		case 2:
			legalmode = double_expr( mnemonic, allowed, exprlist[0], exprlist[1] )
		case _:
			legalmode = False

	# any forced address mode is only active for one line
	_CPU.forcemode = None

	# 'NoWay' should never appear if things are working correctly
	return ( legalmode, 'NoWay' if legalmode else 'BadMode' )

# -------------------------------

def getbyteval(expr, current, offset):
	'''get 8-bit value for ASSUME'''
	ok, val = EXP.getinrange( expr, 0x00, 0xff )
	return val * offset if ok and EXP.resolved(val) else current

def getwordval(expr, current):
	'''get (almost) 16-bit value for ASSUME'''
	ok, val = EXP.getinrange( expr, 0x0000, 0xff00 )
	return val if ok and EXP.resolved(val) else current

def getsizeflag(expr, current):
	'''get index or accumulator size flag'''
	ok, val = EXP.getinrange( expr, 8, 16 )
	if ok and EXP.resolved(val):
		match val:
			case 8:
				return False
			case 16:
				return True
			case _:
				UM.error( 'OddVal', val )

	return current

# required method
def doassume(cmd, arg):
	''' handle cpu-specific "ASSUME" psop '''
	match cmd:
		# all cpus support these assumptions

		# set forced address mode ?
		case 'addr':
			match arg:
				case 'absolute':
					_CPU.forcemode = 'ab'
				case 'zeropage' | 'direct':
					_CPU.forcemode = 'zp'
				case 'long':
					_CPU.forcemode = 'l'
				case _:
					return False

		# set zero (direct) page location ?
		case 'zeropage':
			_CPU.directpage = getbyteval( arg, _CPU.directpage, 0x100 )

		# remaining options only apply to 16-bit cpus

		# set index register size ?
		case 'index' if _CPU.cpu16bit:
			_CPU.ndx16bit = getsizeflag( arg, _CPU.ndx16bit )

		# set accumulator size ?
		case 'accum' if _CPU.cpu16bit:
			_CPU.acc16bit = getsizeflag( arg, _CPU.acc16bit )

		# set direct page ?
		case 'directpage' if _CPU.cpu16bit:
			_CPU.directpage = getwordval( arg, _CPU.directpage )

		# set data bank ?
		case 'databank' if _CPU.cpu16bit:
			_CPU.databank = getbyteval( arg, _CPU.databank, 0x1000 )

		# don't recognize; did not handle
		case _:
			return False

	# handled (error or not)
	return True

# -------------------------------

# mostly just a module syntax check
# - doesn't catch every syntax error
if __name__  == "__main__":
	setcpu( '6502' )

