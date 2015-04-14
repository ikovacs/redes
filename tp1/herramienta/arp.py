#!/usr/bin/env python2

from scapy.all import *
from math import log

true = True
false = False

TYPE_ARP = 0x806
ARP_REQUEST = 1
ARP_REPLY = 2

RLY = 0
REQ = 1

eth_count = 0
arp_count = 0

eth = dict()
arp = dict()
arp2 = dict()

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

def arp_entropy():
	global arp, arp_count
	entropy = .0
	for psrc in arp:
		for pdst in arp[psrc]:
			c = arp[psrc][pdst][RLY]
			if c > 0:
				p = (float(c) / float(arp_count))
				entropy += p * -(log(p)/log(2))

			c = arp[psrc][pdst][REQ]
			if c > 0:
				p = (float(c) / float(arp_count))
				entropy += p * -(log(p)/log(2))

	return entropy

def eth_packet(packet):
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

def arp_packet(packet):
	global arp, arp_count

	arp_count += 1

	psrc = packet[ARP].psrc
	pdst = packet[ARP].pdst
	request = true if packet[ARP].op == ARP_REQUEST else false

	if psrc not in arp:
		arp[psrc] = dict()

	if pdst not in arp[psrc]:
		arp[psrc][pdst] = [0, 0]

	if request:
		arp[psrc][pdst][REQ] += 1
	else:
		arp[psrc][pdst][RLY] += 1

	arp_ent = arp_entropy()

	print 'ARP Entropy: {}'.format(arp_ent)


def packet_captured(packet):
	try:
		eth_packet(packet)
		if packet[Ether].type == TYPE_ARP:
			arp_packet(packet)
	except Exception, e:
		print e

sniff(filter='', prn=packet_captured)
