#!/usr/bin/python

import os
import optparse

parser = optparse.OptionParser()
parser.add_option('', '--min', dest='min_npiv', help='min npiv')
parser.add_option('', '--max', dest='max_npiv', help='max npiv')
parser.add_option('', '--sys', dest='sys', help='sys path')

(opts, args) = parser.parse_args()

if not opts.min_npiv:
	raise BaseException('min npiv needed')

if not opts.max_npiv:
	opts.max_npiv = int(opts.min_npiv) + 1

if not opts.sys:
	raise BaseException('sys path needed')

for i in xrange(int(opts.min_npiv), int(opts.max_npiv)):
	cmd = 'echo "20000000000000%02x:10000000000000%02x" > %s' % (i, i, opts.sys) 

	os.system(cmd)

