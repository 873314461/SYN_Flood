# coding:utf-8
import socket
import struct
import random

# checksum functions needed for calculation checksum
def checksum(msg):
	s = 0
	# loop taking 2 characters at a time
	for i in range(0, len(msg), 2):
		w = (ord(msg[i]) << 8) + (ord(msg[i+1]) )
		s = s + w
	
	s = (s>>16) + (s & 0xffff)
	#s = s + (s >> 16);
	#complement and mask to 4 byte short
	s = ~s & 0xffff
	
	return s

def make_packet(src_port, dst_port, src_ip, dst_ip, src_mac, dst_mac):
	print src_ip
	print src_mac
	print src_port


	packet = ''
	
	source_ip = src_ip
	dest_ip = dst_ip # or socket.gethostbyname('www.google.com')
	
	# ip header fields
	ihl = 5
	version = 4
	tos = 0
	tot_len = 20 + 20  # python seems to correctly fill the total length, dont know how ??
	id = 54321  #Id of this packet
	frag_off = 0
	ttl = 255
	protocol = socket.IPPROTO_TCP
	check = 10  # python seems to correctly fill the checksum
	saddr =socket.inet_aton ( source_ip )  #Spoof the source ip address if you want to
	daddr = socket.inet_aton ( dest_ip )
	
	ihl_version = (version << 4) + ihl
	
	# the ! in the pack format string means network order
	ip_header = struct.pack('!BBHHHBBH4s4s', ihl_version, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)
	
	# tcp header fields
	source = src_port   # source port
	dest = dst_port   # destination port
	seq = 0
	ack_seq = 0
	doff = 5    #4 bit field, size of tcp header, 5 * 4 = 20 bytes
	#tcp flags
	fin = 0
	syn = 1
	rst = 0
	psh = 0
	ack = 0
	urg = 0
	window = socket.htons (5840)    #   maximum allowed window size
	check = 0
	urg_ptr = 0
	
	offset_res = (doff << 4) + 0
	tcp_flags = fin + (syn << 1) + (rst << 2) + (psh <<3) +(ack << 4) + (urg << 5)
	
	# the ! in the pack format string means network order
	tcp_header = struct.pack('!HHLLBBHHH', source, dest, seq, ack_seq, offset_res, tcp_flags,  window, check, urg_ptr)

	# pseudo header fields
	source_address = socket.inet_aton( source_ip )
	dest_address = socket.inet_aton(dest_ip)
	placeholder = 0
	protocol = socket.IPPROTO_TCP
	tcp_length = len(tcp_header)
	
	psh = struct.pack('!4s4sBBH', source_address , dest_address , placeholder , protocol , tcp_length)
	psh = psh + tcp_header
	
	tcp_checksum = checksum(psh)
	
	# make the tcp header again and fill the correct checksum
	tcp_header = struct.pack('!HHLLBBHHH', source, dest, seq, ack_seq, offset_res, tcp_flags,  window, tcp_checksum , urg_ptr)
	
	packet_e = struct.pack("!6s6s2s", dst_mac, src_mac, "\x08\x00")

	return packet_e+ip_header + tcp_header

def getRandomIP():
	return "%d.%d.%d.%d" % (random.random()*255, random.random()*255, random.random()*255, random.random()*255)

def getRandomPort():
	return int(random.random()*65535)

def getRandomMac():
	return struct.pack("BBBBBB", random.randint(0x00, 0xff), random.randint(0x00, 0xff), random.randint(0x00, 0xff), random.randint(0x00, 0xff), random.randint(0x00, 0xff), random.randint(0x00, 0xff))

def sendData(dst_ip, dst_port):
	rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
	rawSocket.bind(("lo",socket.htons(0x0800)))
	packet = make_packet(getRandomPort(), dst_port,
		 				getRandomIP(), dst_ip,
						getRandomMac(), getRandomMac()
				)
	rawSocket.send(packet) 
