#!/usr/bin/env python2

import sys

grafo = open(sys.argv[1], 'w+')
grafo.write('digraph {\n')

temp = dict()

for line in sys.stdin:
	values = line.strip().split()
	if values[0] == 'eth':
		key = values[1]+'-'+values[2]
		if int(values[3]) == 34525:
			key = key+'-'+'IPv6'
			if not key in temp.keys():
				temp[key] = 0
		if int(values[3]) == 2054:
			key = key+'-'+'ARP'
			if not key in temp.keys():
				temp[key] = 0
		if int(values[3]) == 2048:
			key = key+'-'+'IPv4'
			if not key in temp.keys():
				temp[key] = 0
	
for key, value in temp.items():
	values = key.split('-')
	grafo.write('\"' + values[0] + '\"' + ' -> ' + '\"' + values[1] + '\"' + '[label=' + values[2] + '];\n')
grafo.write('}\n')
grafo.close()
