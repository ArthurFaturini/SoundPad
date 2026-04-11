import pyaudio
import wave
from keyboard import *
from time import sleep
import argparse
# import pydub
# import audioloop

# help(pyaudio)


audio = pyaudio.PyAudio()

# for dispostivos in range(1, audio.get_device_count(), 1):
#     print(audio.get_device_info_by_index(dispostivos).get('name'))
#     if "Voicemeeter Input" in audio.get_device_info_by_index(dispostivos).get('name') :
#         print(audio.get_device_info_by_index(dispostivos).get('index'))

output_device_index = 50

parser = argparse.ArgumentParser() # Ativando o argparse
parser.add_argument('--path', help='Caminho do arquivo') # Adicionando um argumento
args = parser.parse_args() # Armazenando os argumentos passados em uma variável

def playAudio():
    try:
        # file = wave.open("C:/Users/ArthurFaturini/Documents/Programacao/Soundpad/bolo_de_morango.wav", 'rb') 
        file = wave.open(args.path, 'rb') 

        stream = audio.open(format=audio.get_format_from_width(file.getsampwidth()),
            channels=file.getnchannels(),
            rate=file.getframerate(),
            output=True,
            output_device_index=output_device_index)

        data = file.readframes(1024)
        while data:
            stream.write(data)
            data = file.readframes(1024)
        stream.stop_stream()
        stream.close()
    except:
        print("[ERRO] TENTE NOVAMENTE!")


def main():
    while True:
        sleep(0.1)
        if is_pressed('ctrl+b'):
              playAudio()
        if is_pressed('ctrl+esc'):
            break

        
# Encerra a instância do pyaudio
# audio.terminate()

main()
