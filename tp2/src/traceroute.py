#!/usr/bin/env python3

import socket as Socket
import struct as Struct
import os as OS
import sys as Sys

def checksum(msg):
	s = 0

	# loop taking 2 characters at a time
	for i in range(0, len(msg), 2):
		w = (msg[i]) + ((msg[i+1]) << 8 )
		s = s + w

	s = (s>>16) + (s & 0xffff);
	s = s + (s >> 16);

	#complement and mask to 4 byte short
	s = ~s & 0xffff

	return Socket.htons(s)

class IP:
	def __init__(self, src=0, dst=0, ttl=255):
		self.version = 4 # IPv4
		self.internet_header_length = 5 # (*) (**)
		self.differenciated_services_code_point = 0
		self.explicit_congestion_notification = 0
		self.total_length = 0 # (*)
		self.identification = Socket.htons(OS.getpid())
		self.flags = 0
		self.fragment_offset = 0
		self.time_to_live = ttl
		self.protocol = Socket.IPPROTO_ICMP
		self.header_checksum = 0 # (*)
		self.source_address = src
		self.destination_address = dst

	def pack(self):
		#TODO: faltan algunos campos que por lo general son 0.
		return Struct.pack('!BBHHHBBH4s4s',
			(self.version << 4) + self.internet_header_length,
			(self.differenciated_services_code_point << 2) + self.explicit_congestion_notification,
			self.total_length,
			self.identification,
			self.fragment_offset,
			self.time_to_live,
			self.protocol,
			self.header_checksum,
			self.source_address,
			self.destination_address
		)

	def unpack(self, data):
		host = data[1]
		packet = data[0]
		ip_header = Struct.unpack('!BBHHHBBH4s4s', packet[:20])

		self.version = ip_header[0] >> 4
		self.internet_header_length = ip_header[0] & 0xf
		#self.differenciated_services_code_point = ip_header[1]
		#self.explicit_congestion_notification = ip_header[1]
		self.total_length = ip_header[2]
		self.identification = ip_header[3]
		#self.flags = ip_header[4]
		#self.fragment_offset = ip_header[4]
		self.time_to_live = ip_header[5]
		self.protocol = ip_header[6]
		self.header_checksum = ip_header[7]
		self.source_address = ip_header[8]
		self.destination_address = ip_header[9]

	def print(self):
		print('version', self.version)
		print('internet_header_length', self.internet_header_length)
		#print('differenciated_services_code_point', self.differenciated_services_code_point)
		#print('explicit_congestion_notification', self.explicit_congestion_notification)
		print('total_length', self.total_length)
		print('identification', self.identification)
		#print('flags', self.flags)
		#print('fragment_offset', self.fragment_offset)
		print('time_to_live', self.time_to_live)
		print('protocol', self.protocol, 'ICMP' if self.protocol == Socket.IPPROTO_ICMP else '(?)')
		print('header_checksum', hex(self.header_checksum))
		print('source_address', Socket.inet_ntoa(self.source_address))
		print('destination_address', Socket.inet_ntoa(self.destination_address))


#(*) El kernel se encarga de completar con los valores correctos
#(**) El tamano del header ip sin opciones es sizeof(ip_header) / 4 bytes = 5

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMP_TIME_TO_LIVE_EXCEEDED = 11

class Echo():
	def __init__(self, sequence_number=0):
		self.type = ICMP_ECHO_REQUEST
		self.code = 0
		self.checksum = 0
		self.identifier = Socket.htons(OS.getpid())
		self.sequence_number = Socket.htons(sequence_number)

	def pack(self):
		echoRequest = Struct.pack('!BBHHH',
			self.type,
			self.code,
			0,
			self.identifier,
			self.sequence_number
		)

		return Struct.pack('!BBHHH',
			self.type,
			self.code,
			checksum(echoRequest),
			self.identifier,
			self.sequence_number
		)

	def unpack(self, data):
		host = data[1]
		packet = data[0]
		icmp_header = Struct.unpack('!BBH', packet[20:24])

		self.type = icmp_header[0]
		self.code = icmp_header[1]
		self.checksum = icmp_header[2]
		self.identifier = 0
		self.sequence_number = 0

		if self.type == ICMP_ECHO_REPLY:
			icmp_header = Struct.unpack('!HH', packet[24:28])
			self.identifier = icmp_header[0]
			self.sequence_number = icmp_header[1]	

		if self.type == ICMP_TIME_TO_LIVE_EXCEEDED:
			pass # el payload es el paquete original (ip = IP(); ip.unpack(packet[28:]))
			

	def print(self):
		print('type', self.type, "RELPY" if self.type == ICMP_ECHO_REPLY else ("REQUEST" if self.type == ICMP_ECHO_REQUEST else "?"))
		print('code', self.code)
		print('checksum', hex(self.checksum))
		print('identifier', self.identifier)
		print('sequence_number', self.sequence_number)

# localhost
local_hostname = Socket.gethostname()
local_host = Socket.gethostbyname(local_hostname)
local_ip = Socket.inet_aton(local_host)

# www.google.com
remote_hostname = 'www.google.com'
remote_host = Socket.gethostbyname(remote_hostname)
remote_ip = Socket.inet_aton(remote_host)

#print('Pinging from', local_hostname, local_host, 'to', remote_hostname, remote_host)

SOCKET_TIMEOUT = 1 # segundos

socket = Socket.socket(Socket.AF_INET, Socket.SOCK_RAW, Socket.IPPROTO_ICMP)
socket.setsockopt(Socket.IPPROTO_IP, Socket.IP_HDRINCL, 1)
socket.setsockopt(Socket.SOL_SOCKET, Socket.SO_RCVTIMEO, Struct.pack('LL', SOCKET_TIMEOUT, 0))

ip = IP(src=local_ip, dst=remote_ip, ttl=1)
echoRequest = Echo(1)

ip.print()
echoRequest.print()

# Enviar ping!
socket.sendto(ip.pack()+echoRequest.pack(), (remote_host, 0))

# Esperar respuesta o timeout
try:
	data = socket.recvfrom(65565)
	
	print('=' * 80)

	ip = IP()
	ip.unpack(data)
	ip.print()
	
	if(ip.protocol == Socket.IPPROTO_ICMP):
		icmp = Echo()
		icmp.unpack(data)
		icmp.print()

except BlockingIOError:
	print('timeout!')
