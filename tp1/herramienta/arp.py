#!/usr/bin/env python2

from scapy.all import *
from numpy import *

true = True
false = False

TYPE_ARP = 0x806
ARP_REQUEST = 1
ARP_REPLY = 2

eth_count = 0
arp_count = 0

eth = dict()
arp = dict()

def entropy():
	global eth
	entropy = 0
	for key in eth:
		p = (float(eth[key]) / float(eth_count))
		entropy += p * -log2(p)
	return entropy

def arp_entropy():
	global arp
	entropy = 0
	for key in arp:
		p = (float(arp[key]) / float(arp_count))
		entropy += p * -log2(p)
	return entropy

def packet_captured(packet):
	global eth, arp, eth_count, arp_count

	eth_count += 1

	eth_hw_src = packet[Ether].src
	eth_hw_dst = packet[Ether].dst
	eth_type = packet[Ether].type
	
	if eth_hw_src not in eth:
		eth[eth_hw_src] = 0
	else:
		eth[eth_hw_src] += 1

	if eth_type == TYPE_ARP:
		arp_count += 1
		arp_ip_src = packet[ARP].psrc
		arp_ip_dst = packet[ARP].pdst
		arp_hw_src = packet[ARP].hwsrc
		arp_hw_dst = packet[ARP].hwdst
		arp_type = packet[ARP].op

		if arp_ip_src not in arp:
			arp[arp_ip_src] = 0
		else:
			arp[arp_ip_src] += 1

	arp_ent = arp_entropy() if arp_count > 0 else -1.0

	print 'eth: {} arp: {}'.format(entropy(), arp_ent)

sniff(filter='', prn=packet_captured)
