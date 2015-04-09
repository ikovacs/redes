#include <pcap/pcap.h>
#include <arpa/inet.h>

#include <iomanip>
#include <iostream>

using namespace std;

/* ethernet headers are always exactly 14 bytes [1] */
#define SIZE_ETHERNET 14

/* Ethernet addresses are 6 bytes */
#define ETHER_ADDR_LEN	6

/* Ethernet header */
struct sniff_ethernet {
	u_char ether_dhost[ETHER_ADDR_LEN]; /* destination host address */
	u_char ether_shost[ETHER_ADDR_LEN]; /* source host address */
	u_short ether_type; /* IP? ARP? RARP? etc */
};

/* IP header */
struct sniff_ip {
	u_char ip_vhl; /* version << 4 | header length >> 2 */
	u_char ip_tos; /* type of service */
	u_short ip_len; /* total length */
	u_short ip_id; /* identification */
	u_short ip_off; /* fragment offset field */
	#define IP_RF 0x8000 /* reserved fragment flag */
	#define IP_DF 0x4000 /* dont fragment flag */
	#define IP_MF 0x2000 /* more fragments flag */
	#define IP_OFFMASK 0x1fff /* mask for fragmenting bits */
	u_char ip_ttl; /* time to live */
	u_char ip_p; /* protocol */
	u_short ip_sum; /* checksum */
	struct in_addr ip_src,ip_dst; /* source and dest address */
};
#define IP_HL(ip) (((ip)->ip_vhl) & 0x0f)
#define IP_V(ip) (((ip)->ip_vhl) >> 4)

/* TCP header */
typedef u_int tcp_seq;

struct sniff_tcp {
        u_short th_sport; /* source port */
        u_short th_dport; /* destination port */
        tcp_seq th_seq; /* sequence number */
        tcp_seq th_ack; /* acknowledgement number */
        u_char  th_offx2; /* data offset, rsvd */
#define TH_OFF(th) (((th)->th_offx2 & 0xf0) >> 4)
        u_char th_flags;
        #define TH_FIN 0x01
        #define TH_SYN 0x02
        #define TH_RST 0x04
        #define TH_PUSH 0x08
        #define TH_ACK 0x10
        #define TH_URG 0x20
        #define TH_ECE 0x40
        #define TH_CWR 0x80
        #define TH_FLAGS (TH_FIN|TH_SYN|TH_RST|TH_ACK|TH_URG|TH_ECE|TH_CWR)
        u_short th_win; /* window */
        u_short th_sum; /* checksum */
        u_short th_urp; /* urgent pointer */
};

/* ARP Header, (assuming Ethernet+IPv4) */ 
#define ARP_REQUEST 1 /* ARP Request */
#define ARP_REPLY 2 /* ARP Reply */
struct sniff_arp {
    u_int16_t htype; /* Hardware Type */
    u_int16_t ptype; /* Protocol Type */
    u_char hlen; /* Hardware Address Length */
    u_char plen; /* Protocol Address Length */
    u_int16_t oper; /* Operation Code */
    u_char sha[6]; /* Sender hardware address */
    u_char spa[4]; /* Sender IP address */
    u_char tha[6]; /* Target hardware address */
    u_char tpa[4]; /* Target IP address */
}; 

void got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet);

int main(int argc, char *argv[]) {

	char error[PCAP_ERRBUF_SIZE];
	char *device;

	/* Elección de dispositivo de red */

	//device = argv[1]; // (manual)
	device = pcap_lookupdev(error); // (automático)

	if(device != 0) {
		cout << "Device: " << device << endl;
	}
	else {
		cerr << "Couldn't find default device: " << error << endl;
		return 2;
	}

	/* Apertura de dispositivo de red para captura */

	pcap_t *handle;
	int promiscuous_mode = 1; // (true)
	int read_timeout = 1000; // milliseconds

	handle = pcap_open_live(device, BUFSIZ, promiscuous_mode, read_timeout, error);

	if(handle == 0) {
		cerr << error << endl;
		return 2;
	}

	/* Verificar si soporta la capa de enlace */

	int ans;

	ans = pcap_datalink(handle);

	if(ans != DLT_EN10MB) {
		cerr << "Device " << device << " doesn't provide Ethernet headers.\n" << endl;
		return 2;
	}

	/* Crear un filtro */

	char filter_expression[] = "arp";
	struct bpf_program filter;
	int optimize_expression = 0; // (false)
	bpf_u_int32 net;

	ans = pcap_compile(handle, &filter, filter_expression, optimize_expression, net);

	if(ans == -1) {
		cerr << pcap_geterr(handle) << endl;
		return 2;
	}

	ans = pcap_setfilter(handle, &filter);

	if(ans == -1) {
		cerr << pcap_geterr(handle) << endl;
		return 2;	
	}

	/* Sniffing */

	ans = pcap_loop(handle, -1, got_packet, 0);

	/* Terminar */

	pcap_close(handle);

	return 0;
}

void got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet) {
	
	struct sniff_ethernet *ethernet_header;
	struct sniff_arp *arp_header;

	ethernet_header = (struct sniff_ethernet*) (packet);
	arp_header = (struct sniff_arp*) (packet + SIZE_ETHERNET);

	cout << "ARP" << endl;
	cout << " | Hardware type: " << ((ntohs(arp_header->htype) == 1) ? "Ethernet" : "Unknown") << endl;
	cout << " | Protocol type: " << ((ntohs(arp_header->ptype) == 0x0800) ? "IPv4" : "Unknown") << endl;
	cout << " | Operation: " << ((ntohs(arp_header->oper) == ARP_REQUEST) ? "ARP Request" : "ARP Reply") << endl;
	cout << " | Sender MAC: ";

		cout << hex << (int) arp_header->sha[0] << ":";
		cout << hex << (int) arp_header->sha[1] << ":";
		cout << hex << (int) arp_header->sha[2] << ":";
		cout << hex << (int) arp_header->sha[3] << ":";
		cout << hex << (int) arp_header->sha[4] << ":";
		cout << hex << (int) arp_header->sha[5] << endl;

	cout << " | Sender IP: ";

		cout << dec << (int) arp_header->spa[0] << ".";
		cout << dec << (int) arp_header->spa[1] << ".";
		cout << dec << (int) arp_header->spa[2] << ".";
		cout << dec << (int) arp_header->spa[3] << endl;

	cout << " | Receiver MAC: ";

		cout << hex << (int) arp_header->tha[0] << ":";
		cout << hex << (int) arp_header->tha[1] << ":";
		cout << hex << (int) arp_header->tha[2] << ":";
		cout << hex << (int) arp_header->tha[3] << ":";
		cout << hex << (int) arp_header->tha[4] << ":";
		cout << hex << (int) arp_header->tha[5] << endl;

	cout << " | Receiver IP: ";

		cout << dec << (int) arp_header->tpa[0] << ".";
		cout << dec << (int) arp_header->tpa[1] << ".";
		cout << dec << (int) arp_header->tpa[2] << ".";
		cout << dec << (int) arp_header->tpa[3] << endl;

	cout << endl;
}
