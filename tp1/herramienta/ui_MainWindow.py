# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(621, 438)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.deviceBox = QtWidgets.QComboBox(self.centralwidget)
        self.deviceBox.setObjectName("deviceBox")
        self.horizontalLayout.addWidget(self.deviceBox)
        self.filterEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.filterEdit.setObjectName("filterEdit")
        self.horizontalLayout.addWidget(self.filterEdit)
        self.captureButton = QtWidgets.QPushButton(self.centralwidget)
        self.captureButton.setCheckable(True)
        self.captureButton.setObjectName("captureButton")
        self.horizontalLayout.addWidget(self.captureButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.packetList = QtWidgets.QListWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.packetList.setFont(font)
        self.packetList.setObjectName("packetList")
        self.verticalLayout.addWidget(self.packetList)
        self.packetCountLabel = QtWidgets.QLabel(self.centralwidget)
        self.packetCountLabel.setObjectName("packetCountLabel")
        self.verticalLayout.addWidget(self.packetCountLabel)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 621, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ARP Sniffer"))
        self.filterEdit.setPlaceholderText(_translate("MainWindow", "Filter Expression"))
        self.captureButton.setText(_translate("MainWindow", "Capture"))
        self.packetCountLabel.setText(_translate("MainWindow", "packets: 0"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

