# Hobby Cross-Assembler (HXA) V1.00 - INS_T_XX (CPU descriptor only)

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

# source language: Python 3.11.4

# first created: 01/18/03	(in Thompson AWK 4.0)
# last revision: 11/20/23

# preferred public function prefix: CPU

# ----------------------------

# - the T_XX "family" of test "processors" currently do nothing except
# provide values for other HXA modules
# - this permits all non-processor specific aspects of HXA
# to be tested (which turns out to be most of HXA, actually :-) )
# - this file also provides a compact look at the functions which must
# be provided here and called elsewhere in order to adapt HXA to other,
# real processors

# Address modes: none

# Instruction set: none

# ----------------------------
import re
# other HXA modules
import hxa_usermesg as UM
import hxa_expressions as EXP
# ----------------------------

# required method
def name():
	''' return generic or family variant name '''
	return 'HXA_T'

# required method
def reserved():
	''' generic initialization '''
	# note reserved symbols
	return [ ('__HXA_T__', True) ]

# required method
def iscpu(this):
	''' is token a recognized CPU ? '''
	# - here only the standard cpu descriptor is accepted: "T_PC_MB(SZ)"
	# - "PC" is program counter size ("08" to "32" bits)
	# - "MB" is orientation of multi-byte quantities, least- or most-
	# significant byte first ("L" or "M")
	# - "(SZ)" is optional "byte size" (smallest addressable unit), 8- or 16- or 32-bits
	# - if not present, eight bit bytes are assumed
	# - ex: "T_16_L" -> 16 bit program counter, least significant byte first, 8-bit byte size
	# - ex: "T_24_M16" -> 24 bit program counter, most significant byte first, 16-bit byte size

	m = re.fullmatch( 'T_[0-9][0-9]_[LM](08|16|32)?', this, re.IGNORECASE )
	return m is not None

# required method
def getdescriptor(this):
	''' return cpu descriptor '''
	# - one and the same as cpu in this case
	return this.upper()

# required method
def setcpu(this):
	''' setup specific cpu for use '''
	# - nothing to do !
	return True

# required method
def isop(this):
	''' is token in current instruction set ? '''
	# - there are no instructions in the set
	return False

# required method
def doop(mnemonic, cnt, expr):
	''' process cpu-specific mnemonic and any associated expression(s) '''
	# - since there aren't any mnemonics this shouldn't be called
	UM.noway( mnemonic )

# required method
def doassume(cmd, arg):
	''' handle cpu-specific "ASSUME" psop '''
	# here we just echo them to test whether the call works or not

	# "UMdoecho()" is *not* a function that's required to be called
	# by any cpu module; it's used here just to show
	# that the arguments have been passed correctly (or not)

	str = f'Cmd: {cmd} Arg: {arg}'

	UM.doecho( None, str )

	# everything passes but the string "printable"
	# - this is strictly for testing
	# - "printable" is a command recognized by earlier ASSUME handling (in hxa_strings)
	# - but if the argument isn't, then ASSUME handling continues until it reaches here
	# - if "printable" shows up, then its argument was bad and we report it
	# - we could do this with any command that is recognized and handled (or not) by
	# previous handlers, but one is enough for testing purposes

	return 'printable' not in str


