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

## Modos de Funcionamiento de los Pedales MIDI

### Modo Botón (Toggle)

- Funciona como un interruptor: al pisar activa (envía valor MIDI 127) y al pisar de nuevo desactiva (envía valor 0).
- Ideal para controlar funciones binarias como:
  - Encender o apagar efectos.
  - Activar loops o secuencias.
  - Silenciar pistas.

### Modo Pedal (Expresión)

- Permite un control gradual según la posición del pedal.
- Envía valores MIDI proporcionales (0 a 127) según cuánto se pisa el pedal.
- Útil para controlar parámetros con variación continua, como:
  - Volumen.
  - Intensidad de efectos (reverberación, delay).
  - Tono o modulación.

### Opciones de Control Change (CC) en Modo Pedal (Expresión)

#### Pedal Izquierdo

- **MIDI (CC 4):** Personalizable para cualquier función, evita interferencias.
- **Sustain (CC 64):** Simula pedal de sustain, mantiene notas sonando.
- **Soft (CC 67):** Reduce volumen y brillo para un tono más suave.
- **Sostenuto (CC 66):** Mantiene notas tocadas al pisar el pedal.

#### Pedal Derecho

- Igual que el izquierdo, pero el CC personalizable es:
- **MIDI (CC 1):** Usado comúnmente para modulación (Mod Wheel).

---

## Requisitos

- Python 3.8 o superior
- pygame
- mido
- python-rtmidi (recomendado para backend MIDI)
- customtkinter
- loopMIDI (para crear puerto MIDI virtual en Windows)
