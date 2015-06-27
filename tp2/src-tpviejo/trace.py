#! /usr/bin/python

import json
from math import sqrt
from mytraceroute import * 

def print_hops(file, hops, times, transatlantic, mins, maxs):
    with open('%s' % (file), 'w') as f:
        f.write("hop\tips\ttime\tis_transat\tcant_ips\tmin_times\tmax_times\n")
        for i in hops.keys():
            if type(hops[i]) is list:
                f.write("%s\t[%s]" % (i, ",".join(hops[i])))
            else:
                f.write("%s\t%s" % (i, hops[i]))
            f.write("\t%.4f\t%s\t%s\t%.4f\t%.4f\n" % (times[i], transatlantic[i-1], str(len(hops[i])), mins[i], maxs[i]))
        f.closed

def print_transatlantics(file, trans):
    with open('%s' % (file), 'w') as f:
        for i in range(0,len(trans)):
            f.write("[%s]" % ", ".join(trans[i]))
        f.closed

def rtt_between_hops(times):
    diffs = [times[0]]
    for i in range(1, len(times)):
        diffs.append(times[i]-times[i-1])
    return diffs

def standard_deviation(diffs,avg):
    acum = 0
    for i in range(0,len(diffs)):
        acum += pow(diffs[i]-avg,2)
    return sqrt(acum/len(diffs)-1)

def standard_value(diffs, avg, sd):
    zrtt = []
    for i in range(0,len(diffs)):
        zrtt.append((diffs[i] - avg) / sd[i])
    return ZRTT

def get_transatlantics(R,sd,hops,diffs,m=2):

    transatlantics = []
    for i in range(0,len(diffs)):
        if diffs[i] > R + m * sd:
            transatlantics.append(1)
        else:
            transatlantics.append(0)
    transatlantics.append(0)
    return transatlantics

def main():
    host = input('Ingrese nombre del host: ')

    arch = 'traceroute_files/%s.txt' % host
    print "Comienzo de traceroute a: " + host
    print "Hora: " + str(time.time())
    print "Se guarda en: " + arch

    traceroute = MyTraceRoute()

    #hops, times = traceroute.normal_traceroute(host=host)

    hops, times = traceroute.full_traceroute(host=host)
    #print_hops(arch, hops, times)
        
    avg_host = [sum(times[ttl])/len(times[ttl]) for ttl in range(1, len(times.keys()) + 1)]

    #Calculo tiempos entre hops
    diffs = rtt_between_hops(avg_host)
    print(diffs)

    #Calculo RTT (promedio)
    avg = reduce(lambda x, y: x + y, diffs) / len(diffs)
    print(avg)
    
    #Calculo SRTT 
    sd = standard_deviation(diffs, avg)
    print(sd)

    #Calculo ZRTT
    zrtt = standard_value(diffs,avg,sd)
    print(zrtt)

    #transatlantics = get_transatlantics(avg,sd,hops,diffs)

    #traceroute.get_path()
    #print traceroute.get_path()

    #print_hops(arch, hops, times, transatlantics, mins, maxs)
    print "Terminado traceroute a: " + host

if __name__ == "__main__":
    main()
