import os
import sys
import subprocess
import string
import json
import pyaudio
import psutil
from pathlib import Path


def start_watchdog(original_device, is_voicemeeter_close):
    main_pid = str(os.getpid())
    # Chamamos o python para rodar o nosso arquivo externo
    # Passamos o PID e o nome do dispositivo como argumentos
    subprocess.Popen(
        [sys.executable, "engine/watchdog.py", main_pid, original_device, is_voicemeeter_close],
        creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
    )
    
    return None


# Aprimorar essa função!
def set_default_audio_device(device_name):
    # Pega o caminho da pasta onde o config.py está (pasta engine)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Sobe um nível para a raiz e entra na pasta do nircmd
    nircmd_path = os.path.join(BASE_DIR, "..", "nircmd-x64", "nircmd.exe")
    try:
        # Roda o comando via nircmd para mudar o dispositivo de som padrão
        subprocess.run([nircmd_path, "setdefaultsounddevice", device_name], check=True)
    except Exception as e:
        print(f"[ERRO] Não foi possível trocar o áudio: {e}")
    finally:
        return None


def check_voicemeeter_running():
    # Verifica se o voicemeeter está rodando
    for proc in psutil.process_iter(['name']):
        if "voicemeeter" in proc.info['name'].lower():
            return True
    return False


def find_in_all_drives(filepath):
    # 1. Identifica quais drives existem (C, D, E...)
    drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

    for drive in drives:
        # rglob faz a busca recursiva em todas as subpastas
        for path in Path(drive).rglob(filepath):
            return str(path) # Retorna o primeiro que encontrar
            
    return None


def find_input_device():
    # Instancia a classe do Pyaudio brevemente
    audio = pyaudio.PyAudio()

    # Instancia o nome do dispositivo padrão do voicemeeter e o sample rate dele
    defaultNameInputDevice = "Voicemeeter Input (VB-Audio Voicemeeter VAIO)"
    defaultSampleRate = 48000.0

    try:
        for devices in range(1, audio.get_device_count(), 1):
            if defaultNameInputDevice in audio.get_device_info_by_index(devices).get('name') and defaultSampleRate == audio.get_device_info_by_index(devices).get('defaultSampleRate'):
                idDevice = audio.get_device_info_by_index(devices).get('index')
        return idDevice
    except:
        return None
    finally:
        audio.terminate()

            
def start_voicemeeter(voicemeeterPath):
    # Inicia o VoiceMeeter em paralelo com o código, ou seja, o código não para
    return subprocess.Popen([f"{voicemeeterPath}"])


def build_json():
    targetFile = "voicemeeterpro_x64.exe" # Aplicativo padrão que será utilizado
    voicemeeterPath = find_in_all_drives(targetFile) # Retornando o caminho do VoiceMeeter
    idInputDevice = find_input_device() # Retorna o id do dispositivo padrão do Voicemeeter

    # Layout padrão do config.json
    defaultJsonConfig = {"voicemeeter_path": voicemeeterPath,
                         "input_device_settings": {
                            "default_id": idInputDevice,
                            "default_name": "Voicemeeter Input (VB-Audio Voicemeeter VAIO)",
                            "last_used_id": idInputDevice,
                            "last_used_name": "Voicemeeter Input (VB-Audio Voicemeeter VAIO)"
                        },
                        "output_device_settings":{
                            "default_name": "Alto-falantes",
                            "voicemeeter_name": "Voicemeeter Input"
                        },
                        "hotkeys": {
                            "<ctrl>+b": "bolo_de_morango.wav"
                        },
                        "personalized_user_options":{
                            "voicemeeter_close_when_app_close": "True"
                        }
                        }
    # Criando o config.json
    with open('config.json', 'w', encoding="utf-8") as configWrite:
        json.dump(defaultJsonConfig, configWrite, indent=4, ensure_ascii=False)
    
    return defaultJsonConfig
    

def read_json():
    file_path = "config.json"

    try:
        if not os.path.exists(file_path):
            # Se o config.json não existir ele já cria o config.json padrão
            return build_json()

        with open(file_path, 'r', encoding='utf-8') as configRead: # Abre o config.json
            json_object = json.load(configRead) # Lê o config.json
            return json_object

    except Exception as e:
        # Caso não exista o arquivo ou ocorra algum erro, ele criará de novo o JSON
        return build_json()
