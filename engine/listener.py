from pynput import keyboard
import threading
import player

def trigger_audio(path, device_index, audio_instance):
    # Esta função será executada dentro de uma nova Thread permitindo que o som toque sem travar o programa principal
    threading.Thread(
        target=player.play_audio, 
        args=(path, device_index, audio_instance),
        daemon=True # Daemon=True faz o som parar se o usuário fechar o programa principal
    ).start()

def start_hotkeys(hotkey_map, device_index, audio_instance):
    # Foi criado o dicionário de funções (bindings)
    # Agora o lambda chama o trigger_audio, que por sua vez cria a Thread
    bindings = {
        key: lambda p=path: trigger_audio(p, device_index, audio_instance) 
        for key, path in hotkey_map.items()
    }
    
    with keyboard.GlobalHotKeys(bindings) as listener:
        listener.join()
