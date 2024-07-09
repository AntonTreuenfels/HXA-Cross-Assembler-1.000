# Regress One - compare output of one set of HXA test files to "canonical" version

# (c) 2023 by Anton Treuenfels

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

# first created: 03/15/23
# last revision: 07/08/24

# -----------------------------

import glob
import os
import sys
import filecmp
import subprocess

# -----------------------------

# directory of correct test results
regdir = '.\\test\\regress'
# directory of tests themselves
testdir = '.\\test'
# typical extensions of test result files
exts = ['lst', 'err', 'obj', 'raw', 'hex', 's19', 's28', 's37', 't19', 't28', 't37', 'u19', 'u28', 'u37']
# these extensions are rarely used except for testing purposes
exts.extend( ['ta', '001', '005'] )

def getfiles(path, fatal=False):

	files = glob.glob( path )

	if len(files) < 1 and fatal:
		print( f'No {path} files found' )
		sys.exit( 1 )

	return files

def getcanon(testnum):

	canon = getfiles( f'{regdir}\\test{testnum}*.*' )

	return canon

def getresults(testnum):

	results = []

	for ext in exts:
		files = getfiles( f'{testdir}\\test{testnum}*.{ext}' )
		if len(files) > 0:
			results.extend( files )

	return results

def pairup(canon, results):

	can = {}

	for file in canon:
		path, filename = os.path.split( file )
		can[ filename ] = file

	res = {}

	for file in results:
		path, filename = os.path.split( file )
		if filename in can:
			res[ filename ] = file
		else:
			print( f'{filename} not found in canon (extra)' )

	comp = {}

	for filename in can:
		if filename in res:
			comp[ res[filename] ] = can[ filename ]
		else:
			print( f'{filename} not found in results (missing)' )

	return comp

def compare(pairs):

	ok = True

	def comperr(mesg):
		nonlocal ok

		print( mesg )
		ok = False

	def comptext(rpath, cpath):

		with open(rpath, 'rt') as f:
			rlines = f.readlines()
		with open(cpath, 'rt') as f:
			clines = f.readlines()

		rlen = len( rlines )
		clen = len( clines )

		if rlen < clen:
			comperr( 'Not enough lines in result file' )
		elif rlen > clen:
			comperr( 'Too many lines in result file' )

		for i in range(min(rlen, clen)):
			if rlines[i] != clines[i]:
				# these are in every list and error file header:
				# - variant number
				# - datestamp
				if i in [ 0, 4 ]:
					continue
				tline = clines[ i ].rstrip()
				# is this a datestamp line (much less often) ?
				# - comment marker may not be at left edge if non-default output
				# - year may not be on same line if non-default output
				# - could make it even harder to test, but this is as far as tests go
				if '; ***' in tline and tline.endswith(('2021', '2022', '2023', '2024')):
					continue
				# is this a timing line (under ten seconds) ?
				elif '00:00:' in tline:
					continue
				# a variable stats time ?
				elif 'per second' in tline:
					continue
				# a special case test ?
				elif any( test in cpath for test in ['457c', '526', '528', '542', '550']):
					# datestamp is on two lines (once only) ?
					if '457c' in cpath and i+1 in [9, 10]:
						continue
					# - the actual time$() test
					elif '526' in cpath and i+1 in [35, 36, 41, 42, 44, 61, 65, 66, 96]: 
						continue
					# - time() used ?
					elif '528' in cpath and i+1 in [35, 36, 41, 42, 43, 84]:
						continue
					# - seed() or rnd() used ?
					elif '542' in cpath and i >= 90:
						continue
					# - time$() used ?
					elif '550' in cpath and i+1 in [530, 531, 532, 536, 537, 538, 540, 550, 551, 552, 557, 558, 559, 697, 698]:
						continue
				# a real difference
				else:
					comperr( f'\nMismatch at line {i+1} of {canpath}' )
					comperr( f'\t canon: {clines[i]}' )
					comperr( f'\tresult: {rlines[i]}' )

	def compbin(rpath, cpath):

		with open(rpath, 'rb') as f:
			rbin = f.read()
		with open(cpath, 'rb') as f:
			cbin = f.read()

		rlen = len( rbin )
		clen = len( cbin )

		if rlen < clen:
			comperr( 'Not enough bytes in result' )
		elif rlen > clen:
			comperr( 'Too many bytes in result' )
		elif rbin != cbin:
			comperr( "Binary files are different" )


	for respath in pairs:
		canpath = pairs[ respath ]
		print( f'\nComparing {respath} to {canpath}' )

		ok = True

		# ASCII comparison ?
		if not respath.endswith('obj'):
			comptext( respath, canpath )

		# binary comparison
		else:
			compbin( respath, canpath )
#
		# files do not match ?
		if not ok:
			print( f'\n***\n*** {respath} does not match {canpath}\n***' )

def runtests(files):

	for file in files:
		subprocess.run( ['python', 'hxa.py', file, '-hxa_t', '-q'] )

def dotest(testnum):

	files = getfiles( f'{testdir}\\test{testnum}*.a', True )
	runtests( files )

	canon = getcanon( testnum )

	results = getresults( testnum )

	pairs = pairup( canon, results )

	compare( pairs )

	return 0

if __name__ == '__main__':
	sys.exit( dotest(sys.argv[1]) )