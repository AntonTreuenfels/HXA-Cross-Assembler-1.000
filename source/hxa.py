# Hobby Cross-Assembler (HXA) V1.200 - Top Level Executive

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

# first created: 01/18/03		(in Thompson AWK 4.0)
# last revision: 09/17/24

# preferred public function prefix: none (other modules cannot call this module)
# - it is only imported as part of testing a "cpu_" module

# -----------------------------
import sys
# other HXA modules
import hxa_pseudo as PSOP
import hxa_macro as MAC
import hxa_usermesg as UM
import hxa_codegen as CG
import hxa_symbol as SYM
import hxa_progctr as PC
import hxa_strings as STR
import hxa_float as FP
import hxa_source as SRC
import hxa_file as OS
import hxa_misc as UTIL
# -----------------------------

# -----------------------------
# version IDs
# -----------------------------

# one decimal digit per nybble
# - lowest three nybbles are for minor version numbers and bug fix indicators
# - and no, we're not likely to get 99,999 major version numbers :-)
# - HXA versions implemented in TAWK are all less than '1.00'

verNum = 0x00001200
verStr = '1.200'

# pre-defined symbols

predefines = [
	( '__HXA__', True ),
	( '__VER__', verNum ),
	( '__VER__$', f'HXA v{verStr}' ),
]

# -----------------------------

def checkargs():
	''' check command line '''
	# python hxa.py filename -cpuhandler [-q] [-h]

	def  bailout(exitcode=4, msgndx=None, msgval=None):
		'''show help message and quit'''
		if msgndx is not None:
			UM.newline()
			UM.firestop( msgndx, msgval )

		UM.useage()
		sys.exit( exitcode )

	srcfile = handler = None
	# don't try to handle more than three arguments
	for i in range(1, min(len(sys.argv), 4)):
		arg = sys.argv[ i ].lower()

		# is it a filename ?
		if not arg.startswith(('-', '--', '/')):
			if srcfile is None:
			# this is an assumption, but a reasonable one
				srcfile = arg
			else:
				bailout( 4, "UniqVal", srcfile )

		# is it a cpu handler we know about ?
		elif arg.startswith('-hxa'):
			if handler is None:
				handler = arg[1:]
			else:
				bailout( 4, "UniqVal", handler )

		# is it a "help" flag ?
		elif arg in ['-h', '/?', '--help']:
			bailout( 0 )

		# is it a "quiet" flag ?
		elif arg in ['-q', '--quiet']:
			UM.quiet( True )

		# something we don't recognize
		else:
			bailout( 4, "BadToken", arg )

	# did we find a filename and a cpu handler ?
	if srcfile is not None and handler is not None:
		return ( srcfile, handler )
	# no...
	else:
		bailout()

def doinits(sourcefile, handler):
	''' run module initializations '''
	# since we're not sure when the various modules
	# run their '__init__()' functions, and even if we
	# did know the order it could change in the future,
	# and that some intializations we want to do depend
	# on them having all having been run...
	# - we wait until now, when we know they've all been run
	CG.init( handler )
	# next two methods need CG.init() to run first
	UM.init( verNum, verStr )
	SYM.addreserve( predefines )
	return( OS.init(sourcefile) )

# -----------------------------

def beginpass(this):
	'''start an assembler pass'''
	UM.newline()
	OS.errwrite( UM.info(f'Beg{this}') )
	UTIL.dostarttimer( None, f'__Pass{this}' )

def endpass(this):
	'''finish an assembly pass'''
	UTIL.dostoptimer( None, f'__Pass{this}' )
	UM.info( f'End{this}' )
	UM.quitonerr()

# -----------------------------

def domacro(label, name, exprfield):
	'''handle user-defined macro '''
	if PSOP.taking():
		SYM.here( label )
		MAC.invoke( name, exprfield )

def doop(label, mnemonic, exprfield):
	'''handle CPU mnemonic'''
	if PSOP.taking():
		ok, exprlist = STR.splitfield( exprfield )
		if ok:
			SYM.here( label )
			ok, key = CG.doop( mnemonic, exprlist )
			if not ok:
				UM.error( key )

def dolabel(label):
	'''handle user-defined label'''
	if PSOP.taking():
		SYM.here( label, True )

# -----------------------------

def doline(text):
	''' process one source line '''
# accepted line patterns:

# label
# label     opcode
# label     opcode      expression(s)
# label     pseudo-op
# label     pseudo-op   expression(s)
# label     macro
# label     macro       arg(s)

#           opcode
#           opcode      expression(s)
#           pseudo-op
#           pseudo-op   expression(s)
#           macro
#           macro       arg(s)

	def _split(this):
		tokens = this.split( None, 1 )		# 1 or 2 tokens
		return ( tokens[0], tokens[1] if len(tokens) > 1 else None )

	token0, token1 = _split( text )

	# check if first token is a psop...
	if PSOP.ispseudo(token0):
		PSOP.dopseudo( None, token0, token1 )

	# ... or a macro...
	elif MAC.ismacro(token0):
		domacro( None, token0, token1 )

	# ...or a CPU mnemonic...
	elif CG.isop(token0):
		doop( None, token0, token1 )

	# ...or a label
	elif SYM.islabel(token0):

		# a label all by itself ?
		if token1 is None:
			dolabel( token0 )

		# no, there's more...
		else:
			token1, token2 = _split( token1 )

			# check if second token is a psop...
			if PSOP.ispseudo(token1):
				PSOP.dopseudo( token0, token1, token2 )

			# ... or a macro...
			elif MAC.ismacro(token1):
				domacro( token0, token1, token2 )

			# ...or a CPU mnemonic...
			elif CG.isop(token1):
				doop( token0, token1, token2 )

			# second token is not a psop, macro or mnemonic
			else:
				UM.error( 'NeedOpcode', token1 )

	# first token is not a label, psop, macro or mnemonic
	else:
		UM.error( 'NeedToken', token0 )

# -----------------------------
# Setup
# -----------------------------

def setup():
	sourcefile, handler = checkargs()

	rootfile = doinits( sourcefile, handler )

	UM.info('Version')

	return rootfile

# -----------------------------
# Pass One
# -----------------------------

def passone(rootfile):
	beginpass( 'One' )

	# push root file on file stack
	OS.pushfile( rootfile, 0, 0 )

	# while file stack not empty...
	while OS.popfile():

		# while a file has not been completely read...
		ok, text = SRC.nextline()
		while ok:
			doline( text )
			ok, text = SRC.nextline()

	MAC.endsource()
	UTIL.endsource()
	endpass( 'One' )

# -----------------------------
# Pass Two
# -----------------------------

def passtwo():
	beginpass( 'Two' )

	if PC.makeabsolute():
		SYM.makeabsolute()
		CG.resolve()

	endpass( 'Two' )

# -----------------------------
# Write Files
# -----------------------------

def writefiles():

	# no list or object files if already have error(s)
	# - but even if none now, errors can happen during file writing...
	if UM.geterrcode() < 2:
		# listing
		SRC.list()

		# object
		CG.putobject()

	# error
	UM.showerrcnt()
	OS.writeerr()

# -----------------------------
# Main
# -----------------------------

def main():

	root = setup()
	passone( root )
	passtwo()
	writefiles()

	# 0 -> okay, 1..7 -> warning/error of some kind
	sys.exit( UM.geterrcode() )

# -------------------------------

if __name__  == "__main__":
	main()