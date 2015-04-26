#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sys import stdin
from matplotlib.pyplot import *
import matplotlib.pyplot as plt

# entropía (eth/arp) vs tiempo
ax = plt.subplot(111)
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
#titulo más arriba
figure_title = "Entropia del modelo respecto al tiempo transcurrido"
plt.text(0.5, 1.04, figure_title,
         horizontalalignment='center',
         fontsize=20,
         transform = ax.transAxes)

xlabel(u"Segundos")
ylabel(u"Entropía")
plot(x_seconds, y_entropyEth, label=u"Modelo Ethernet")
plot(x_seconds, y_entropyArp, label=u"Modelo ARP")

#Leyenda arriba
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True)

show()
