
import mido

print("Puertos de salida MIDI disponibles:")
for port in mido.get_output_names():
    print(port)