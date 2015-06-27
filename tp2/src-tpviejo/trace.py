#! /usr/bin/python

import json
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
    host = input('Ingrese nombre del host: ')

    arch = 'traceroute_files/%s.txt' % host
    print "Comienzo de traceroute a: " + host
    print "Hora: " + str(time.time())
    print "Se guarda en: " + arch

    traceroute = MyTraceRoute()

    # hops, times = traceroute.normal_traceroute(host=host)

    hops, times = traceroute.full_traceroute(host=host)
    # print_hops(arch, hops, times)
    print 'hops: %s' % hops
    print 'times: %s' % times
    avg_host = [sum(times[ttl]) / len(times[ttl]) for ttl in range(1, len(times.keys()) + 1)]

    # Calculo tiempos entre hops
    diffs = rtt_between_hops(avg_host)
    print(diffs)

    # Calculo RTT (promedio)
    avg = sum(diffs) / len(diffs)
    print(avg)

    # Calculo SRTT
    sd = standard_deviation(diffs, avg)
    print(sd)

    # Calculo ZRTT
    zrtt = standard_value(diffs, avg, sd)
    print(zrtt)

    traceroute.get_path()
    print traceroute.get_path()

    print_hops(arch, hops, avg_host, zrtt, diffs)
    print "Terminado traceroute a: " + host


if __name__ == "__main__":
    main()
