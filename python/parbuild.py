#!/usr/bin/env python
import genparmake

os.system('make -C mcm/Log')

# Generate the ob makefile
os.system('../scripts/genparmake.py')

