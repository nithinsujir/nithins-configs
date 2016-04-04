#!/usr/bin/python
import mmap
NVDIMM_DEV = '/dev/agigaram1'
NVDIMM_SIZE = 1024 * 1024 * 1024

PATTERN1 = '1'
PATTERN2 = '2'
PATTERN3 = '3'

f = open(NVDIMM_DEV, 'r+b')
mm = mmap.mmap(f.fileno(), NVDIMM_SIZE,  flags = mmap.MAP_SHARED, prot = mmap.PROT_READ | mmap.PROT_WRITE)

def write_pattern(pat):
    mm.seek(0)

    for i in xrange((NVDIMM_SIZE / len(pat)) -  len(pat)):
        mm.write(pat)

pat1 = PATTERN1
pat2 = PATTERN2
pat3 = PATTERN3

# Bump the strings upto 4k
for i in xrange(12):
    pat1 = pat1 * 2
    pat2 = pat2 * 2
    pat3 = pat3 * 2

write_pattern(pat1)

