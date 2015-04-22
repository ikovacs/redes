#!/usr/bin/env python2

import sys

hist = open(sys.argv[1], 'w+')

temp = dict()

for line in sys.stdin:
	values = line.strip().split()
	if values[0] == 'arp':
		key = values[1]
		if not key in temp.keys():
			temp[key] = 1
		else:
			temp[key] += 1
	
for key, value in temp.items():
	hist.write(key + ' ' + str(value) + '\n')
hist.close()
