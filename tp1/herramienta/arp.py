#!/usr/bin/env python2

import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import *

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()
