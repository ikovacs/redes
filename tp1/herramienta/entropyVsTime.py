#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sys import stdin
from matplotlib.pyplot import *

# entropía (eth/arp) vs tiempo

x_seconds = list()
y_entropyEth = list()
y_entropyArp = list()

for line in stdin:
	# segundos_entropíaEthernet_entropíaARP
	cols = line.strip().split()
	x_seconds.append(float(cols[0]))
	y_entropyEth.append(float(cols[1]))
	y_entropyArp.append(float(cols[2]))

figure(1)
title(u"Entropía VS Tiempo")
xlabel(u"Segundos")
ylabel(u"Entropía")
plot(x_seconds, y_entropyEth, label=u"Ethernet")
plot(x_seconds, y_entropyArp, label=u"ARP")
legend(loc='lower right')
show()
