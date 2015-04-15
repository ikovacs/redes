
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui_MainWindow import Ui_MainWindow
from Sniffer import Sniffer
from scapy.all import *
from ArpEntropy import ArpEntropy
from EtherEntropy import EtherEntropy

ONE_SECOND = 1000

class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		#
		self.ui.actionStop.setEnabled(False)
		self.ui.actionStart.triggered.connect(self.onCaptureStart)
		self.ui.actionStop.triggered.connect(self.onCaptureStop)
		self.ui.actionReset.triggered.connect(self.onResetCapture)
		self.ui.actionQuit.triggered.connect(self.close)
		#
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.updateEntropy)
		#
		self.arpPackets = list()
		self.ethPackets = list()
		#
		self.sniffer = Sniffer()
		self.sniffer.packetCaptured.connect(self.onPacketCaptured)
		self.thread = QThread()
		self.sniffer.moveToThread(self.thread)
		self.thread.started.connect(self.sniffer.sniff)
		self.sniffer.finished.connect(self.thread.quit)
		#
		self.packets = 0
		#

	def calcEthernetEntropy(self):
		ent = EtherEntropy()
		ent.addAll(self.ethPackets)
		self.ui.ethEntropyLabel.setText('Ethernet: {:.4f}'.format(ent.entropy()))

	def calcArpEntropy(self):
		ent = ArpEntropy()
		ent.addAll(self.arpPackets)
		self.ui.arpEntropyLabel.setText('ARP: {}'.format(ent.entropy()))

	def updateEntropy(self):
		self.calcArpEntropy() # si son muchos paquetes tirar en un thread
		self.calcEthernetEntropy()

	def updateStatics(self):
		self.ui.packetsLabel.setText('Packets: {:d}'.format(self.packets))
		self.ui.ethPacketsLabel.setText('Ethernet Packets: {:d}'.format(len(self.ethPackets)))
		self.ui.arpPacketsLabel.setText('ARP Packets: {:d}'.format(len(self.arpPackets)))

	def onPacketCaptured(self, packet):
		self.packets += 1
		self.updateStatics()

		if Ether in packet:
			self.processEthernetPacket(packet)
		
		if ARP in packet:
			self.processArpPacket(packet)

	def onCaptureStart(self):
		self.ui.actionStart.setEnabled(False)
		self.ui.actionStop.setEnabled(True)
		self.thread.start()
		self.timer.start(ONE_SECOND)

	def onCaptureStop(self):
		self.ui.actionStart.setEnabled(True)
		self.ui.actionStop.setEnabled(False)
		self.sniffer.stop()
		self.timer.stop()

	def onResetCapture(self):
		self.packets = 0
		self.ethPackets = list()
		self.arpPackets = list()
		self.updateStatics()

	def processEthernetPacket(self, packet):
		self.ethPackets.append(packet) # Por ahora solo guardo el paquete

	def processArpPacket(self, packet):
		self.arpPackets.append(packet) # Por ahora solo guardo el paquete