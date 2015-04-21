#!/usr/bin/env python2

import sys

grafo = open(sys.argv[1], 'w+')
grafo.write('digraph {\n')

temp = dict()

for line in sys.stdin:
	values = line.strip().split()
	if values[0] == 'eth':
		key = values[1]+'-'+values[2]
		if not key in temp.keys():
			temp[key] = 1
		else:
			temp[key] += 1
	
for key, value in temp.items():
	values = key.split('-')
	grafo.write('\"' + values[0] + '\"' + ' -> ' + '\"' + values[1] + '\"' + '[label=' + str(value) + '];\n')
grafo.write('}\n')
grafo.close()
