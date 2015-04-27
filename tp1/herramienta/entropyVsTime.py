#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import stdin
from matplotlib.pyplot import *
import matplotlib.pyplot as plt

# entropía (eth/arp) vs tiempo
ax = plt.subplot(111)
x_seconds = list()
y_entropyEth = list()
y_entropyArp = list()
contador = 10


for line in stdin:
	# segundos_entropíaEthernet_entropíaARP
	if contador == 30:
		cols = line.strip().split()
		x_seconds.append(float(cols[0])/60)
		y_entropyEth.append(float(cols[1]))
		y_entropyArp.append(float(cols[2]))
		contador = 0
	else:
		contador += 1

figure(1)
#titulo más arriba
figure_title = "Entropia del modelo respecto al tiempo transcurrido"
plt.text(0.5, 1.04, figure_title,
         horizontalalignment='center',
         fontsize=20,
         transform = ax.transAxes)

xlabel(u"Minutos")
ylabel(u"Entropía")
#x, y, color='green', linestyle='dashed', marker='o',
#     markerfacecolor='blue', markersize=12
plot(x_seconds, y_entropyEth, color='green', marker='o', markerfacecolor='green', markersize=6, label=u"Modelo Ethernet")
plot(x_seconds, y_entropyArp, color='red', marker='o', markerfacecolor='red', markersize=6, label=u"Modelo ARP")

#Leyenda arriba
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True)

show()
