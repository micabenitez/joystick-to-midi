import mido
from mido import Message

def abrir_puerto(nombre_puerto="loopMIDI Port 3"):
    try:
        outport = mido.open_output(nombre_puerto)
        return outport
    except Exception as e:
        print(f"No se pudo abrir puerto MIDI: {e}")
        return None

def enviar_cc(outport, cc, valor):
    if outport is None:
        return
    msg = Message("control_change", control=cc, value=valor)
    outport.send(msg)