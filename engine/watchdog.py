import sys
import psutil
import time
import subprocess
import config

def cleanup(original_device, is_voicemeeter_close):
    try:
        # 1. Mata o Voicemeeter se o usuário quiser via config.json
        if is_voicemeeter_close:
            subprocess.run(
                ["taskkill", "/f", "/im", "voicemeeterpro_x64.exe"],
                creationflags=subprocess.CREATE_NO_WINDOW, # Não cria uma janela de console
                stdout=subprocess.DEVNULL, # Descarta a mensagem de sucesso
                stderr=subprocess.DEVNULL  # Descarta a mensagem de erro (se já estiver fechado)
            )
        # 2. Reseta o dispositivo padrão de áudio original do usuário via NirCmd
        config.set_default_audio_device(original_device)
    except Exception as e:
        print("")

if __name__ == "__main__":
    try:
        # Recebe o PID e o Nome do Dispositivo via argumentos
        # Ex: python watchdog.py 1234 "Alto-falantes"
        main_pid = int(sys.argv[1])
        device_name = sys.argv[2]
        # Variável de controle para saber se o usuário quer fechar o voicemeeter quando o aplicativo encerra
        is_voicemeeter_close = bool(sys.argv[3])

        # Monitora enquanto o PID do main existir
        while psutil.pid_exists(main_pid):
            time.sleep(1)

        # Caso o programa principal encerre, o watchdog encerrar os processos zumbis
        cleanup(device_name, is_voicemeeter_close)
    except Exception as e:
        print()