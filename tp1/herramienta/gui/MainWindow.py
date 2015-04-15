
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui_MainWindow import Ui_MainWindow
from Sniffer import Sniffer
from scapy.all import *
from ArpEntropy import ArpEntropy
from EtherEntropy import EtherEntropy
from datetime import datetime

ONE_SECOND = 1000

class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		#
		self.ui.actionInterval.triggered.connect(self.onCaptureInterval)
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
		self.maxArpEntropy = [0, -1]
		self.maxEthEntropy = [0, -1]

	def saveCapture(self):
		pass

	def X(self):
		# top 10 ip requests
		pass

	def calcEthernetEntropy(self):
		ent = EtherEntropy()
		ent.addAll(self.ethPackets)
		ans = ent.entropy()
		self.ui.ethEntropyLabel.setText('Ethernet: {:.4f}'.format(ans))
		if self.maxEthEntropy[1] < ans:
			now = datetime.strftime(datetime.now(), '%H:%M:%S') #%Y-%m-%d %H:%M:%S
			self.maxEthEntropy = [ now, ans ]
			self.ui.maxEthEntropyLabel.setText(
				'Max: {:.4f} ({})'.format(
					self.maxEthEntropy[1],
					self.maxEthEntropy[0]))

	def calcArpEntropy(self):
		ent = ArpEntropy()
		ent.addAll(self.arpPackets)
		ans = ent.entropy()
		self.ui.arpEntropyLabel.setText('ARP: {}'.format(ans))

		if self.maxArpEntropy[1] < ans:
			now = datetime.strftime(datetime.now(), '%H:%M:%S')
			self.maxArpEntropy = [ now, ans ]
			self.ui.maxArpEntropyLabel.setText(
				'Max: {:.4f} ({})'.format(
					self.maxArpEntropy[1],
					self.maxArpEntropy[0]))

	def updateEntropy(self):
		self.calcArpEntropy() # si son muchos paquetes tirar en un thread, no hay que cargar mucho el UI Thread (supongo)
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

	def onCaptureInterval(self):
		minutes, ok = QInputDialog.getInt(self, "Capture", "Minutes")
		if ok:
			self.sniffer.setTimeout(minutes * 60)
			self.onCaptureStart()

	def onCaptureStart(self):
		self.ui.actionInterval.setEnabled(False)
		self.ui.actionStart.setEnabled(False)
		self.ui.actionStop.setEnabled(True)
		self.thread.start()
		self.timer.start(ONE_SECOND)

	def onCaptureStop(self):
		self.ui.actionInterval.setEnabled(True)
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