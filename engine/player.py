import wave
import pyaudio
import argparse


def play_audio(path, device_index=50, audio_instance=None):
    # Verifica se a função foi chamada via cmd
    local_instance = False
    if audio_instance is None:
        # Por ser chamada via cmd é preciso instanciar a classe do PyAudio
        audio_instance = pyaudio.PyAudio()
        local_instance = True

    try:
        # Abre o arquivo de áudio a ser tocado
        file = wave.open(path, 'rb') 

        stream = audio_instance.open(format=audio_instance.get_format_from_width(file.getsampwidth()),
            channels=file.getnchannels(),
            rate=file.getframerate(),
            output=True,
            output_device_index=device_index)

        data = file.readframes(1024)
        while data:
            stream.write(data)
            data = file.readframes(1024)
    finally:
        # Encerra na memória o arquivo de áudio
        stream.stop_stream()
        stream.close()
        file.close()
        # Se a instância foi criada aqui dentro, fecha ela. 
        # Se veio do main, deixa quieto para não quebrar o app.
        if local_instance:
            audio_instance.terminate()

if __name__ == "__main__":
    parser = argparse.ArgumentParser() # Ativando o argparse
    parser.add_argument('--path', type=str, required=True, help='Caminho do arquivo') # Adicionando um argumento
    parser.add_argument('--device', type=int, default=50, help='Index do dispositivo') # Adicionando um argumento
    args = parser.parse_args() # Armazenando os argumentos passados em uma variável

    play_audio(path=args.path, device_index=args.device)
