# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/MainWindow.ui'
#
# Created: Fri Apr 17 23:24:53 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(390, 309)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.staticsBox = QtGui.QGroupBox(self.centralwidget)
        self.staticsBox.setFlat(False)
        self.staticsBox.setObjectName(_fromUtf8("staticsBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.staticsBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.packetsLabel = QtGui.QLabel(self.staticsBox)
        self.packetsLabel.setObjectName(_fromUtf8("packetsLabel"))
        self.verticalLayout.addWidget(self.packetsLabel)
        self.ethPacketsLabel = QtGui.QLabel(self.staticsBox)
        self.ethPacketsLabel.setObjectName(_fromUtf8("ethPacketsLabel"))
        self.verticalLayout.addWidget(self.ethPacketsLabel)
        self.arpPacketsLabel = QtGui.QLabel(self.staticsBox)
        self.arpPacketsLabel.setObjectName(_fromUtf8("arpPacketsLabel"))
        self.verticalLayout.addWidget(self.arpPacketsLabel)
        self.verticalLayout_4.addWidget(self.staticsBox)
        self.entropyBox = QtGui.QGroupBox(self.centralwidget)
        self.entropyBox.setFlat(False)
        self.entropyBox.setObjectName(_fromUtf8("entropyBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.entropyBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.ethEntropyLabel = QtGui.QLabel(self.entropyBox)
        self.ethEntropyLabel.setObjectName(_fromUtf8("ethEntropyLabel"))
        self.verticalLayout_3.addWidget(self.ethEntropyLabel)
        self.arpEntropyLabel = QtGui.QLabel(self.entropyBox)
        self.arpEntropyLabel.setObjectName(_fromUtf8("arpEntropyLabel"))
        self.verticalLayout_3.addWidget(self.arpEntropyLabel)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.maxEthEntropyLabel = QtGui.QLabel(self.entropyBox)
        self.maxEthEntropyLabel.setObjectName(_fromUtf8("maxEthEntropyLabel"))
        self.verticalLayout_2.addWidget(self.maxEthEntropyLabel)
        self.maxArpEntropyLabel = QtGui.QLabel(self.entropyBox)
        self.maxArpEntropyLabel.setObjectName(_fromUtf8("maxArpEntropyLabel"))
        self.verticalLayout_2.addWidget(self.maxArpEntropyLabel)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addWidget(self.entropyBox)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout_4.addWidget(self.progressBar)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 390, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuCatuper = QtGui.QMenu(self.menubar)
        self.menuCatuper.setObjectName(_fromUtf8("menuCatuper"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionStart = QtGui.QAction(MainWindow)
        self.actionStart.setObjectName(_fromUtf8("actionStart"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionStop = QtGui.QAction(MainWindow)
        self.actionStop.setEnabled(False)
        self.actionStop.setObjectName(_fromUtf8("actionStop"))
        self.actionReset = QtGui.QAction(MainWindow)
        self.actionReset.setObjectName(_fromUtf8("actionReset"))
        self.actionInterval = QtGui.QAction(MainWindow)
        self.actionInterval.setObjectName(_fromUtf8("actionInterval"))
        self.actionSaveCapture = QtGui.QAction(MainWindow)
        self.actionSaveCapture.setObjectName(_fromUtf8("actionSaveCapture"))
        self.actionSaveEntropy = QtGui.QAction(MainWindow)
        self.actionSaveEntropy.setObjectName(_fromUtf8("actionSaveEntropy"))
        self.menuFile.addAction(self.actionSaveCapture)
        self.menuFile.addAction(self.actionSaveEntropy)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuCatuper.addAction(self.actionInterval)
        self.menuCatuper.addAction(self.actionStart)
        self.menuCatuper.addAction(self.actionStop)
        self.menuCatuper.addAction(self.actionReset)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCatuper.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Sniffer", None))
        self.staticsBox.setTitle(_translate("MainWindow", "Statics", None))
        self.packetsLabel.setText(_translate("MainWindow", "Packets: 0", None))
        self.ethPacketsLabel.setText(_translate("MainWindow", "Ethernet Packets: 0", None))
        self.arpPacketsLabel.setText(_translate("MainWindow", "ARP Packets: 0", None))
        self.entropyBox.setTitle(_translate("MainWindow", "Entropy", None))
        self.ethEntropyLabel.setText(_translate("MainWindow", "Ethernet: -1", None))
        self.arpEntropyLabel.setText(_translate("MainWindow", "ARP: -1", None))
        self.maxEthEntropyLabel.setText(_translate("MainWindow", "Max: undef", None))
        self.maxArpEntropyLabel.setText(_translate("MainWindow", "Max: undef", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuCatuper.setTitle(_translate("MainWindow", "Capture", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))
        self.actionStart.setText(_translate("MainWindow", "Start", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionStop.setText(_translate("MainWindow", "Stop", None))
        self.actionReset.setText(_translate("MainWindow", "Reset", None))
        self.actionInterval.setText(_translate("MainWindow", "Interval", None))
        self.actionSaveCapture.setText(_translate("MainWindow", "Save Capture", None))
        self.actionSaveEntropy.setText(_translate("MainWindow", "Save Entropy", None))

