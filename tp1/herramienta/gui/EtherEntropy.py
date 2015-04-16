
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from scapy.all import *
from math import log

ARP_REQUEST = 1
ARP_REPLY = 2

RLY = 0
REQ = 1

class EtherEntropy(QObject):

	resultReady = pyqtSignal(float)

	def __init__(self, parent=None):
		super(EtherEntropy, self).__init__(parent)
		self.ethPackets = dict()
		self.ethPacketsCount = 0

	def clean(self):
		self.ethPackets = dict()

	def addAll(self, packets):
		self.ethPacketsCount += len(packets)
		for packet in packets:
			self.add(packet)

	def add(self, packet):
		self.ethPacketsCount += 1
		hwsrc = packet[Ether].src
		hwdst = packet[Ether].dst
		etype = str(packet[Ether].type)
		key = ''.join([hwsrc,hwdst,etype])
		if key not in self.ethPackets:
			self.ethPackets[key] = 1
		else:
			self.ethPackets[key] += 1

	def entropy(self):
		entropy = .0
		for key in self.ethPackets:
			s = self.ethPackets[key]
			p = (float(s) / float(self.ethPacketsCount))
			entropy += p * -(log(p)/log(2))
		self.resultReady.emit(entropy)
		return entropy
