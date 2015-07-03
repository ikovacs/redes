#! /usr/bin/python

import sys
import ast
import urllib
import json
from math import sqrt

idx_hop_num = 0
idx_ips = 1
idx_time = 2

class IPLocator:

	hops = {}

	def __init__(self, hops_file):
		self.hops = {}
		f = open(hops_file)
		lines = f.readlines()
		f.close()

		values = lines[1:]

		i = 1
		for hop_info in values:
			hop_data = hop_info.split("\t")

			hop_num = int(hop_data[idx_hop_num])
			hop_ips = []
			for ip in hop_data[idx_ips].split(","):
				for r in ["[", "]"]:
					ip = ip.replace(r, "")
				hop_ips.append(ip)
			hop_time = float(hop_data[idx_time])

			self.hops[hop_num] = { 
				'ips' : hop_ips,
				'time' : hop_time ,
			}

	def get_ip_path(self):
		path = {}
		for i in self.hops.keys():
			ips = self.hops[i]['ips']

			try: ips.remove('?')
			except ValueError: pass
			
			if len(ips) > 0: path[i] = ips[0]
		return path

	def save_locations(self, locations_file):
		location_file_name = locations_file + "_geo.csv"

		print "Guardando locations de ips en " + location_file_name + "..."

		f = open(location_file_name, 'w')

		f.write('hop,ip,continent,country,city,isp,organization,lat lng\n')

		ips = self.get_ip_path()

		for i in ips:
		
			data_location = self.get_location(ips[i])

			data = (
				i, 
				ips[i], 
				data_location['continent_name'], 
				data_location['country_name'], 
				data_location['city'], 
				data_location['isp'], 
				data_location['organization'], 
				data_location['latitude'], 
				data_location['longitude']
				)

			print data 

			f.write("%d,%s,%s,%s,%s,%s,%s,%s %s\n" % data)

		f.close()


	def get_location(self, ip):
		jresp = urllib.urlopen('http://api.ipaddresslabs.com/iplocation/v1.7/locateip?key=SAK24DX676988HRK26BZ&ip=%s&format=json' % ip).read()
		response = json.loads(jresp.encode("ascii", "ignore"))
		
		if response['query_status']['query_status_code'] == 'OK':
			return response['geolocation_data']


	def rtt_between_hops(self):
		diffs = []
		for hop in self.hops.keys():

			if hop != self.hops.keys()[-1]: 
				diffs.append(self.hops[hop+1]['time'] - self.hops[hop]['time'])
			else:
				diffs.append(0)
		return diffs

	def standard_deviation(self,diffs,avg):
		acum = 0
		for i in range(0,len(diffs)):
			acum += pow(diffs[i]-avg,2)
		return sqrt(acum/len(diffs)-1)

	def get_transatlantics(self,m=2):

		diffs = self.rtt_between_hops()
		#print(diffs)
		R = reduce(lambda x, y: x + y, diffs) / len(diffs)
		#print(R)
		sd = self.standard_deviation(diffs,R)

		transatlantics = []
		for i in range(0,len(diffs)):
			if diffs[i] > R + m * sd:
				transatlantics.append(1)
			else:
				transatlantics.append(0)
		return transatlantics

def main(params):

	if len(params) > 0: 
		hops_file = params[0]

		if len(params) == 1: 
			operation = ""
		else:
			operation = params[1]

		l = IPLocator(hops_file)

		if operation == "transa":


			m = float(params[2])
			print l.get_transatlantics(m)

		else:
			l.save_locations(hops_file)

	else: 
		print "Uso correcto: iplocator file_from_trace operacion [m]"
		print "Donde:"
		print "\tfile_from_trace: archivo que se obtuvo al correr repetidor"
		print "\toperacion: si es 'transa' va a devolver un arreglo de booleanos diciendo que hop es transatlantico. ES OBLIGATORIO EL PARAMETRO m. En caso de que operacion sea otro valor, se va a guardar en un txt los ips con sus datos de geolocalizacion"

if __name__ == "__main__":
	main(sys.argv[1:])