# Hobby Cross-Assembler (HXA) V1.200 - Floats

# (c) 2024 by Anton Treuenfels

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

# first created: 09/17/24
# last revision: 10/14/24

# preferred public function prefix: FP

# -----------------------------
import math
from struct import pack
# other HXA modules
import hxa_codegen as CG
import hxa_usermesg as UM
import hxa_misc as UTIL
# -----------------------------

# module variables

class FPvariables(object):

	def __init__(self):

		# range limit constants

		self.DOUBLE_MAX = (2 - 2**-52) * 2**1023	# 1.797693134862315708145274237317e+308
		self.DOUBLE_MIN = 2**-1022					# 2.2250738585072013830902327173324e-308

		self.SINGLE_MAX = (2 - 2**-23) * 2**127		# 3.4028234663852885981170418348452e+38
		self.SINGLE_MIN = 2**-126					# 1.1754943508222875079687365372222e-38

		self.HALF_MAX = (2 - 2**-10) * 2**15		# 65504
		self.HALF_MIN = 2**-14						# 0.00006103515625

		self.ESM4_MAX = (2 - 2**-31) * 2**126		# 1.7014118342085515047455513491911e+38
		self.ESM4_MIN = 2**-128						# 2.9387358770557187699218413430556e-39

		# floating point output format

		self.output = 'ieee-double-be'				# default

_FP = FPvariables()

# -----------------------------
# psop: ASSUME flag|flag[:=]val
# -----------------------------

def doassume(flag, arg):
	'''check if ASSUME refers to floating point'''

	def _normalize(this):
		match this:
			case 'cbm'|'apple2'|'bbc'|'bbc-6502':
				return 'esm4-be'
			case 'bbc-z80':
				return 'esm4-le'
			case _:
				return this

	if flag == 'float':
		if arg in [
			'ieee-double', 'ieee-double-be', 'ieee-double-le',
			'ieee-single', 'ieee-single-be', 'ieee-single-le',
			'ieee-half', 'ieee-half-be', 'ieee-half-le',
			'esm4', 'esm4-be', 'esm4-le',
			'cbm', 'apple2', 'bbc', 'bbc-6502', 'bbc-z80', 
		]:
			_FP.output = _normalize( arg )
			# handled
			return True

	# not handled here
	return False

# -----------------------------

def _accept(this):
	'''collect a finite floating point value'''
	# we assume the result is an IEEE-754 double
	try:
		val = float( this )
	# this is by far the most common error float() throws
	except ValueError:
		UM.error( "NeedFloat", this )
	# this is a difficult error to throw (haven't managed it yet)
	except OverflowError:
		UM.error( "BadRange", this )
	# this is a difficult error to throw (haven't managed it yet)
	except Exception:
		UM.error( "BadToken", this )
	# we have something Python considers a float value
	else:
		# is it finite ?
		if not math.isfinite(val):
			UM.error( "BadRange", this )
		# zero ? (which can also happen for very small numbers, eg., 1e-350)
		elif val == 0:
			return 0, 0, 0, 0
		# probably only sub-normals can be caught here, but also probably doesn't hurt
		elif UTIL.inrange(math.fabs(val), _FP.DOUBLE_MIN, _FP.DOUBLE_MAX):
			# get sign, mantissa and exponent
			man, exp = math.frexp( val )
			sgn = 1 if man < 0 else 0
			# 1-bit sign, 11-bit exponent, 52-bit mantissa (technically)
			return sgn, exp, math.fabs(man), val

	# not a float value we can do anything with
	return None, None, None, None

# -----------------------------
# psop: FLOAT val [[, val]...]
# -----------------------------

def dofloat(label, floats):
	''' handle FLOAT psop '''
	for fpval in floats:
		sign, expo, mant, valu = _accept( fpval )
		if valu is None:
			continue

		match (_FP.output):
			# 1-bit sign, 11-bit exponent, 52-bit mantissa
			case 'ieee-double'|'ieee-double-be'|'ieee-double-le':
				bytefmt = '<d' if _FP.output.endswith('le') else '>d'
				bytelst = pack( bytefmt, valu )
				CG.store( 'bytes', bytearray(bytelst) )

			# 1-bit sign, 8-bit exponent, 23-bit mantissa
			case 'ieee-single'|'ieee-single-be'|'ieee-single-le':
				if valu == 0 or UTIL.inrange(math.fabs(valu), _FP.SINGLE_MIN, _FP.SINGLE_MAX):
					exp = expo + 126 if mant != 0 else 0
					man = int( round(mant * 2**24) )
					fp0 = (sign << 7) | ((exp & 0xFE) >> 1)
					fp1 = ((man & 0x7F0000) >> 16) | ((exp & 0x01) << 7)
					fp2 = (man & 0x00FF00) >> 8
					fp3 = (man & 0x0000FF)
					bytelst = [fp3, fp2, fp1, fp0] if _FP.output.endswith('le') else [fp0, fp1, fp2, fp3]
					CG.store( 'bytes', bytearray(bytelst) )

			# 1-bit sign, 5-bit exponent, 10-bit mantissa
			case 'ieee-half'|'ieee-half-be'|'ieee-half-le':
				if valu == 0 or UTIL.inrange(abs(valu), _FP.HALF_MIN, _FP.HALF_MAX):
					exp = expo + 14 if mant != 0 else 0
					man = int( mant * 2**11 )
					fp0 = (sign << 7) | ((exp & 0x1F) << 2) | ((man & 0x0300) >> 8)
					fp1 = (man & 0x00FF)
					bytelst = [fp1, fp0] if _FP.output.endswith('le') else [fp0, fp1]
					CG.store( 'bytes', bytearray(bytelst) )

			# 8-bit exponent, 1-bit sign, 31-bit mantissa
			case 'esm4'|'esm4-be'|'esm4-le':
				if valu == 0 or UTIL.inrange(abs(valu), _FP.ESM4_MIN, _FP.ESM4_MAX):
					exp = expo + 128 if mant != 0 else 0
					man = int( mant * 2**32 )
					fp0 = ((man & 0x7F000000) >> 24) | (sign << 7)
					fp1 = (man & 0x00FF0000) >> 16
					fp2 = (man & 0x0000FF00) >>  8
					fp3 = (man & 0x000000FF)
					bytelst= [fp3, fp2, fp1, fp0, exp] if _FP.output.endswith('le') else [exp, fp0, fp1, fp2, fp3]
					CG.store( 'bytes', bytearray(bytelst) )

			# oops !
			case _:
				UM.noway( _FP.output )



