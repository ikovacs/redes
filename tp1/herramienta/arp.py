#!/usr/bin/env python2

from scapy.all import *
from math import log

true = True
false = False

TYPE_ARP = 0x806
ARP_REQUEST = 1
ARP_REPLY = 2

eth_count = 0
arp_count = 0

eth = dict()
arp = dict()

def eth_entropy():
	global eth, eth_count
	entropy = .0

	if eth_count > 0:
		for hwsrc in eth:
			for hwdst in eth[hwsrc]:
				for etype in eth[hwsrc][hwdst]:
					c = eth[hwsrc][hwdst][etype]
					p = (float(c) / float(eth_count))
					entropy += p * -(log(p)/log(2))
	return entropy

def packet_captured(packet):
	global eth, eth_count

	eth_count += 1
	
	hwsrc = packet[Ether].src
	hwdst = packet[Ether].dst
	etype = packet[Ether].type 
	
	if hwsrc not in eth:
		eth[hwsrc] = dict()

	if hwdst not in eth[hwsrc]:
		eth[hwsrc][hwdst] = dict()

	if etype not in eth[hwsrc][hwdst]:
		eth[hwsrc][hwdst][etype] = 1
	else:
		eth[hwsrc][hwdst][etype] += 1

	eth_ent = eth_entropy()

	print 'Ethernet Entropy: {}'.format(eth_ent)
		
		

sniff(filter='', prn=packet_captured)
