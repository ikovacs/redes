#! /usr/bin/python
from scapy.all import *
from scapy.layers.inet import ICMP, IP

rtts = []
loss_packets = 0


def ping_echo_request_to(host, ttl=255, timeout=1):
    cur_time = time.time()
    resp = sr(IP(dst=host, ttl=ttl) / ICMP(), timeout=timeout)
    # print type(resp)
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


def estimatedRTT_for_alfa(alfa, file_name):
    file = open(file_name, 'w+')
    for n in range(len(rtts) / 50, len(rtts), len(rtts) / 50):
        file.write('estimatedRTT for %s: %s \n' % (n, estimatedRTT(alfa, n)))
    file.close()


def main():
    host = input('Ingrese nombre del host: ')
    cant_pings = 5
    pingIterator(cant_pings, host)

    for i in range(len(rtts) / 5, len(rtts), len(rtts) / 5):
        estimatedRTT_for(i, 'files/estimatedRTT_%s_host_%s_n_fijo.txt' % (i, host))

    for i in [x * 0.2 for x in range(6)]:
        estimatedRTT_for_alfa(i, 'files/estimatedRTT_%s_host_%s_alfa_fijo.txt' % (i, host))

    cant_reply = len(rtts)
    cant_request = len(rtts) + loss_packets
    print 'Echo reply: %s' % cant_reply
    print 'Echo request: %s' % cant_request
    print 'Estimated Packet Loss Probability: %s' % (1 - cant_reply / cant_request)


if __name__ == "__main__":
    main()
