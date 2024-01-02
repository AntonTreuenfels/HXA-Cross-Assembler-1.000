# Hobby Cross-Assembler (HXA) V1.00 - Miscellaneous 

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

# source language: Python 3.7.1

# first created: 01/24/03	(in Thompson AWK 4.0)
# last revision: 12/29/23

# preferred public function prefix: UTIL

# -----------------------------
import time
# other HXA modules
import hxa_usermesg as UM
# -----------------------------

# module variables

class MSCvariables(object):

	def __init__(self):

		self.timer = {				# named timers
			# these are also keys in the user message table
#			'__PassOne': None,			# internal: pass one
#			'__PassTwo': None,			# internal: pass two
		}

		self.userstack = []			# user stack

_MSC = MSCvariables()

# -----------------------------

def iformat(val):
	''' format integer value for display '''
	if abs(val) < 256:
		return f'{val}'
	else:
		return f'{val} ({"0x" if val >= 0 else "-0x"}{abs(val):02X})'

# -----------------------------

# default internal limit values

_maxLimit = {
	'maxwarn': 50,		# warning messages
	'maxerr':  25,		# error messages
	'maxdepth': 64,		# block nesting depth
	'maxloop': 2048,	# number of loops
	'maxputback': 128,	# consecutive "putback" lines
	'maxseg': 1023,		# number of segments
	'maxstack': 128,	# user stack depth
}

def checkmax(key, currval):
	''' range check internal limit value '''
	# in general check *after* increasing value of what's being checked
	if currval > _maxLimit[ key ]:
		UM.fatal( key, f'{iformat(currval)} > {iformat(_maxLimit[key])}' )

# -----------------------------
# psop: MAX--- expr
# - 'psop' is also the key to use for checking (and reporting) over limit values
# -----------------------------

def domax(psop, val):
	''' modify default internal limit value '''
	_maxLimit[ psop ] = val

# -----------------------------

def isrunning(name):
	'''is this timer currently running ?'''
	# a start time has been recorded but not a stop time ?
	return len( _MSC.timer[name] ) == 1

def readtimer(name):
	# read timer value (in nanoseconds from epoch)
	if name in _MSC.timer:
		endtime = time.time_ns() if isrunning(name) else _MSC.timer[name][1]
		return endtime - _MSC.timer[ name ][ 0 ]
	else:
		UM.undefined( name )
		return 0

def elapsedtime(nanos):
	# nanoseconds to "HRS":"MIN":SEC:MS"
	millis = nanos // 1e6		# convert to milliseconds (could be zero)
	hrs = mins = secs = 0
	while millis >= 3600000:	# how many hours ?
		hrs += 1
		millis -= 3600000
	while millis >= 60000:		# how many minutes ?
		mins += 1
		millies -= 60000
	while millis >= 1000:		# how many seconds ?
		secs += 1
		millis -= 1000
	return f'{hrs:02}:{mins:02}:{secs:02}:{millis:04}'

# -----------------------------
# psop: SHOWTIMER name
# -----------------------------

def doshowtimer(label, name):
	'''handle SHOWTIMER psop'''
	if name in _MSC.timer:
		UM.doecho( None, UM.eqformat(name, elapsedtime(readtimer(name))) )
	else:
		UM.undefined( name )

# -----------------------------
# psop: STARTTIMER name
# -----------------------------

def dostarttimer(label, name):
	'''handle STARTTIMER psop'''
	if name in _MSC.timer and isrunning(name):
		UM.warn( 'TimerReset' )

	# note current time (in nanoseconds from epoch)
	_MSC.timer[ name ] = [ time.time_ns() ]

# -----------------------------
# psop: STOPTIMER name
# -----------------------------

def dostoptimer(label, name):
	'''handle STOPTIMER psop'''
	if not name in _MSC.timer:
		UM.undefined( name )
	elif isrunning(name):
		_MSC.timer[ name ].append( time.time_ns() )
	else:
		UM.noeffect( name )

# -----------------------------
# User Stack operations
# -----------------------------

def eos():
	'''is user stack empty ?'''
	return len(_MSC.userstack) == 0

def endsource():
	'''end of first pass'''
	if not eos():
		UM.error( "StkNotEmpty", _MSC.userstack.pop() )

def _canpop():
	'''report error if user stack empty'''
	if not eos():
		return True
	else:
		UM.error( "StkEmpty" )
		return False

# -----------------------------
# psop: PUSHS expr
# -----------------------------

def dopushs(label, value):
	'''handle PUSH psop'''
	_MSC.userstack.append( value )
	checkmax( 'maxstack', len(_MSC.userstack) )

def dopop():
	'''return top item on user stack'''
	return _MSC.userstack.pop() if _canpop() else ''

def dopeek(ndx=1):
	'''peek item on user stack at index'''
	return _MSC.userstack[-ndx] if _canpop() and inrange(ndx, 1, len(_MSC.userstack) ) else ''

# -----------------------------

def nullfnc(ignore0=None, ignore1=None, ignore2=None, ignore3=None):
	''' null function with up to four ignored arguments '''

	# when we want to do absolutely nothing...

	pass

# -----------------------------

def maxfields(fields, max):
	''' ignore any excess fields beyond a maximum number '''
	if fields is not None and len(fields) > max:
		ignored = fields[max:]
		while len(ignored):
			UM.ignored( ignored.pop(0) ) 
		fields = fields[:max]

	return fields

# -----------------------------

def sameval(new, existing):
	''' new value must match existing value '''
	if new == existing:
		return True
	else:
		UM.warn( 'UniqVal', existing )
		UM.ignored( new )
		return False

def samename(new, existing):
	''' verify two names match '''
	# can we compare or comparisons match ?
	if ( new is None
		or existing is None
		or new.casefold() == existing.casefold()
	):
		return True
	else:
		# first is what the second should be
		UM.error( 'NeedMatch', existing )
		UM.ignored( new )
		return False

# -----------------------------

def inrange(val, min, max):
	''' range check a value '''
	if val < min:
		UM.error( 'BadRngLo', f'{iformat(val)} < {iformat(min)}' )
	elif val > max:
		UM.error( 'BadRngHi', f'{iformat(val)} > {iformat(max)}' )
	else:
		return True
		
	return False

# -----------------------------
# Listing support
# -----------------------------

def getpasstime(name):

	pname = f'__Pass{name}'
	psecs = readtimer( pname )
	return pname, psecs
