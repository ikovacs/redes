
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui_MainWindow import Ui_MainWindow
from Sniffer import Sniffer
from scapy.all import *
from ArpEntropy import ArpEntropy
from EtherEntropy import EtherEntropy
from datetime import datetime

ONE_SECOND = 1000

MILLIS_200 = 200

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
		self.arpPackets = list()
		self.ethPackets = list()
		#
		self.arpEntropies = list()
		self.ethEntropies = list()
		#
		self.sniffer = Sniffer()
		self.sniffer.packetCaptured.connect(self.onPacketCaptured)
		self.thread = QThread()
		self.sniffer.moveToThread(self.thread)
		self.thread.started.connect(self.sniffer.sniff)
		self.sniffer.finished.connect(self.thread.quit)
		self.sniffer.finished.connect(self.onCaptureStop)
		#
		self.packets = 0
		#
		self.maxArpEntropy = [0, -1]
		self.maxEthEntropy = [0, -1]
		#
		self.ethEntropyThread = QThread()
		self.ethEntropy = EtherEntropy()
		self.ethEntropyThread.started.connect(self.ethEntropy.entropy)
		self.ethEntropy.resultReady.connect(self.onEthEntropyReady)
		self.ethEntropy.resultReady.connect(self.ethEntropyThread.quit)
		#
		self.arpEntropyThread = QThread()
		self.arpEntropy = ArpEntropy()
		self.arpEntropyThread.started.connect(self.arpEntropy.entropy)
		self.arpEntropy.resultReady.connect(self.onArpEntropyReady)
		self.arpEntropy.resultReady.connect(self.arpEntropyThread.quit)
		#
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.updateEntropy)
		#
		self.timer2 = QTimer(self)
		self.timer2.timeout.connect(self.updateStatics)
		self.timer2.start(MILLIS_200)
		#
		self.ui.actionSaveCapture.triggered.connect(self.saveCapture)
		self.ui.actionSaveEntropy.triggered.connect(self.saveEntropy)

	def saveCapture(self):
		fileName = QFileDialog.getSaveFileName(self, "Save Capture", QDir.homePath(), "Text File (*.txt)")
		fileName = fileName[0]
		if fileName != "":
			fle = open(fileName, 'w+')
			for packet in self.ethPackets:
				hwsrc = packet[Ether].src
				hwdst = packet[Ether].dst
				etype = str(packet[Ether].type)
				line = '{} {} {} {}\n'.format('eth', hwsrc, hwdst, etype)
				fle.write(line)
			for packet in self.arpPackets:
				psrc = packet[ARP].psrc
				pdst = packet[ARP].pdst
				hwsrc = packet[ARP].hwsrc
				hwdst = packet[ARP].hwdst
				operation = str(packet[ARP].op)
				line = '{} {} {} {} {} {}\n'.format('arp',
					psrc, pdst,
					hwsrc, hwdst, operation)
				fle.write(line)
			fle.close()


	def saveEntropy(self):
		fileName = QFileDialog.getSaveFileName(self, "Save Entropy", QDir.homePath(), "Text File (*.txt)")
		fileName = fileName[0]
		if fileName != "":
			fle = open(fileName, 'w+')
			for i in range(len(self.ethEntropies)):
				line = '{} {} {}\n'.format(i, self.ethEntropies[i], self.arpEntropies[i])
				fle.write(line)
			fle.close()

	def X(self):
		# top 10 ip replies, por logica si una ip manda muchas replies es que tiene muchas request por lo que es muy solicitada, un server?
		# de esa forma podemos destacar ip replies
		pass

	def calcEthernetEntropy(self):
		self.ethEntropy.addAll(self.ethPackets)
		self.ethEntropyThread.start()

	def onEthEntropyReady(self, ans):
		self.ui.ethEntropyLabel.setText('Ethernet: {:.4f}'.format(ans))
		if self.maxEthEntropy[1] < ans:
			now = datetime.strftime(datetime.now(), '%H:%M:%S') #%Y-%m-%d %H:%M:%S
			self.maxEthEntropy = [ now, ans ]
			self.ui.maxEthEntropyLabel.setText(
				'Max: {:.4f} ({})'.format(
					self.maxEthEntropy[1],
					self.maxEthEntropy[0]))
		self.ethEntropies.append(ans)

	def onArpEntropyReady(self, ans):
		self.ui.arpEntropyLabel.setText('ARP: {}'.format(ans))
		if self.maxArpEntropy[1] < ans:
			now = datetime.strftime(datetime.now(), '%H:%M:%S')
			self.maxArpEntropy = [ now, ans ]
			self.ui.maxArpEntropyLabel.setText(
				'Max: {:.4f} ({})'.format(
					self.maxArpEntropy[1],
					self.maxArpEntropy[0]))
		self.arpEntropies.append(ans)

	def calcArpEntropy(self):
		self.arpEntropy.addAll(self.arpPackets)
		self.arpEntropyThread.start()

	def updateEntropy(self):
		self.calcArpEntropy()
		self.calcEthernetEntropy()

	def updateStatics(self):
		self.ui.packetsLabel.setText('Packets: {:d}'.format(self.packets))
		self.ui.ethPacketsLabel.setText('Ethernet Packets: {:d}'.format(len(self.ethPackets)))
		self.ui.arpPacketsLabel.setText('ARP Packets: {:d}'.format(len(self.arpPackets)))

	def onPacketCaptured(self, packet):
		self.packets += 1
		#self.updateStatics()

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