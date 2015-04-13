#!/usr/bin/env python2

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow
from ui_MainWindow import *
from Sniffer import *

class MainWindow(QMainWindow):

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.captureButton.toggled.connect(self.onCaptureButtonToggled)
		self.sniffing = False
		self.packetCount = 0
		self.arpPackets = 0
		self.arpReplies = 0
		self.arpRequests = 0

	def onCaptureButtonToggled(self, checked):
		if self.sniffing != checked:
			if checked:
				self.sniffing = True
				self.sniffer = Sniffer()
				self.snifferThread = QThread()
				self.sniffer.moveToThread(self.snifferThread)
				self.sniffer.packetCaptured.connect(self.onPacketCaptured)
				self.snifferThread.started.connect(self.sniffer.sniff)
				self.snifferThread.start()
			else:
				self.sniffing = False
				self.sniffer.stop()

	def onPacketCaptured(self, packet):
		
		self.packetCount += 1
		
		if packet[Ether].type == ARP_TYPE:
			self.arpPackets += 1
			if packet[ARP].op == ARP_REQUEST:
				arpType = 'Request'
				self.arpRequests += 1
			else:
				arpType = 'Reply'
				self.arpReplies += 1

			self.ui.packetList.addItem('{:^7s} {:^17s} {:^16s} {:^17s} {:^16s}'.format(
				arpType,
				packet[ARP].hwsrc,
				packet[ARP].psrc,
				packet[ARP].hwdst,
				packet[ARP].pdst))

		self.ui.packetCountLabel.setText(
				'{:d} packets, {:d} ARP packets, {:d} ARP Requests {:d} ARP Replies '.format(
					self.packetCount,
					self.arpPackets,
					self.arpRequests,
					self.arpReplies))

	def entropy(self):
		pass
		# entropy = sum( P(a) * I(a) )
