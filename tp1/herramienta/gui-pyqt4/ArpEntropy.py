
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from scapy.all import *
from math import log

ARP_REQUEST = 1
ARP_REPLY = 2

RLY = 0
REQ = 1

class ArpEntropy(QObject):

	resultReady = pyqtSignal(float)

	def __init__(self, parent=None):
		super(ArpEntropy, self).__init__(parent)
		self.arpPackets = dict()
		self.arpPacketsCount = 0

	def clean(self):
		self.arpPackets = dict()
		self.arpPacketsCount = 0

	def addAll(self, packets):
		self.arpPacketsCount += len(packets)
		for packet in packets:
			self.add(packet)

	def add(self, packet):
		self.arpPacketsCount += 1
		psrc = packet[ARP].psrc
		pdst = packet[ARP].pdst
		hwsrc = packet[ARP].hwsrc
		hwdst = packet[ARP].hwdst
		operation = str(packet[ARP].op)
		key = ''.join([psrc,hwsrc,pdst,hwdst,operation])

		if key not in self.arpPackets:
			self.arpPackets[key] = 1
		else:
			self.arpPackets[key] += 1

	def entropy(self):
		entropy = .0
		for key in self.arpPackets:
			s = self.arpPackets[key]
			p = (float(s) / float(self.arpPacketsCount))
			entropy += p * -(log(p)/log(2))
		self.resultReady.emit(entropy)
		return entropy
