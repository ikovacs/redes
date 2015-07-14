#! /usr/bin/python

import json, os, sys
from math import sqrt
from mytraceroute import *


def print_hops(file, hops, avg_host, zrtt, diffs):
    with open('%s' % (file), 'w') as f:
        f.write("hop\tips\tavg_host\tzrtt\trtt_between_hops\n")
        for i in hops.keys():
            if type(hops[i]) is list:
                f.write("%s\t[%s]" % (i, ",".join(hops[i])))
            else:
                f.write("%s\t%s" % (i, hops[i]))
            f.write("\t%.4f\t%.4f\t%.4f\n" % (avg_host[i-1], zrtt[i-1], diffs[i-1]))
        f.closed

def rtt_between_hops(times):
    diffs = [times[0]]
    for i in range(1, len(times)):
        diffs.append(times[i] - times[i - 1])
    return diffs


def standard_deviation(diffs, avg):
    acum = 0
    for i in range(0, len(diffs)):
        acum += pow(diffs[i] - avg, 2)
    return sqrt(acum / len(diffs) - 1)


def standard_value(diffs, avg, sd):
    zrtt = []
    for i in range(0, len(diffs)):
        zrtt.append((diffs[i] - avg) / sd)
    return zrtt


def main():
    host = sys.argv[1]

    path = 'traceroute_files'
    if not os.path.exists(path):
        os.mkdir(path)
    arch = path+'/%s.txt' % host

    traceroute = MyTraceRoute()

    hops, times = traceroute.full_traceroute(host=host,packages=1000)
    
    # Calculo promedio de RTT entre todos los host
    avg_host = [sum(times[ttl]) / len(times[ttl]) for ttl in range(1, len(times.keys()) + 1)]

    # Calculo tiempos entre hops
    diffs = rtt_between_hops(avg_host)
    #print(diffs)

    # Calculo RTT (promedio)
    avg = sum(diffs) / len(diffs)
    #print(avg)

    # Calculo SRTT
    sd = standard_deviation(diffs, avg)
    #print(sd)

    # Calculo ZRTT
    zrtt = standard_value(diffs, avg, sd)
    #print(zrtt)

    print_hops(arch, hops, avg_host, zrtt, diffs)
    #print "Terminado traceroute a: " + host


if __name__ == "__main__":
    main()
