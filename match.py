import os
import asyncio
import threading
from tkinter import *
import sounddevice as sd
from shazamio import Shazam
from tkinter import messagebox
from scipy.io.wavfile import write
from transformers import pipeline
from tkinter import Toplevel, Label, Button, font as tkFont
from PIL import Image, ImageTk
import requests
from PIL import Image, ImageTk 
from io import BytesIO


# =============== utilities =================

def list_audio_devices():
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"Device {i}: {device['name']}")
        print(f"  Channels: {device['max_input_channels']}")
        print(f"  Sample Rate: {device['default_samplerate']}")
        print()
        
        
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

def reativar_botao():
    atualizar_estado_do_botao(False)
    janela.update_idletasks()
    janela.update()   

async def recognize_song(file_path):
    shazam = Shazam()
    recognize_result = await shazam.recognize_song(file_path)

    if recognize_result.get('track'):
        track_info = recognize_result['track']
        print("Shazam info ok")
        return track_info
    
    os.remove(file_path)
    reativar_botao()
    
def transcrever_audio(file_path):
    try:
        pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small")
        result = pipe(file_path)
        print("Transcription ok")
        return result["text"]
    except Exception as e:
        print(f"Erro ao transcrever o áudio: {e}")
        return None

# Função que realiza a transcrição e o reconhecimento de em paralelo
def process_audio(file_path, window):
    transcription = transcrever_audio(file_path)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    recognition_result = loop.run_until_complete(recognize_song(file_path))

    # formatar os resultados
    song_title = recognition_result.get('title') if recognition_result else "não encontrada"
    artist_name = recognition_result.get('subtitle') if recognition_result else ""
    image_url = recognition_result['images']['background'] if recognition_result and 'images' in recognition_result and 'background' in recognition_result['images'] else None
    transcription_text = transcription if transcription else "não transcrita"

    # Exibir resultados
    # messagebox.showinfo(
    #     "Resultado",
    #     f"Transcrição do Áudio:\n{transcription_text}\n\nMúsica Encontrada:\nArtista: {artist_name}\nTítulo: {song_title}",
    #     parent=window
    # )

    show_custom_message_window(
    "Resultado",
    artist_name=artist_name,
    song_title=song_title,
    transcription_text=transcription_text,
    image_url=image_url
)
    
    os.remove(file_path)
    reativar_botao()
    print("End of process")


def show_custom_message_window(title, artist_name, song_title, transcription_text, image_url):
    # Cria uma nova janela
    message_window = Toplevel(janela)
    message_window.title("Resultado")
    message_window.geometry("700x450")
    
    # Centrando a janela na tela
    window_width = message_window.winfo_reqwidth()
    window_height = message_window.winfo_reqheight()
    position_right = int(message_window.winfo_screenwidth()/2 - window_width/2)
    position_down = int(message_window.winfo_screenheight()/2 - window_height/2)
    message_window.geometry(f"+{position_right}+{position_down}")
    
    # Aplica um estilo de fonte
    bold_font = tkFont.Font(family="Helvetica", size=15, weight="bold")
    italic_font = tkFont.Font(family="Helvetica", size=15, slant="italic")

    lbl_music_found = Label(message_window, text="\nMUSICA INFO:\n", font=bold_font)
    lbl_music_found.pack()

    # Verifica se a URL da imagem é válida
    if image_url is None or not image_url.startswith(('http://', 'https://')):
        print("URL da imagem inválida ou não fornecida.")
    else:
        # Tenta carregar a imagem do artista
        try:
            response = requests.get(image_url)
            # Verifica se a requisição teve sucesso
            if response.status_code == 200:
                artist_image = Image.open(BytesIO(response.content))
                artist_photo = ImageTk.PhotoImage(artist_image.resize((200, 200)))
                
                # Cria um label para a imagem do artista na janela
                image_label = Label(message_window, image=artist_photo)
                image_label.image = artist_photo  
                image_label.pack()
            else:
                print("Não foi possível carregar a imagem do artista.")
        except Exception as e:
            print(f"Ocorreu um erro ao baixar a imagem do artista: {e}")
    
    lbl_title = Label(message_window, text=f"Título: {song_title}", font=bold_font)
    lbl_title.pack()
    
    lbl_artist = Label(message_window, text=f"Artista: {artist_name}", font=italic_font)
    lbl_artist.pack()

    # Cria Labels para adicionar formatação ao texto
    lbl_transcription = Label(message_window, text="\nTRANSCRIÇAO DE AUDIO:", font=bold_font)
    lbl_transcription.pack(anchor='w', padx=5)

    # Caixa de texto da transcrição normal
    lbl_transcription_text = Label(message_window, text=transcription_text, font=italic_font)
    lbl_transcription_text.pack(anchor='w', padx=5)
    
    # Botão para fechar a janela
    btn_close = Button(message_window, text="Fechar", command=message_window.destroy)
    btn_close.pack(anchor='s', pady=10)
    
    #background 
    message_window.configure(bg='#1a1a1a')
    lbl_transcription.configure(bg='#1a1a1a', fg='white')
    lbl_transcription_text.configure(bg='#1a1a1a', fg='white')
    lbl_music_found.configure(bg='#1a1a1a', fg='white')
    lbl_artist.configure(bg='#1a1a1a', fg='white')
    lbl_title.configure(bg='#1a1a1a', fg='white')
    btn_close.configure(bg='#1a1a1a', fg='white')
    



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
        threading.Thread(target=process_audio, args=(file_path, janela)).start()
    else:
        atualizar_estado_do_botao(False) 



    
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

