#! /usr/bin/python

import unicodedata
import urllib
import json
import sys
from math import *
from scapy.all import *

rtt_of_unknown = 0


class MyTraceRoute:
    hops = {}
    times = {}
    min_times = {}
    max_times = {}

    def request(self, host, ttl=30, timeout=1):
        cur_time = time.time()
        resp = sr(IP(dst=host, ttl=ttl) / ICMP(), timeout=timeout)
        rtt = (time.time() - cur_time)*1000
        resp += (rtt, )
        return resp

    def full_traceroute(self, host, timeout=1, packages=4):
        self.hops = {}
        self.times = {}
        ttl = 1
        no_termino = True
        while no_termino:

            self.times[ttl] = []
            for i in range(1, packages):
                ans, unans, rtt = self.request(host, ttl, timeout)

                if len(ans.res) > 0:  # hubo respuesta
                    hop_ip = ans.res[0][1].src # storing the src ip from ICMP error message

                    if ans.res[0][1].type == 0: # checking for  ICMP echo-reply
                        no_termino = False

                else:   # no contesto nadie
                    hop_ip = "?"
                    rtt = rtt_of_unknown    # SI NADIE CONTESTA QUE TIEMPO LE PONEMOS??

                if not self.hops.has_key(ttl): self.hops[ttl] = []
                if not hop_ip in self.hops[ttl]: self.hops[ttl].append(hop_ip)
                self.times[ttl].append(rtt)

                if i == 1: 
                    self.min_times[ttl] = rtt
                    self.max_times[ttl] = rtt
                else:
                    self.min_times[ttl] = min(self.min_times[ttl], rtt)
                    self.max_times[ttl] = max(self.max_times[ttl], rtt)

            ttl += 1

        return (self.hops, self.times, self.min_times, self.max_times)

    def normal_traceroute(self, host, timeout=2):
        hops = {}
        times = {}
        ttl = 1
        no_termino = True
        while no_termino:
            ans, unans, rtt = self.request(host, ttl, timeout)

            if len(ans.res) > 0:  # hubo respuesta		
                hop_ip = ans.res[0][1].src # storing the src ip from ICMP error message

                if ans.res[0][1].type == 0: # checking for  ICMP echo-reply
                    no_termino = False

            else:   # no contesto nadie
                hop_ip = "?"
                rtt = rtt_of_unknown

            self.hops[ttl] = hop_ip
            self.times[ttl] = rtt
            ttl += 1

        return (self.hops, self.times)

    def scapy_traceroute(self, host):
        return traceroute([host], maxttl=20, retry=-2)

    # para las direcciones privadas o mal formadas devuelve (None, None).
    def get_location(self, ip):
        jresp = urllib.urlopen("http://api.hostip.info/get_json.php?ip=%s&position=true" % ip).read()
        response = json.loads(jresp.encode("ascii", "ignore"))
        return (response['lat'], response['lng'])

    # devuelve un arreglo de los hops que se pudieron geolocalizar
    def get_path(self):
        path = []
        for ip in self.hops.values():
            lat, lng = self.get_location(ip)
            if lat != None and lng != None:
                path.append((ip, float(lat), float(lng)))

        return path