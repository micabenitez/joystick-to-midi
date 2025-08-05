# Joystick To Midi

Aplicación que convierte movimientos de joystick en mensajes MIDI mediante una interfaz gráfica sencilla con CustomTkinter, usando pygame para joystick y mido para MIDI.

![Logo ControlToMidi](https://github.com/user-attachments/assets/dcfa6da1-e335-42fc-b557-3af72a4900f1)
---

## Características

- Controla dos ejes del joystick (izquierdo y derecho).
- Modos de funcionamiento para cada eje: **Botón (toggle)** o **Pedal (expresión)**.
- Configuración visual de los valores de Control Change (CC) para cada lado.
- Envío de mensajes MIDI a través de puerto LoopMIDI.
- Interfaz gráfica moderna y fácil de usar con CustomTkinter.
- Soporta Windows.

---

## Requisitos

- Python 3.8 o superior
- pygame
- mido
- python-rtmidi (recomendado para backend MIDI)
- customtkinter
- loopMIDI (para crear puerto MIDI virtual en Windows)
