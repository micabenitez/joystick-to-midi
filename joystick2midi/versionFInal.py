import customtkinter as ctk
import pygame
import threading
import time
import mido
from mido import Message

# Inicialización MIDI y joystick
pygame.init()
pygame.joystick.init()

cc_izq = 4
cc_der = 1

toggle_izq = False
toggle_der = False
pedal_izq_activo = False
pedal_der_activo = False

UMBRAL_ACTIVACION = 0.2
UMBRAL_LIBERACION = 0.1

CC_PRESETS = {
    "Midi": 4,
    "Sustain": 64,
    "Soft": 67,
    "Sostenuto": 66
}

# Setup joystick y MIDI
if pygame.joystick.get_count() == 0:
    print("No joystick encontrado")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

try:
    outport = mido.open_output("loopMIDI Port 3")
except:
    print("No se pudo abrir puerto MIDI")
    exit()

def leer_joystick(stop_event):
    global toggle_izq, toggle_der
    global pedal_izq_activo, pedal_der_activo, cc_izq, cc_der

    while not stop_event.is_set():
        pygame.event.pump()
        valor = joystick.get_axis(1)

        if valor > UMBRAL_ACTIVACION:
            if modo_izq_var.get() == "expresion":
                valor_midi = int(min(max(valor, 0), 1) * 127)
                outport.send(Message("control_change", control=cc_izq, value=valor_midi))
            elif modo_izq_var.get() == "boton" and not pedal_izq_activo:
                toggle_izq = not toggle_izq
                outport.send(Message("control_change", control=cc_izq, value=127 if toggle_izq else 0))
                pedal_izq_activo = True
        elif valor < UMBRAL_LIBERACION:
            pedal_izq_activo = False

        if valor < -UMBRAL_ACTIVACION:
            if modo_der_var.get() == "expresion":
                valor_midi = int(min(max(abs(valor), 0), 1) * 127)
                outport.send(Message("control_change", control=cc_der, value=valor_midi))
            elif modo_der_var.get() == "boton" and not pedal_der_activo:
                toggle_der = not toggle_der
                outport.send(Message("control_change", control=cc_der, value=127 if toggle_der else 0))
                pedal_der_activo = True
        elif abs(valor) < UMBRAL_LIBERACION:
            pedal_der_activo = False

        time.sleep(0.01)

# ------------------ GUI ------------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("ControlToMidi")
root.geometry("700x550")

modo_label_font = ("Arial", 14, "bold")
# Variables de modo y CC (visuales y funcionales)
modo_izq_var = ctk.StringVar(value="boton")
modo_der_var = ctk.StringVar(value="expresion")
# ----------- Funciones GUI ------------
def set_cc(lado, valor):
    global cc_izq, cc_der
    if lado == "izq":
        cc_izq = valor
    else:
        cc_der = valor
    actualizar_estilos()

def actualizar_estilos():
    # Actualizar visibilidad de frames CC
    if modo_izq_var.get() == "boton":
        cc_frame_izq.pack_forget()
    else:
        cc_frame_izq.pack(pady=5)

    if modo_der_var.get() == "boton":
        cc_frame_der.pack_forget()
    else:
        cc_frame_der.pack(pady=5)

    # Indicadores de estado
    lbl_estado_izq.configure(
        text=f"Modo: {'Pedal' if modo_izq_var.get() == 'expresion' else 'Botón'}"
             + (f" | CC: {cc_izq}" if modo_izq_var.get() == "expresion" else "")
    )
    lbl_estado_der.configure(
        text=f"Modo: {'Pedal' if modo_der_var.get() == 'expresion' else 'Botón'}"
             + (f" | CC: {cc_der}" if modo_der_var.get() == "expresion" else "")
    )

    resumen_texto = (
        f"Lado Izquierdo: {modo_izq_var.get().capitalize()}"
        + (f" (CC {cc_izq})" if modo_izq_var.get() == "expresion" else "") + "   |   "
        f"Lado Derecho: {modo_der_var.get().capitalize()}"
        + (f" (CC {cc_der})" if modo_der_var.get() == "expresion" else "")
    )
    resumen_label.configure(text=resumen_texto)

# ---------- Títulos ----------
ctk.CTkLabel(root, text="Joystick To Midi", font=("Arial", 28, "bold")).pack(pady=(15, 5))
ctk.CTkLabel(root, text="PEDALES", font=modo_label_font).pack(pady=(0, 10))

# ---------- Contenedor principal ----------
main_frame = ctk.CTkFrame(root)
main_frame.pack(expand=True, fill="both", padx=20, pady=10)
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# ---------- Frame IZQ ----------
frame_izq = ctk.CTkFrame(main_frame, width=250, height=300)
frame_izq.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
frame_izq.pack_propagate(False)

ctk.CTkLabel(frame_izq, text="IZQUIERDA", font=modo_label_font).pack(pady=(10, 5))

# Modo botones lado IZQ
modo_frame_izq = ctk.CTkFrame(frame_izq, fg_color="transparent")
modo_frame_izq.pack(pady=5)
ctk.CTkRadioButton(modo_frame_izq, text="Botón", variable=modo_izq_var,
                   value="boton", command=actualizar_estilos).pack(side="left", padx=5)
ctk.CTkRadioButton(modo_frame_izq, text="Pedal", variable=modo_izq_var,
                   value="expresion", command=actualizar_estilos).pack(side="left", padx=5)

lbl_estado_izq = ctk.CTkLabel(frame_izq, text="", font=("Arial", 12))
lbl_estado_izq.pack(pady=(5, 0))

cc_frame_izq = ctk.CTkFrame(frame_izq)
for nombre, valor in CC_PRESETS.items():
    ctk.CTkButton(cc_frame_izq, text=nombre, width=150,
                  command=lambda v=valor: set_cc("izq", v)).pack(pady=2)

# ---------- Frame DER ----------
frame_der = ctk.CTkFrame(main_frame, width=250, height=300)
frame_der.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
frame_der.pack_propagate(False)

ctk.CTkLabel(frame_der, text="DERECHA", font=modo_label_font).pack(pady=(10, 5))
modo_frame_der = ctk.CTkFrame(frame_der, fg_color="transparent")
modo_frame_der.pack(pady=5)

ctk.CTkRadioButton(modo_frame_der, text="Botón", variable=modo_der_var,
                   value="boton", command=actualizar_estilos).pack(side="left", padx=5)
ctk.CTkRadioButton(modo_frame_der, text="Pedal", variable=modo_der_var,
                   value="expresion", command=actualizar_estilos).pack(side="left", padx=5)

lbl_estado_der = ctk.CTkLabel(frame_der, text="", font=("Arial", 12))
lbl_estado_der.pack(pady=(5, 0))

cc_frame_der = ctk.CTkFrame(frame_der)
for nombre, valor in CC_PRESETS.items():
    v_real = valor if nombre != "Midi" else 1
    ctk.CTkButton(cc_frame_der, text=nombre, width=150,
                  command=lambda v=v_real: set_cc("der", v)).pack(pady=2)

# ---------- Resumen inferior ----------
resumen_label = ctk.CTkLabel(root, text="", font=("Arial", 12, "italic"))
resumen_label.pack(pady=(10, 15))

# ---------- Iniciar GUI y joystick ----------
actualizar_estilos()

stop_event = threading.Event()
hilo = threading.Thread(target=leer_joystick, args=(stop_event,), daemon=True)
hilo.start()

def cerrar():
    stop_event.set()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", cerrar)
root.mainloop()
