# coding:utf-8
import socket
import struct
from ctypes import *
from binascii import *

# 监听的主机IP
host = "192.168.1.243"

class Ethernet(Structure):

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        self.dest = socket_buffer[:6]
        self.src = socket_buffer[6:12]
        self.type = socket_buffer[12:14]

        self.protocol_map = {'0800': "IP", '0806':"ARP", '86DD': "IPv6", '880B': "PPP"}

        a = ""
        # readable ip address
        self.src_address = b2a_hex(self.dest)
        self.src_address = self.src_address[:2] + ':' \
                        + self.src_address[2:4] + ':' \
                        + self.src_address[4:6] + ':' \
                        + self.src_address[6:8] + ':' \
                        + self.src_address[8:10] + ':' \
                        + self.src_address[10:]

        self.dst_address = b2a_hex(self.src)
        self.dst_address = self.dst_address[:2] + ':' \
                        + self.dst_address[2:4] + ':' \
                        + self.dst_address[4:6] + ':' \
                        + self.dst_address[6:8] + ':' \
                        + self.dst_address[8:10] + ':' \
                        + self.dst_address[10:]

        # type of protocol
        try:
            self.protocol = self.protocol_map[b2a_hex(self.type)]
        except:
            self.protocol = b2a_hex(self.type)

# IP头定义
class IP(Structure):
    _fields_ = [
        ("ihl",             c_ubyte, 4),
        ("version",         c_ubyte, 4),
        ("tos",             c_ubyte),
        ("len",             c_ushort),
        ("id",              c_ushort),
        ("offset",          c_ushort),
        ("ttl",             c_ubyte),
        ("protocol_num",    c_ubyte),
        ("sum",             c_ushort),
        ("src",             c_uint),
        ("dst",             c_uint),
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        self.protocol_map = {1: "ICMP", 2:"IGMP", 6: "TCP", 17: "UDP"}

        # readable ip address
        self.src_address = socket.inet_ntoa(struct.pack("<I", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<I", self.dst))

        # type of protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
#sniffer.bind((host, 0))
#sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

try:
    while True:
        raw_buffer = sniffer.recvfrom(65535)[0]

        eth_header = Ethernet(raw_buffer[:14])
        print "Protocol: %s\nMAC_Src: %s\nMAC_Dest: %s" %(eth_header.protocol,
                                                        eth_header.src_address,
                                                        eth_header.dst_address,)
         
        ip_header = IP(raw_buffer[14:34])
        print "Protocol: %s\nMAC_Src: %s\nMAC_Dest: %s\n\n" % (ip_header.protocol, 
                                                        ip_header.src_address, 
                                                        ip_header.dst_address)

        
except KeyboardInterrupt:
    pass