#!/usr/bin/env python
import re
import sys
import time
import os
import optparse

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

OB_EXPECTED  = 61
JAVA_EXPECTED = 258

#MCM_EXPECTED = 249
X86_EXPECTED = 987 + OB_EXPECTED + JAVA_EXPECTED
#COM_EXPECTED = 220
PPC_EXPECTED = 1117 + OB_EXPECTED + JAVA_EXPECTED
#LIB_EXPECTED = 500



CPU = os.getenv('I_CPU')

if CPU == 'x86':
    TOTAL_EXPECTED = X86_EXPECTED
else:
    TOTAL_EXPECTED = PPC_EXPECTED


class error():
    def __init__ (self, err_string):
        self.err_string = err_string

def run_cmd(command):
    p = os.popen(command)
    s = p.readlines()
    p.close()
    return s

class ProgressBar(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # in ms
        self.TICK = 10000

        #self.setGeometry(0, 300, 250, 250)
        self.setWindowTitle('Build Progress ' + os.getcwd())

        self.title = QtGui.QLabel(CPU)
        self.bar = QtGui.QProgressBar(self)

        #self.title_ppc = QtGui.QLabel('ppc')
        #self.ppc = QtGui.QProgressBar(self)

        '''
        self.title_mcm = QtGui.QLabel('mcm')
        self.mcm = QtGui.QProgressBar(self)

        self.title_com = QtGui.QLabel('com')
        self.com = QtGui.QProgressBar(self)

        self.title_lib = QtGui.QLabel('lib')
        self.lib = QtGui.QProgressBar(self)
        '''

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.title, 1, 0)
        grid.addWidget(self.bar, 1, 1)

        #grid.addWidget(self.title_ppc, 2, 0)
        #grid.addWidget(self.ppc, 2, 1)

        '''
        grid.addWidget(self.title_mcm, 3, 0)
        grid.addWidget(self.mcm, 3, 1)

        grid.addWidget(self.title_com, 4, 0)
        grid.addWidget(self.com, 4, 1)

        grid.addWidget(self.title_lib, 5, 0)
        grid.addWidget(self.lib, 5, 1)
        '''

        self.setLayout(grid)
        #self.resize(250, 100)

        self.timer = QtCore.QBasicTimer()
        self.timer.start(self.TICK, self)

        self.timerEvent(self)

    def timerEvent(self, event):
        obcount = run_cmd('grep Leaving parob.log | wc -l')[0].strip()
        build_count = run_cmd('grep Leaving parbuild.' + CPU + '.log | wc -l')[0].strip()
        java_count = run_cmd('grep javac parbuild.' + CPU + '.log | wc -l')[0].strip()
        '''
        mcm_count = run_cmd('grep Leaving mcm/mcm.log | wc -l')[0].strip()
        com_count = run_cmd('grep Leaving component/com.log | wc -l')[0].strip()
        lib_count = run_cmd('grep Leaving lib-x86.log | wc -l')[0].strip()
        '''

        #print '\rmcm: %s/%d x86: %s/%d com: %s/%d ppc: %s/%d        ' % (mcm_count, MCM_EXPECTED, build_count,
        #                  X86_EXPECTED, com_count, COM_EXPECTED, ppc_count, PPC_EXPECTED),
        #sys.stdout.flush()

        self.bar.setValue(((int(build_count) + int(obcount) + int(java_count)) * 100) / TOTAL_EXPECTED)
        #self.ppc.setValue((int(ppc_count) + int(obcount) * 100)/ PPC_EXPECTED)
        '''
        self.mcm.setValue((int(mcm_count) * 100)/ MCM_EXPECTED)
        self.com.setValue((int(com_count) * 100)/ COM_EXPECTED)
        self.lib.setValue((int(lib_count) * 100)/ LIB_EXPECTED)
        '''


app = QtGui.QApplication(sys.argv)
icon = ProgressBar()
icon.show()
sys.exit(app.exec_())




