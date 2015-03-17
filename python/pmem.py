#!/usr/bin/env python
import os, mmap
import array
import sys
import curses.ascii

PAGE_MASK = ~(mmap.PAGESIZE - 1)
addr = int(sys.argv[1], 16)

try:
	len = int(sys.argv[2])
except:
	len = 64

mdev = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)

m = mmap.mmap(mdev, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ, offset=addr & PAGE_MASK)
m.seek(addr & ~PAGE_MASK)

s = m.read(len)
#print ord(s[0])
#print ord(s[1])
#print ord(s[2])
#print ord(s[3])

values = array.array('B')
values.fromstring(s)
values.byteswap()

ascii_str = ''
for i in xrange(0, len):
	if not i % 16:
		print ascii_str
		ascii_str = ''
		print "%04d:" % i,

	print "%02x" % values[i],

	if curses.ascii.isprint(values[i]):
		ascii_str = ascii_str + chr(values[i])
	else:
		ascii_str = ascii_str + '.'


m.close()
os.close(mdev)
