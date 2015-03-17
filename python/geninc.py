#!/usr/bin/python
import struct

def create_file(filename, size_kb):

        f = open(filename,'wb')

        for i in  xrange(size_kb/8):

                f.write(struct.pack('Q',i))

        f.close()

create_file('/tmp/x.bin', 1024)

