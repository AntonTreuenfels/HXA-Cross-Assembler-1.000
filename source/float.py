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
# last revision: 09/17/24

# preferred public function prefix: FP

# -----------------------------
import math
# other HXA modules
import hxa_pseudo as PSOP
import hxa_usermesg as UM
# -----------------------------

def _accept(this):
	'''collect a finite floating point value'''
	try:
		val = float( this )
	except ValueError:
		UM.error( "NeedFloat", this )
	except OverflowError:
		UM.error( "BadRange", this )
	# some floating point exception we haven't considered yet (just in case)
	# - 'TypeError' may be the only one left, but that seems mostly for blank arguments to float()
	except Exception as ex:
		template = "An exception of type {0} occurred. Arguments:\n{1!r}"
		message = template.format(type(ex).__name__, ex.args)
		UM.error( "BadToken", message )
	# we have something Python considers a float value
	else:
		# is it something other than '+inf', '-inf', or 'nan' ?
		if math.isfinite(val):
			return val
		else:
			UM.error( "NeedFloat", val )

	return None

# -----------------------------

def driver():
	
	tests = [
		1,
		3.1415,
		1e9,
		"1",
		"  3.1415  ",
		"  1E9  ",
		"abc",
		"Inf",
		"+Inf",
		"-Inf",
		"Infinity",
		"NaN",
		2**2000,
	]
	
	for t in tests:
		print( v if (v := _accept(t)) is not None else f'{t} provoked an error' )

if __name__ == "__main__":
	driver()
