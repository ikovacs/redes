
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from scapy.all import *
from math import log

ARP_REQUEST = 1
ARP_REPLY = 2

RLY = 0
REQ = 1

class EtherEntropy(QObject):

	def __init__(self, parent=None):
		super(EtherEntropy, self).__init__(parent)
		self.ethPackets = dict()
		self.ethPacketsCount = 0

	def addAll(self, packets):
		self.ethPacketsCount += len(packets)
		for packet in packets:
			self.add(packet)

	def add(self, packet):
		
		self.ethPacketsCount += 1

		hwsrc = packet[Ether].src
		hwdst = packet[Ether].dst
		etype = packet[Ether].type 
		
		if hwsrc not in self.ethPackets:
			self.ethPackets[hwsrc] = dict()

		if hwdst not in self.ethPackets[hwsrc]:
			self.ethPackets[hwsrc][hwdst] = dict()

		if etype not in self.ethPackets[hwsrc][hwdst]:
			self.ethPackets[hwsrc][hwdst][etype] = 1
		else:
			self.ethPackets[hwsrc][hwdst][etype] += 1

	def entropy(self):
		entropy = .0
		if self.ethPacketsCount > 0:
			for hwsrc in self.ethPackets:
				for hwdst in self.ethPackets[hwsrc]:
					for etype in self.ethPackets[hwsrc][hwdst]:
						c = self.ethPackets[hwsrc][hwdst][etype]
						p = (float(c) / float(self.ethPacketsCount))
						entropy += p * -(log(p)/log(2))
		return entropy
