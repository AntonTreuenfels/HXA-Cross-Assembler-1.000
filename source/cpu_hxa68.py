# Hobby Cross-Assembler (HXA) V1.100 - Instruction Set (68xx Version)

# (c) 2024 by Anton Treuenfels

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
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

# e-mail: teamtempst@yahoo.com

# source language: Python 3.11.4

# first created: 03/01/24
# last revision: 06/15/24

# preferred public function prefix: 'CPU'

# ----------------------------
# other HXA modules
import hxa_usermesg as UM
import hxa_codegen as CG
import hxa_expressions as EXP
# ----------------------------

# Address modes:					Operand:

# acc 	Integrated Accumulator		(none)
# accx	Seperate Accumulator 		A | B
# dir	Direct						addr8 (if less than 256)
# dual	Dual						accx [ ] (imm | dir | ndx | ext)
# ext	Extended					addr16
# imm 	Immediate					data8
# inh	Inherent					(none)
# ndx	Indexed						indx8
# rel	Relative					disp8

# M6800 instruction set

_ins6800 = {
 'ABA':  { ('inh', 0x1B) },
 'ADC':  { ('dual', None) },
 'ADCA': { ('imm', 0x89), ('dir', 0x99), ('ndx', 0xA9), ('ext', 0xB9) },
 'ADCB': { ('imm', 0xC9), ('dir', 0xD9), ('ndx', 0xE9), ('ext', 0xF9) },
 'ADD':  { ('dual', None) }, 
 'ADDA': { ('imm', 0x8B), ('dir', 0x9B), ('ndx', 0xAB), ('ext', 0xBB) },
 'ADDB': { ('imm', 0xCB), ('dir', 0xDB), ('ndx', 0xEB), ('ext', 0xFB) },
 'AND':  { ('dual', None) },
 'ANDA': { ('imm', 0x84), ('dir', 0x94), ('ndx', 0xA4), ('ext', 0xB4) },
 'ANDB': { ('imm', 0xC4), ('dir', 0xD4), ('ndx', 0xE4), ('ext', 0xF4) },
 'ASL':  { ('accx', None), ('ndx', 0x68), ('ext', 0x78) },
 'ASLA': { ('acc', 0x48) },
 'ASLB': { ('acc', 0x58) },
 'ASR':  { ('accx', None), ('ndx', 0x67), ('ext', 0x77) },
 'ASRA': { ('acc', 0x47) },
 'ASRB': { ('acc', 0x57) },
 'BCC':  { ('rel', 0x24) },
 'BCS':  { ('rel', 0x25) },
 'BEQ':  { ('rel', 0x27) },
 'BGE':  { ('rel', 0x2C) },
 'BGT':  { ('rel', 0x2E) },
 'BHI':  { ('rel', 0x22) },
 'BIT':  { ('dual', None) },
 'BITA': { ('imm', 0x85), ('dir', 0x95), ('ndx', 0xA5), ('ext', 0xB5) },
 'BITB': { ('imm', 0xC5), ('dir', 0xD5), ('ndx', 0xE5), ('ext', 0xF5) },
 'BLE':  { ('rel', 0x2F) },
 'BLS':  { ('rel', 0x23) },
 'BLT':  { ('rel', 0x2D) },
 'BMI':  { ('rel', 0x28) },
 'BNE':  { ('rel', 0x26) },
 'BPL':  { ('rel', 0x2A) },
 'BRA':  { ('rel', 0x20) },
 'BSR':  { ('rel', 0x8D) },
 'BVC':  { ('rel', 0x28) },
 'BVS':  { ('rel', 0x29) },
 'CBA':  { ('inh', 0x11) },
 'CLC':  { ('inh', 0x0C) },
 'CLI':  { ('inh', 0x0E) },
 'CLR':  { ('accx', None), ('ndx', 0x6F), ('ext', 0x7F) },
 'CLRA': { ('acc', 0x4F) },
 'CLRB': { ('acc', 0x5F) },
 'CLV':  { ('inh', 0x0A) },
 'CMP':  { ('dual', None) },
 'CMPA': { ('imm', 0x81), ('dir', 0x91), ('ndx', 0xA1), ('ext', 0xB1) },
 'CMPB': { ('imm', 0xC1), ('dir', 0xD1), ('ndx', 0xE1), ('ext', 0xF1) },
 'COM':  { ('accx', None), ('ndx', 0x63), ('ext', 0x73) },
 'COMA': { ('acc', 0x43) },
 'COMB': { ('acc', 0x53) },
 'CPX':  { ('imm', 0x8C), ('dir', 0x9C), ('ndx', 0xAC), ('ext', 0xBC) },
 'DAA':  { ('inh', 0x19) },
 'DEC':  { ('accx', None), ('ndx', 0x6A), ('ext', 0x7A) },
 'DECA': { ('acc', 0x4A) },
 'DECB': { ('acc', 0x5A) },
 'DES':  { ('inh', 0x34) },
 'DEX':  { ('inh', 0x09) },
 'EOR':  { ('dual', None) },
 'EORA': { ('imm', 0x88), ('dir', 0x98), ('ndx', 0xA8), ('ext', 0xB8) },
 'EORB': { ('imm', 0xC8), ('dir', 0xD8), ('ndx', 0xE8), ('ext', 0xF8) },
 'INC':  { ('accx', None), ('ndx', 0x6C), ('ext', 0x7C) },
 'INCA': { ('acc', 0x4C) },
 'INCB': { ('acc', 0x5C) },
 'INS':  { ('inh', 0x31) },
 'INX':  { ('inh', 0x08) },
 'JMP':  { ('ndx', 0x6E), ('ext', 0x7E) },
 'JSR':  { ('ndx', 0xAD), ('ext', 0xBD) },
 'LDA':  { ('dual', None) },
 'LDAA': { ('imm', 0x86), ('dir', 0x96), ('ndx', 0xA6), ('ext', 0xB6) },
 'LDAB': { ('imm', 0xC6), ('dir', 0xD6), ('ndx', 0xE6), ('ext', 0xF6) },
 'LDS':  { ('imm', 0x8E), ('dir', 0x9E), ('ndx', 0xAE), ('ext', 0xBE) },
 'LDX':  { ('imm', 0xCE), ('dir', 0xDE), ('ndx', 0xEE), ('ext', 0xFE) },
 'LSR':  { ('accx', None), ('ndx', 0x64), ('ext', 0x74) },
 'LSRA': { ('acc', 0x44) },
 'LSRB': { ('acc', 0x54) },
 'NEG':  { ('accx', None), ('ndx', 0x60), ('ext', 0x70) },
 'NEGA': { ('acc', 0x40) },
 'NEGB': { ('acc', 0x50) },
 'NOP':  { ('inh', 0x01) },
 'ORA':  { ('dual', None) },
 'ORAA': { ('imm', 0x8A), ('dir', 0x9A), ('ndx', 0xAA), ('ext', 0xBA) },
 'ORAB': { ('imm', 0xCA), ('dir', 0xDA), ('ndx', 0xEA), ('ext', 0xFA) },
 'PSH':  { ('accx', None) },
 'PSHA': { ('acc', 0x36) },
 'PSHB': { ('acc', 0x37) },
 'PUL':  { ('accx', None) },
 'PULA': { ('acc', 0x32) },
 'PULB': { ('acc', 0x33) },
 'ROL':  { ('accx', None), ('ndx', 0x69), ('ext', 0x79) },
 'ROLA': { ('acc', 0x49) },
 'ROLB': { ('acc', 0x59) },
 'ROR':  { ('accx', None), ('ndx', 0x66), ('ext', 0x76) },
 'RORA': { ('acc', 0x46) },
 'RORB': { ('acc', 0x56) },
 'RTI':  { ('inh', 0x3B) },
 'RTS':  { ('inh', 0x39) },
 'SBA':  { ('inh', 0x10) },
 'SBC':  { ('dual', None) },
 'SBCA': { ('imm', 0x82), ('dir', 0x92), ('ndx', 0xA2), ('ext', 0xB2) },
 'SBCB': { ('imm', 0xC2), ('dir', 0xD2), ('ndx', 0xE2), ('ext', 0xF2) },
 'SEC':  { ('inh', 0x0D) },
 'SEI':  { ('inh', 0x0F) },
 'SEV':  { ('inh', 0x08) },
 'STA':  { ('dual', None) },
 'STAA': { ('dir', 0x97), ('ndx', 0xA7), ('ext', 0xB7) },
 'STAB': { ('dir', 0xD7), ('ndx', 0xE7), ('ext', 0xF7) },
 'STS':  { ('dir', 0x9F), ('ndx', 0xAF), ('ext', 0xBF) },
 'STX':  { ('dir', 0xDF), ('ndx', 0xEF), ('ext', 0xFF) },
 'SUB':  { ('dual', None) },
 'SUBA': { ('imm', 0x80), ('dir', 0x90), ('ndx', 0xA0), ('ext', 0xB0) },
 'SUBB': { ('imm', 0xC0), ('dir', 0xD0), ('ndx', 0xE0), ('ext', 0xF0) },
 'SWI':  { ('inh', 0x3F) },
 'TAB':  { ('inh', 0x16) },
 'TAP':  { ('inh', 0x06) },
 'TBA':  { ('inh', 0x17) },
 'TPA':  { ('inh', 0x07) },
 'TST':  { ('accx', None), ('ndx', 0x6D), ('ext', 0x7D) },
 'TSTA': { ('acc', 0x4D) },
 'TSTB': { ('acc', 0x5D) },
 'TSX':  { ('inh', 0x30) },
 'TXS':  { ('inh', 0x35) },
 'WAI':  { ('inh', 0x3E) }, 
}

# M6801/6803 instruction set (additions only)

_ins6803 = {
 'ABX':  { ('inh', 0x3A) },
 'ADDD': { ('imm', 0xC3), ('dir', 0xD3), ('ndx', 0xE3), ('ext', 0xF3) },
 'ASLD': { ('inh', 0x05) },
 'BHS':  { ('rel', 0x24) },					# alias for 'BCC'
 'BLO':  { ('rel', 0x25) }, 				# alias for 'BCS'
 'BRN':  { ('rel', 0x21) },
 'JSR':  { ('dir', 0x9D) },					# avoid accidental 'HCF' ?
 'LDD':  { ('imm', 0xCC), ('dir', 0xDC), ('ndx', 0xEC), ('ext', 0xFC) },
 'LSL':  { ('ndx', 0x68), ('ext', 0x78) },	# alias for 'ASL'
 'LSLD': { ('inh', 0x05) },					# alias for 'ASLD'
 'LSRD': { ('inh', 0x04) },
 'MUL':  { ('inh', 0x3D) },
 'PSHX': { ('inh', 0x3C) },
 'PULX': { ('inh', 0x38) },
 'STD':  { ('dir', 0xDD), ('ndx', 0xED), ('ext', 0xFD) },
 'SUBD': { ('imm', 0x83), ('dir', 0x93), ('ndx', 0xA3), ('ext', 0xB3) },
}

# -----------------------------

class CPUvariables(object):

	def __init__(self):

		self.directpage = 0		# default direct page

		self.forcemode = None	# forced address mode flag

		self.mnemonics = set()	# recognized menmonics
		self.opcodes = dict()	# opcodes of mnemonics

_CPU = CPUvariables()

# ----------------------------

# required method
def name():
	''' return generic or family variant name '''
	return 'HXA68'

# required method
def reserved():
	'''HXA68 reserved symbols'''
	return [ ('__HXA68__', True),
		# 6800
		('A', True), ('B', True), ('X', True),
		('S', True), ('P', True), ('PC', True),
		# 6801/6803
		('D', True), 
		]

def _normalize(this):
	'''normalize 6800 family name'''
	this = this.upper()
	if this.startswith('MC'):
		return this[2:]
	elif this.startswith('M'):
		return this[1:]
	else:
		return this

# required method
def iscpu(this):
	'''is token a recognized CPU ?'''
	return _normalize(this) in [ '6800', '6801', '6803' ]

# required method
def getdescriptor(this):
	'''return cpu descriptor'''
	return 'T_16_M'

# required method
def setcpu(this):
	''' setup specific cpu for use '''

	def addins(this):
		'''add opcodes to current instruction set'''
		for mnemonic in this.keys():
			if not mnemonic in _CPU.mnemonics:
				_CPU.mnemonics.add( mnemonic )					# for faster lookup
				_CPU.opcodes[ mnemonic ] = dict()				# initialize dictionary
			_CPU.opcodes[ mnemonic ].update( this[mnemonic] )	# add addrmode, opcode pairs

	# default values
	
	_CPU.directpage = 0

	# other processors add instructions
	match _normalize(this):
		case '6800':
			addins( _ins6800 )
		case '6801' | '6803':
			addins( _ins6800 )
			addins( _ins6803 )
		case _:
			UM.noway( this )

	return True

# required method
def isop(this):
	'''is token in current instruction set'''
	return this.upper() in _CPU.mnemonics

# -----------------------------

def save_opcode(mnemonic, addrmode):
	'''save a 68 xx opcode'''
	CG.store( 'bit08', _CPU.opcodes[mnemonic][addrmode] )

def save_data(type, expr):
	'''evaluate and save 8- or 16-bit data'''
	# evalution may be incomplete after first pass
	ok, val = EXP.getnum( expr )
	CG.store( type, val if ok else 0 )
	return True if ok else False

# -----------------------------

def save00(mnemonic, addrmode):
	'''save opcode with no data'''
	if not _CPU.forcemode:
		save_opcode( mnemonic, addrmode )
		return True
	else:	# these modes can't be forced
		return False

def save08u(mnemonic, addrmode, expr):
	'''save opcode and 8-bit direct page addr'''
	if not _CPU.forcemode:
		save_opcode( mnemonic, addrmode )
		return save_data( 'ubit08', expr )
	else:	# these modes can't be forced
		return False

def save08r(mnemonic, expr):
	'''save opcode and 8-bit relative offeset'''
	if not _CPU.forcemode:
		save_opcode( mnemonic, 'rel' )
		return save_data( 'rbit08', expr )
	else:	# these modes can't be forced
		return False

def save08or16(mnemonic, allowed, expr):
	'''save opcode and 8- or 16-bit addr'''
	match _CPU.forcemode:
		case 'direct' if 'dir' in allowed:
			save_opcode( mnemonic, 'dir' )
			return save_data( 'bit08', expr )	# no range check, excess ignored

		case 'extended' if 'ext' in allowed:
			save_opcode( mnemonic, 'ext' )
			return save_data( 'bit16', expr )	# no range check, excess ignored

		case _:
			ok, val = EXP.getnum( expr )
			if ok:
				# are these conditions True ?
				if 'dir' in allowed and EXP.resolved(val) and val < 256:
					save_opcode( mnemonic, 'dir' )
					CG.store( 'ubit08', val )
					return True
				# default to 16-bit addr
				elif 'ext' in allowed:
					save_opcode( mnemonic, 'ext' )
					CG.store( 'ubit16', val )
					return True

	# couldn't evaluate or addr mode not allowed
	return False

# -------------------------------

def saveimm(mnemonic, expr):
	'''save 8- or 16-bit immediate value'''
	if not _CPU.forcemode:
		save_opcode( mnemonic, 'imm' )
		save_data( 'ubit16' if mnemonic in ['CPX', 'LDS', 'LDX'] else 'ubit08', expr[1:] )
		return True
	else:	# these modes can't be forced
		return False

# -------------------------------

def zero_expr(mnemonic, allowed):
	'''handle mnemonic with no following expression'''
	# - all: acc (implicit in the mnemonic), imp
	if 'acc' in allowed:
		return save00( mnemonic, 'acc' )
	elif 'inh' in allowed:
		return save00( mnemonic, 'inh' )
	else:
		return False

# -------------------------------

def single_expr(mnemonic, allowed, expr):
	'''handle mnemonic with one following expression'''

	# immediate ?
	if expr.startswith('#'):
		return saveimm(mnemonic, expr) if 'imm' in allowed else False

	# accumulator, direct, indexed or extended ?
	exp = expr.upper()
	match exp:
		# accumulator (explicit in the expression) ?
		case "A" | "B":
			return save00( mnemonic, 'acc' ) if 'acc' in allowed else False
		# indexed (implicitly from zero) ?
		case "X":
			return save08u(mnemonic, 'ndx', '0') if 'ndx' in allowed else False
		# relative, direct or extended
		case _:
			if 'rel' in allowed:
				return save08r( mnemonic, expr )
			else:
				return save08or16( mnemonic, allowed, expr )

	# no matching address mode
	return False

# -------------------------------

def double_expr(mnemonic, allowed, expr1, expr2):
	'''handle mnemonic with two following expressions'''

	# what about that second expression ?
	# - 6800 : only X
	if expr2.upper() == "X":
		return save08u(mnemonic, 'ndx', expr1) if 'ndx' in allowed else False
	else:
		return False

# -----------------------------

# required method
def doop(mnemonic, exprcnt, exprlist):
	''' process cpu-specific mnemonic and any associated expression(s)'''

	def isaccx(expr):
		return expr in ['A', 'B', 'a', 'b']

	def isdual(expr):
		# if only spaces follow accumulator, they'll have been stripped off already
		# - so here we're looking for 'A|B expr[,X]'
		# - 'A,X' looks like it should be legal, but it's not (no space after 'A')
		return expr.startswith(('A ', 'B ', 'a ', 'b '))

	def noaccum(expr):
		'''expr cannot be 'accx' nor 'dual' mode'''
		return False if isaccx(expr) or isdual(expr) else True

	mnemonic = mnemonic.upper()
	allowed = _CPU.opcodes[ mnemonic ]

	# we don't actually need to do all of the following checks just yet
	# - but the idea is to prevent evaulating expressions that cannot possibly succeed
	# - in turn, cutting down on the possible number of errors that can happen

	# assume we're going to wind up with a legal address mode
	legalmode = True
	# 'accx' is a flag mode meaning an accumulator *may* be the expression
	if 'accx' in allowed:
		match exprcnt:
			case 1:
				expr = exprlist[ 0 ]
				if isaccx(expr):
					mnemonic = f'{mnemonic}{expr.upper()}'
					allowed = _CPU.opcodes[ mnemonic ]
					exprlist = []
					exprcnt = 0
				elif isdual(expr):
					legalmode = False
			case 2:
				legalmode = noaccum( exprlist[0] )
			case _:
				legalmode = False

	# 'dual' is a flag mode meaning that an accumulator *must* start the expression
	elif 'dual' in allowed:
		match exprcnt:
			case 1 | 2:
				expr = exprlist[ 0 ]
				if len(expr) > 2 and isdual(expr):
					mnemonic = f'{mnemonic}{expr[0].upper()}'
					allowed = _CPU.opcodes[ mnemonic ]
					exprlist[0] = expr[2:].lstrip()
				else:
					legalmode = False
			case _:
				legalmode = False

	# 'acc' mode means an accumulator is part of the mnemonic
	# 'inh' mode means the mnemonic specifies everything
	elif 'acc' in allowed or 'inh' in allowed:
		match exprcnt:
			case 0:
				pass
			case _:
				legalmode = False

	# no other mode can start with an accumulator
	elif exprcnt > 0:
		legalmode = noaccum( exprlist[0] )

	# can't force a non-allowed mode
	match _CPU.forcemode:
		case 'direct' if not 'dir' in allowed:
			legalmode = False
		case 'extended' if not 'ext' in allowed:
			legalmode - False
		case _:
			pass

	if legalmode:
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

# required method
def doassume(cmd, arg):
	''' handle cpu-specific "ASSUME" psop '''
	match cmd:
		# all cpus support these assumptions

		# set forced address mode ?
		case 'addr':
			match arg:
				case 'direct' | 'extended':
					_CPU.forcemode = arg
				case _:
					return False


		# don't recognize; did not handle
		case _:
			return False

	# handled (error or not)
	return True

# -------------------------------

# mostly just a module syntax check
# - doesn't catch every syntax error
if __name__  == "__main__":
	setcpu( '6800' )

