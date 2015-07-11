#!/usr/bin/env python

import sys
import math
import pprint

samples = {}
average = {}
median = {}
deviation = {}

for line in sys.stdin:
	if '#' in line:
		continue
	ttl, host, millis = line.strip().split('|')
	ttl = int(ttl)
	if ttl not in samples:
		samples[ttl] = []
		deviation[ttl] = 0
		average[ttl] = 0
		median[ttl] = 0
	try:
		samples[ttl].append((host, float(millis)))
	except:
		pass

# pprint.pprint(samples)

for ttl in samples:
	samples[ttl] = sorted(samples[ttl], key=lambda pair: pair[1])
	n = len(samples[ttl])
	if n > 0:
		if n % 2 == 0:
			median[ttl] = (samples[ttl][n//2][1] + samples[ttl][(n//2)-1][1]) / 2
		else:
			median[ttl] = samples[ttl][n//2][1]

# pprint.pprint(median)

for ttl in samples:
	for host, millis in samples[ttl]:
		average[ttl] += millis
	if len(samples[ttl]) > 0:
		average[ttl] /= len(samples[ttl])

# pprint.pprint(average)

for ttl in samples:
	for host, millis in samples[ttl]:
		deviation[ttl] += pow(millis - average[ttl], 2)
	if len(samples[ttl]) > 1:
		deviation[ttl] /= len(samples[ttl])
	deviation[ttl] = math.sqrt(deviation[ttl])

# pprint.pprint(deviation)

filtered = {} # filtrado usando promedio
filtered_median = {} # filtrado usando mediana
filtered_k = {} # tomando k valores desde el centro del arreglo. k < len(samples[i])

for ttl in samples:
	for host, millis in samples[ttl]:
		if millis <= (average[ttl]+deviation[ttl]) and millis >= (average[ttl]-deviation[ttl]):
			if ttl not in filtered:
				filtered[ttl] = []
			filtered[ttl].append((host, millis))

for ttl in samples:
	for host, millis in samples[ttl]:
		if millis <= (median[ttl]+deviation[ttl]) and millis >= (median[ttl]-deviation[ttl]):
			if ttl not in filtered_median:
				filtered_median[ttl] = []
			filtered_median[ttl].append((host, millis))

k = 10
dk = k // 2

for ttl in samples:
	if ttl not in filtered_k:
		filtered_k[ttl] = []
	i = len(samples[ttl]) // 2
	filtered_k[ttl] = samples[ttl][i-dk:i+dk]

# pprint.pprint(filtered)
# pprint.pprint(filtered_median)
# pprint.pprint(filtered_k)

# for ttl in filtered:
# 	for host, millis in filtered[ttl]:
# 		print("%d|%s|%f" % (ttl, host, millis))

for ttl in average:
	average[ttl] = 0

for ttl in filtered:
	for host, millis in filtered[ttl]:
		average[ttl] += millis
	if len(filtered[ttl]) > 0:
		average[ttl] /= len(filtered[ttl])

pprint.pprint('Average')
pprint.pprint(average)

rtti = {}
rtti[1] = average[1]
anterior_valido = average[1]
for ttl in range(2, len(average)+1):
	if average[ttl] > average[ttl-1]:
		rtti[ttl] = average[ttl] - average[ttl-1]
		anterior_valido = average[ttl]
	else:
		rtti[ttl] = average[ttl] - anterior_valido
	if rtti[ttl] < 0.0:
		rtti[ttl] = 0.0

pprint.pprint('RTTi')
pprint.pprint(rtti)

for ttl in average:
	average[ttl] = 0
	deviation[ttl] = 0

for ttl in rtti:
	average[ttl] += rtti[ttl]
	if len(rtti) > 0:
		average[ttl] /= len(rtti)


#pprint.pprint(rtti)
longitud = 0
for ttl,rttime in rtti.items():
	if rttime > 0:
		longitud += 1

AVERAGE = sum(rtti.values()) / longitud

DEVIATION = 0
for ttl in rtti:
	if average[ttl] > 0:
		DEVIATION += pow(rtti[ttl] - AVERAGE, 2)
DEVIATION = math.sqrt(DEVIATION / len(rtti) - 1)

pprint.pprint('desviation')
pprint.pprint(DEVIATION)

print AVERAGE 

zrtti = {}

for ttl in rtti:
	if rtti[ttl] != 0:
		zrtti[ttl] = (rtti[ttl] - AVERAGE) / DEVIATION
	else:
		zrtti[ttl] = 0.0

pprint.pprint('zrtti')
pprint.pprint(zrtti)
