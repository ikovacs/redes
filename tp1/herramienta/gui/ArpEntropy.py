
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from scapy.all import *
from math import log

ARP_REQUEST = 1
ARP_REPLY = 2

RLY = 0
REQ = 1

class ArpEntropy(QObject):

	def __init__(self, parent=None):
		super(ArpEntropy, self).__init__(parent)
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
		request = True if packet[ARP].op == ARP_REQUEST else False

		if psrc not in self.arpPackets:
			self.arpPackets[psrc] = dict()

		if pdst not in self.arpPackets[psrc]:
			self.arpPackets[psrc][pdst] = [0, 0]

		if request:
			self.arpPackets[psrc][pdst][REQ] += 1
		else:
			self.arpPackets[psrc][pdst][RLY] += 1

	def entropy(self):
		entropy = .0
		for psrc in self.arpPackets:
			for pdst in self.arpPackets[psrc]:
				c = self.arpPackets[psrc][pdst][RLY]
				if c > 0:
					p = (float(c) / float(self.arpPacketsCount))
					entropy += p * -(log(p)/log(2))
				c = self.arpPackets[psrc][pdst][REQ]
				if c > 0:
					p = (float(c) / float(self.arpPacketsCount))
					entropy += p * -(log(p)/log(2))
		return entropy
