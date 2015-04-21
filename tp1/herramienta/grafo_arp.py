#!/usr/bin/env python2

import sys

REPLY = '2'
REQUEST = '1'

grafo = open(sys.argv[1], 'w+')
grafo.write('digraph {\n')

temp = dict()

for line in sys.stdin:
	values = line.strip().split()
	if values[0] == 'arp':	
		key = values[1] + '-' + values[2] + '-' + values[5]
		if not key in temp.keys():
			temp[key] = 1
		else:
			temp[key] += 1
	
for key, value in temp.items():
	values = key.split('-')
	if value > 2:
		if values[2] == REPLY:
			grafo.write('\"' + values[0] + '\"' + ' -> ' + '\"' + values[1] + '\"' + '[label=\"' + str(value) + ' replies \"];\n')
		else:
			grafo.write('\"' + values[0] + '\"' + ' -> ' + '\"' + values[1] + '\"' + '[label=\"' + str(value) + ' requests \"];\n')
grafo.write('}\n')
grafo.close()
