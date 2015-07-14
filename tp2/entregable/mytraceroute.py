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
        resp = sr(IP(dst=host, ttl=ttl) / ICMP(),verbose=0, timeout=timeout)
        rtt = (time.time() - cur_time)*1000
        resp += (rtt, )
        return resp

    def full_traceroute(self, host, timeout=1, packages=10):
        self.hops = {}
        self.times = {}
        ttl = 1
        no_termino = True
        pingLine = "%d|%s|%s"
        while no_termino and ttl <= 255:

            self.times[ttl] = []

            for i in range(1, packages):
                ans, unans, rtt = self.request(host, ttl, timeout)

                if len(ans.res) > 0:
                    hop_ip = ans.res[0][1].src 

                    if ans.res[0][1].type != 11:
                        no_termino = False

                    print pingLine % (ttl, hop_ip, str(rtt))

                else:   # no contesto nadie
                    print pingLine % (ttl, hop_ip, 'TIME_OUT')
            
                if not self.hops.has_key(ttl): self.hops[ttl] = []
                if not hop_ip in self.hops[ttl]: self.hops[ttl].append(hop_ip)
                self.times[ttl].append(rtt)

            ttl += 1

        return (self.hops, self.times)
