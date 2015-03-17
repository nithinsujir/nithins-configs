#!/usr/bin/python
from library import telnet
import optparse
import sys


tel = telnet.telnet('ilo2', 'admin', 'pass', '>')
tel.run('cd system1')
tel.run('reset')
