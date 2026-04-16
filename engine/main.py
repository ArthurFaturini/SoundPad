import config
import listener
import pyaudio
from time import sleep

audio = pyaudio.PyAudio() # Instancia a classe do PyAudio

# Função principal
def main():
    try:
        print("-=-=-=-=-=- SOUNDPAD ENGINE STARTING -=-=-=-=-=-")
        # 1. Carrega as configurações
        configurations = config.read_json()
        if not configurations:
            print("ERROR: Could not load configurations.")
            return

        # Instancia o dispositivo padrão original
        original_device = configurations["output_device_settings"]["default_name"]
        # Instancia o dispostivo padrão utilizado pelo Voicemeeter 
        voicemeeter_device = configurations["output_device_settings"]["voicemeeter_name"]

        # Instancia se a configuração do usuário se quer fechar o voicemeeter quando o aplicativo encerra
        is_voicemeeter_close = configurations["personalized_user_options"]["voicemeeter_close_when_app_close"]

        # Inicializa o WATCHDOG
        config.start_watchdog(original_device, is_voicemeeter_close)

        # 2. Inicializa o Voicemeeter
        # Verifica se o Voicemeeter já está rodando, caso o usuário já utilize
        if not config.check_voicemeeter_running():
            config.start_voicemeeter(configurations['voicemeeter_path'])
            sleep(5.3) # Tempo de espera até o voicemeeter iniciar => VER MELHOR ISSO AQUI DEPOIS
        else:
            print("Voicemeeter já está em execução. Ignorando inicialização.")

        # Define o dispositivo do voicemeeter como padrão
        config.set_default_audio_device(voicemeeter_device)

        # 3. Inicializa o listener
        # Instancia os atalhos para tocar os áudios do usuário
        hotkeys = configurations["hotkeys"]
        # Instancia o index do dispositivo do voicemeeter
        device_index = configurations["input_device_settings"]["default_id"]
        listener.start_hotkeys(hotkeys, device_index, audio)
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        # O FINALLY garante o SHUTDOWN mesmo se o código quebrar ou for fechado
        if audio:
            audio.terminate()
        

if __name__ == "__main__":
    main()
