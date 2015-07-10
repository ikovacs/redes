#! /usr/bin/python
import random, os
from scapy.all import *
from scapy.layers.inet import ICMP, IP

rtts = []
loss_packets = 0


def ping_echo_request_to(host, ttl=255, timeout=1):
    cur_time = time.time()
    resp = sr(IP(dst=host, ttl=ttl) / ICMP(), timeout=timeout)
    if len(resp) <= 0:
        loss_packets += 1
    else:
        rtt = (time.time() - cur_time) * 1000
        rtts.append(rtt)


def pingIterator(cant, host):
    for i in range(cant):
        ping_echo_request_to(host)


def estimatedRTT(alfa, n):
    estimated = 0
    for i in range(n):
        estimated = alfa * estimated + (1 - alfa) * rtts[i]
    return estimated


def estimatedRTT_for(n, file_name):
    file = open(file_name, 'w+')
    for alfa in [x * 0.05 for x in range(21)]:
        file.write('estimatedRTT for %s: %s \n' % (alfa, estimatedRTT(alfa, n)))
    file.close()


M = 10 # Cant. de valores al azar tomados de rtts, debe ser multiplo de su longitud (OJO xD)

def estimatedRTT_for_alfa(alfa, file_name):
    file = open(file_name, 'w+')
    paso_intervalo = len(rtts) / M
    for m in range(M):
        i = random.randint(m * paso_intervalo, (m+1) * paso_intervalo)
        file.write('estimatedRTT for %s: %s \n' % (i, estimatedRTT(alfa, i)))
#    for n in range(len(rtts) / 10, len(rtts), len(rtts) / 10):
#        file.write('estimatedRTT for %s: %s \n' % (n, estimatedRTT(alfa, n)))
    file.close()


def main():
    host = input('Ingrese nombre del host: ')
    cant_pings = 1000 # o 5000 pero siempre el mismo para todos los host
    pingIterator(cant_pings, host)

    path = 'files'
    if not os.path.exists(path):
        os.mkdir(path)

    for n in range(len(rtts) / 4, len(rtts), len(rtts) / 4):
        estimatedRTT_for(n, path+'/estimatedRTT_host_%s_n_fijo: %s.txt' % (host, n))

    for alfa in [x * 0.2 for x in range(6)]:
        estimatedRTT_for_alfa(alfa, path+'/estimatedRTT_host_%s_alfa_fijo: %s.txt' % (host, alfa))

    cant_reply = len(rtts)
    cant_request = len(rtts) + loss_packets
    print 'Echo reply: %s' % cant_reply
    print 'Echo request: %s' % cant_request
    print 'Estimated Packet Loss Probability: %s' % (1 - cant_reply / cant_request)

    file = open(path+'/probability_host_%s' % host, 'w+')
    file.write('Echo reply: %s' % cant_reply)
    file.write('Echo request: %s' % cant_request)
    file.write('Estimated Packet Loss Probability: %s' % (1 - cant_reply / cant_request))
    file.close()


if __name__ == "__main__":
    main()
