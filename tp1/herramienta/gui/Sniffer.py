
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from scapy.all import *

class Sniffer(QObject):

	packetCaptured = pyqtSignal(scapy.layers.l2.Ether)
	finished = pyqtSignal()

	def __init__(self, parent=None):
		super(Sniffer, self).__init__(parent)
		self.stopped = True
		self.timeout = None
		self.packets = None
		self.store = 0

	def setTimeout(self, seconds):
		self.timeout = seconds

	def setStorePackets(self, store):
		if store:
			self.store = 1
		else:
			self.store = 0

	def getCapturedPackets(self):
		return self.packets

	def sniff(self):
		self.stopped = False
		self.packets = sniff(store=self.store, prn=self.gotPacket,stop_filter=self.stopFilter, timeout=self.timeout)
		self.stopped = True # Stopped
		self.timeout = None # Restore
		self.finished.emit()

	def gotPacket(self, packet):
		self.packetCaptured.emit(packet)

	def stopFilter(self, packet):
		return self.stopped

	def stop(self):
		self.stopped = True
