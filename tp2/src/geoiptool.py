#!/usr/bin/env python

import sys
from math import *
from pprint import *

INPUT_SEPARATOR = '|'

# Esta funcion lee de la entrada estandar la salida del trace. Devuelve un diccionario con esta forma: { ttl : [(host, milliseconds ) ... ] }
def read_samples_from_stdin():
	samples = {}
	hosts = {}
	for line in sys.stdin:
		if '#' in line:
			continue
		ttl, host, milliseconds = line.strip().split(INPUT_SEPARATOR)
		try:
			ttl = int(ttl)
			milliseconds = float(milliseconds)
			if ttl not in samples:
				samples[ttl] = []
				hosts[ttl] = []
			samples[ttl].append(milliseconds)
			hosts[ttl].append(host)
		except:
			pass # Do nothing
	return hosts, samples

def hosts_per_ttl(hosts={}):
	fhosts = {}
	for ttl in hosts:
		fhosts[ttl] = []
		for host in hosts[ttl]:
			if host not in fhosts[ttl]:
				fhosts[ttl].append(host)
	return fhosts

from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

def print_hosts(hosts={}):
	# print("ttl", "ip", "hostname", "country", "region", "isp", "lat", "lon", '\n')
	for ttl in hosts:
		# for host in hosts[ttl]:
		host = hosts[ttl][0].strip()
		if '(' in host:
			host = host.split('(')[1][:-1]
		# url = 'http://www.telize.com/geoip/' + host
		url = 'http://ip-api.com/json/' + host
		request = urlopen(Request(url))
		answer = request.read().decode()
		answer = json.loads(answer)
		lon = 0
		lat = 0
		country = "-"
		region = "-"
		isp = "-"
		if answer['status'] == 'success':
			lon = answer['lon']
			lat = answer['lat']
			country = answer['country']
			region = answer['regionName']
			isp = answer['as']
		url = 'http://ipinfo.io/' + host + '/json'
		request = urlopen(Request(url))
		answer = request.read().decode()
		answer = json.loads(answer)
		ip = answer['ip']
		hostname = answer['hostname']
#			print(ttl, ip, hostname, country, region, isp, lat, lon)
		sep = '&'
		print(ttl, sep, ip, sep, country, sep, region, sep, lat, lon, '\\\\ \\hline')
		# print()

hosts, samples = read_samples_from_stdin()
hosts = hosts_per_ttl(hosts)
print_hosts(hosts)
