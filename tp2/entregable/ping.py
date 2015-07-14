#! /usr/bin/python
import random, os, sys
from scapy.all import *
from scapy.layers.inet import ICMP, IP

rtts = []
loss_packets = 0

EchoReply = 0

def ping_echo_request_to(host, ttl=255, timeout=1):
    cur_time = time.time()
    answer = sr1(IP(dst=host, ttl=ttl) / ICMP(),verbose=0, timeout=timeout)

    if answer and answer[ICMP].type == EchoReply:
        rtt = (time.time() - cur_time) * 1000
        global rtts
        rtts.append(rtt)
    else:
        global loss_packets
        loss_packets += 1


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


M = 10 # Cant. de valores al azar tomados de rtts, debe ser multiplo de su longitud 

def estimatedRTT_for_alfa(alfa, file_name):
    file = open(file_name, 'w+')
    paso_intervalo = len(rtts) / M
    for n in range(len(rtts) / 10, len(rtts), len(rtts) / 10):
        file.write('estimatedRTT for %s: %s \n' % (n, estimatedRTT(alfa, n)))
    file.close()


def main():
    host = sys.argv[1] 
    cant_pings = 10000
    pingIterator(cant_pings, host)

    path = 'ping_files'
    if not os.path.exists(path):
        os.mkdir(path)

    for n in range(len(rtts) / 4, len(rtts), len(rtts) / 4):
        estimatedRTT_for(n, path+'/estimatedRTT_host_%s_n_fijo: %s.txt' % (host, n))

    for alfa in [x * 0.2 for x in range(6)]:
        estimatedRTT_for_alfa(alfa, path+'/estimatedRTT_host_%s_alfa_fijo: %s.txt' % (host, alfa))

    alfa = 0.9
    estimatedRTT_for_alfa(alfa, path+'/estimatedRTT_host_%s_alfa_fijo: %s.txt' % (host, alfa))

    cant_reply = len(rtts)
    cant_request = len(rtts) + loss_packets
    print 'Echo reply: %s' % cant_reply
    print 'Echo request: %s' % cant_request
    print 'Estimated Packet Loss Probability: %s' % (1 - (cant_reply / cant_request))

    file = open(path+'/probability_host_%s' % host, 'w+')
    file.write('Echo reply: %s' % cant_reply)
    file.write('Echo request: %s' % cant_request)
    file.write('Estimated Packet Loss Probability: %s' % (1 - (cant_reply / cant_request)))
    file.close()


if __name__ == "__main__":
    main()
