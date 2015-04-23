#!/usr/bin/env python2

import sys

hist = open(sys.argv[1], 'w+')

suma = 0
cont = 0
for line in sys.stdin:
	values = line.strip().split()
	suma += float(values[2])
	cont += 1

hist.write('entropy promedio: ' + str(suma/cont))
hist.close()
