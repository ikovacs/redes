#! /usr/bin/python
from scapy.layers.inet import ICMP, IP

import urllib
import json
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

    def full_traceroute(self, host, timeout=1, packages=10):
        self.hops = {}
        self.times = {}
        ttl = 1
        no_termino = True
        while no_termino and ttl <= 255:
        
            self.times[ttl] = []
            for i in range(1, packages):
                ans, unans, rtt = self.request(host, ttl, timeout)

                if len(ans.res) > 0: 
                    hop_ip = ans.res[0][1].src #storing the src ip from ICMP error message

                    if ans.res[0][1].type != 11: #checking for  ICMP echo-reply
                        no_termino = False

                else:   # no contesto nadie
                    hop_ip = "?"
                    rtt = rtt_of_unknown

                if not self.hops.has_key(ttl): self.hops[ttl] = []
                if not hop_ip in self.hops[ttl]: self.hops[ttl].append(hop_ip)
                self.times[ttl].append(rtt)

            ttl += 1

        return (self.hops, self.times)

    # para las direcciones privadas o mal formadas devuelve (None, None). NO FUNCA..
    def get_location(self, ip):
        jresp = urllib.urlopen("http://api.hostip.info/get_json.php?ip=190.190.247.1&position=true" % ip).read()
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