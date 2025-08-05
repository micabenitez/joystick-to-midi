import pygame
import threading
import sys
import customtkinter as ctk

from config import CC_PRESETS, UMBRAL_ACTIVACION, UMBRAL_LIBERACION
from midi_handler import abrir_puerto
from joystick import JoystickReader
from gui import JoystickToMidiGUI

def main():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No joystick encontrado")
        sys.exit(1)

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    outport = abrir_puerto()
    if outport is None:
        sys.exit(1)

    root = ctk.CTk()

    gui = JoystickToMidiGUI(root, CC_PRESETS, callback_cc_cambiado=None)

    # Creamos el lector joystick, con referencias a variables de la GUI
    lector = JoystickReader(
        joystick,
        outport,
        gui.modo_izq_var,
        gui.modo_der_var,
        gui.cc_izq,
        gui.cc_der,
        UMBRAL_ACTIVACION,
        UMBRAL_LIBERACION
    )

    # Para actualizar CC cuando cambie en la GUI, definimos callback
    def actualizar_cc(lado, valor):
        if lado == "izq":
            lector.cc_izq = valor
        else:
            lector.cc_der = valor

    gui.callback_cc_cambiado = actualizar_cc

    stop_event = threading.Event()
    hilo = threading.Thread(target=lector.leer, args=(stop_event,), daemon=True)
    hilo.start()

    def cerrar():
        stop_event.set()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", cerrar)
    root.mainloop()

if __name__ == "__main__":
    main()
