#!/usr/bin/env python2

from PyQt5.QtCore import QObject, pyqtSignal
from scapy.all import *

ARP_REPLY = 2
ARP_REQUEST = 1
ARP_TYPE = 0x806

class Sniffer(QObject):

	packetCaptured = pyqtSignal(scapy.layers.l2.Ether)

	def __init__(self, parent=None):
		super(Sniffer, self).__init__(parent)

	def sniff(self):
		sniff(filter='', prn=self.packetReceived) # All Ehternet?

	def packetReceived(self, packet):
		self.packetCaptured.emit(packet)
