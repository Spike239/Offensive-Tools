#!/usr/bin/env python3

import argparse
import scapy.all as scapy

def get_target():
    parser = argparse.ArgumentParser(description="ARP Scann")
    parser.add_argument("-t", "--target", required=True, dest="target", help="Hosts o rango de hosts a escanear")

    args = parser.parse_args()

    return args.target

def scan(ip):
    arp_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    arp_packet = broadcast_packet/arp_packet

    answered, unanswered = scapy.srp(arp_packet, timeout=1, verbose=False)

    response = answered.summary()

    if response:
        print(response)

def main():
    target = get_target()
    scan(target)

if __name__ == '__main__':
    main()
