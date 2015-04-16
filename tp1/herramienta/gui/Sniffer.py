
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from scapy.all import *

class Sniffer(QObject):

	packetCaptured = pyqtSignal(Packet)
	finished = pyqtSignal()
	timeout = pyqtSignal()

	def __init__(self, parent=None):
		super(Sniffer, self).__init__(parent)
		self.stopped = True
		self.seconds = None
		self.packets = None
		self.store = 0

	def setTimeout(self, seconds):
		self.seconds = seconds

	def setStorePackets(self, store):
		if store:
			self.store = 1
		else:
			self.store = 0

	def getCapturedPackets(self):
		return self.packets

	def sniff(self):
		self.stopped = False
		self.packets = sniff(store=self.store, prn=self.gotPacket, stop_filter=self.stopFilter, timeout=self.seconds)
		if self.seconds != None:
			self.timeout.emit()
		self.finished.emit()
		self.stopped = True # Stopped
		self.seconds = None # Restore


	def gotPacket(self, packet):
		self.packetCaptured.emit(packet)

	def stopFilter(self, packet):
		return self.stopped

	def stop(self):
		self.stopped = True
