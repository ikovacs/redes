
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from scapy.all import *

class Sniffer(QObject):

	packetCaptured = pyqtSignal(scapy.layers.l2.Ether)
	finished = pyqtSignal()

	def __init__(self, parent=None):
		super(Sniffer, self).__init__(parent)
		self.stopped = True

	def sniff(self):
		self.stopped = False
		sniff(prn=self.gotPacket,stop_filter=self.stopFilter)
		self.finished.emit()

	def gotPacket(self, packet):
		self.packetCaptured.emit(packet)

	def stopFilter(self, packet):
		return self.stopped

	def stop(self):
		self.stopped = True
