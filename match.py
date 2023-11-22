import os
import asyncio
import threading
from tkinter import *
import sounddevice as sd
from shazamio import Shazam
from tkinter import messagebox  
from scipy.io.wavfile import write


# =============== utilities =================

def list_audio_devices():
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"Device {i}: {device['name']}")
        print(f"  Channels: {device['max_input_channels']}")
        print(f"  Sample Rate: {device['default_samplerate']}")
        print()

async def recognize_song(file_path, window):
    shazam = Shazam()
    recognize_result = await shazam.recognize_song(file_path)

    if recognize_result.get('track'):
        track_info = recognize_result['track']
        song_title = track_info.get('title')
        artist_name = track_info.get('subtitle')
        if song_title and artist_name:
            messagebox.showinfo("Resultado", f"Artista: {artist_name}\nMúsica: {song_title}", parent=window)
        else:
            messagebox.showinfo("Resultado", "Informações da música não encontradas.", parent=window)
    else:
        messagebox.showinfo("Resultado", "Nenhuma música reconhecida.", parent=window)
    
    os.remove(file_path)
    reativar_botao()

def reativar_botao():
    atualizar_estado_do_botao(False)
    janela.update_idletasks()
    janela.update()   
    
def record_audio(device_name, duration, sample_rate, channels):
    device_index = None
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if d['name'] == device_name:
            device_index = i
            break

    if device_index is None:
        print("Dispositivo de gravação não encontrado.")
        return

    print("Gravando áudio...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, device=device_index)
    sd.wait()
    print("Gravação finalizada")
    return audio

def atualizar_estado_do_botao(gravando):
    if gravando:
        botao_iniciar.config(text="Gravando...", state="disabled", bg='#FF0000')
    else:
        botao_iniciar.config(text="Iniciar Gravação", state="normal", bg='#111e3f')

def iniciar():
    selected_device_name = selected_device.get()  # Get selected device name from OptionMenu
    atualizar_estado_do_botao(True)
    texto_resposta["text"] = ""
    
    #forcar atualizacao da janela
    janela.update_idletasks()
    janela.update()
    
    duration = 10  # Duration in seconds
    sample_rate = 44100  # Sample rate for recording
    channels = 1  # Mono audio

    audio = record_audio(selected_device_name, duration, sample_rate, channels)
    if audio is not None:
        file_path = "temp_audio.wav"
        write(file_path, sample_rate, audio)
        # analisar áudio de forma assíncrona em uma outra thread.
        threading.Thread(target=lambda: asyncio.run(recognize_song(file_path, janela))).start()
    else:
        atualizar_estado_do_botao(False)  # Se a gravação falhar, reativa o botão.





# ================= interface ===============  

# Tkinter GUI
janela = Tk()
janela.title("Match songs!!")
janela.geometry("400x600")
janela.configure(bg='#111e3f')

# icone
icone = PhotoImage(file='teste.png') 
janela.iconphoto(True, icone)

texto = Label(janela, text="MATCH", bg='#111e3f', fg='white', font=("ARIAL BOLD", 40))
texto.pack(pady=120)  

texto2 = Label(janela, text="Identifique o que está tocando", bg='#111e3f', fg='white', font=("Helvetica", 15))
texto2.pack(pady=10)  

botao_iniciar = Button(janela, text="Iniciar Gravação", command=iniciar, bg='#111e3f', fg='black')
botao_iniciar.pack(pady=5)  

texto_resposta = Label(janela, text="", bg='#111e3f', fg='white')
texto_resposta.pack(pady=70)  

selected_device = StringVar(janela)
devices = sd.query_devices()
input_device_names = [device['name'] for device in devices if device['max_input_channels'] > 0]

device_menu_label = Label(janela, text="Selecione o dispositivo de áudio:", bg='#111e3f', fg='white')
device_menu_label.pack(pady=0)  

device_menu = OptionMenu(janela, selected_device, *input_device_names)
device_menu.configure(bg='gray', fg='white')
device_menu.pack(pady=5)  

if input_device_names:
    selected_device.set(input_device_names[0])

janela.mainloop()

