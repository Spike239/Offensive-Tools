#!/usr/bin/env python3

import argparse, subprocess, signal, sys
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor

def def_handler(sig, frame):
    print(colored("\n[!] Saliendo del programa...", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def get_target():
    parser = argparse.ArgumentParser(description="Herramienta para descubrir Hosts activos (ICMP)")
    parser.add_argument("-t", "--target", required=True, dest="target", help="Host o rango de hosts a escanear")

    args = parser.parse_args()

    return args.target

def parse_target(target_str):
    # 192.168.68.1-100
    target_list = target_str.split('.') # ["192", "168", "68", "1-100"]
    first_three_octets = '.'.join(target_list[:3])

    if len(target_list) == 4:
        if "-" in target_list[3]:
            start, end = target_list[3].split("-")
            return [f"{first_three_octets}.{i}" for i in range(int(start), int(end)+1)]
        else:
            return [target_str]
    else:
        print(colored("\n[!] El formato que ingresaste es incorrecto...\n", "red"))

def host_discovery(target):
    try:
        ping = subprocess.run(["ping", "-c", "1", target], timeout=1, stdout=subprocess.DEVNULL)
        if ping.returncode == 0:
            print(colored(f"\t[i] La IP {target} esta activa", "green"))
    except subprocess.TimeoutExpired:
        pass

def main():
    target_str = get_target()
    targets = parse_target(target_str)

    print(colored("\n[+] Hosts activos en la red:\n", "red"))

    max_threads = 100

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(host_discovery, targets)

if __name__ == '__main__':
    main()
