import os
import re

os.chdir('./mcm/CMog/cmogob')
for filname in os.listdir('.'):
    fil = open(filname, 'r')
    lines = fil.readlines()
    fil.close()

    fil = open(filname, 'w')
    for line in lines:
        if re.search('mOwAtt', line):
            print 'Matched: ' + filname + ' ' + line
            continue

        if re.search('GenerateChangeList', line):
            continue

        fil.write(line)

    fil.close()

