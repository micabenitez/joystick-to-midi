import pygame
import time
from midi_handler import enviar_cc

class JoystickReader:
    def __init__(self, joystick, outport, modo_izq_var, modo_der_var, cc_izq, cc_der, umbral_act=0.2, umbral_lib=0.1):
        self.joystick = joystick
        self.outport = outport
        self.modo_izq_var = modo_izq_var
        self.modo_der_var = modo_der_var
        self.cc_izq = cc_izq
        self.cc_der = cc_der
        self.umbral_act = umbral_act
        self.umbral_lib = umbral_lib

        self.toggle_izq = False
        self.toggle_der = False
        self.pedal_izq_activo = False
        self.pedal_der_activo = False

    def leer(self, stop_event):
        while not stop_event.is_set():
            pygame.event.pump()
            valor = self.joystick.get_axis(1)

            # Izquierda
            if valor > self.umbral_act:
                if self.modo_izq_var.get() == "expresion":
                    valor_midi = int(min(max(valor, 0), 1) * 127)
                    enviar_cc(self.outport, self.cc_izq, valor_midi)
                elif self.modo_izq_var.get() == "boton" and not self.pedal_izq_activo:
                    self.toggle_izq = not self.toggle_izq
                    enviar_cc(self.outport, self.cc_izq, 127 if self.toggle_izq else 0)
                    self.pedal_izq_activo = True
            elif valor < self.umbral_lib:
                self.pedal_izq_activo = False

            # Derecha
            if valor < -self.umbral_act:
                if self.modo_der_var.get() == "expresion":
                    valor_midi = int(min(max(abs(valor), 0), 1) * 127)
                    enviar_cc(self.outport, self.cc_der, valor_midi)
                elif self.modo_der_var.get() == "boton" and not self.pedal_der_activo:
                    self.toggle_der = not self.toggle_der
                    enviar_cc(self.outport, self.cc_der, 127 if self.toggle_der else 0)
                    self.pedal_der_activo = True
            elif abs(valor) < self.umbral_lib:
                self.pedal_der_activo = False

            time.sleep(0.01)