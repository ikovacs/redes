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
    diffs = []
    for i in range(1,len(times)):
        diffs.append(times[i+1]-times[i])
    return diffs

def standard_deviation(diffs,avg):
    acum = 0
    for i in range(0,len(diffs)):
        acum += pow(diffs[i]-avg,2)
    return sqrt(acum/len(diffs)-1)

def standard_value(diffs, proms, sd):
    zrtt = []
    for i in range(0,len(diffs)):
        zrtt.append((diffs[i] - proms[i]) / sd[i])
    return zrtt

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

    hosts = {"www.cuhk.edu.hk":"china.txt"} #"www.ubc.ca":"canada.txt","www.msu.ru":"rusia.txt",

    for host in hosts.keys():
        arch=hosts[host]
        print "Comienzo de traceroute a: "+host
        print "Hora: " + str(time.time())
        print "Se guarda en: " + arch

        t = MyTraceRoute()

        hops, times = t.normal_traceroute(host=host)
        print_hops(arch, hops, times)

        #Calculo tiempos entre hops
        diffs = rtt_between_hops(times)
        print(diffs)

        #Calculo RTT (promedio)
        proms = reduce(lambda x, y: x + y, diffs) / len(diffs)
        print(proms)
        
        #Calculo SRTT 
        sd = standard_deviation(diffs,R)
        print(sd)

        #Calculo ZRTT
        zrtt = standard_value(diffs,proms,sd)
        print(zrtt)


        #Definiendo el RTT a partir de varios paquetes. 
        hopsf, timesf, mins, maxs = t.full_traceroute(host=host, packages=3)

        #transatlantics = get_transatlantics(R,sd,hops,diffs)

        #get_path() solo anda si antes ejecutaste normal_traceroute()
        #print t.get_path()

        #print_hops(arch, hops, times, transatlantics, mins, maxs)
        print "Terminado traceroute a: "+host

if __name__ == "__main__":
    main()
