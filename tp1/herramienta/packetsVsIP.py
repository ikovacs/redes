#!/usr/bin/env python2

import sys
import math

entropy = 8.5144861881
hist = open(sys.argv[1], 'w+')

temp = dict()
total = 0

for line in sys.stdin:
	values = line.strip().split()
	if values[0] == 'arp':
		total += 1
		key = values[1]
		if not key in temp.keys():
			temp[key] = 1
		else:
			temp[key] += 1

for key, value in temp.items():
	p = float(value)/float(total)
	i = - math.log(p,2)
	hist.write(key + ' ' + str(i) + '\n')
hist.close()