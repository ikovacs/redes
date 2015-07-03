#! /usr/bin/python

from mytraceroute import * 
 
def main():
	host = sys.argv[1]

	res,unans = MyTraceRoute.traceroute_scapy(host)
	res.graph()

if __name__ == "__main__":
    main()
