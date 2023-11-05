# pip install shazamio sounddevice scipy
import sounddevice as sd
from scipy.io.wavfile import write
import asyncio
from shazamio import Shazam
import os

def list_audio_devices():
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"Device {i}: {device['name']}")
        print(f"  Channels: {device['max_input_channels']}")
        print(f"  Sample Rate: {device['default_samplerate']}")
        print()

def select_audio_device():
    devices = sd.query_devices()
    valid_device_indices = [i for i, device in enumerate(devices) if device['max_input_channels'] > 0]
    
    if not valid_device_indices:
        print("Nenhum dispositivo de áudio de entrada encontrado.")
        return None
    
    print("Dispositivos de áudio de entrada disponíveis:")
    for i in valid_device_indices:
        print(f"{i}: {devices[i]['name']}")
    
    while True:
        selection = input("Selecione o número do dispositivo de áudio desejado: ")
        try:
            selection = int(selection)
            if selection in valid_device_indices:
                return selection
            else:
                print("Seleção inválida. Tente novamente.")
        except ValueError:
            print("Seleção inválida. Tente novamente.")

async def recognize_song(file_path):
    shazam = Shazam()
    recognize_result = await shazam.recognize_song(file_path)
    
    if recognize_result.get('track'):
        track_info = recognize_result['track']
        song_title = track_info.get('title')
        artist_name = track_info.get('subtitle')
        if song_title and artist_name:
            print(f"Artista: {artist_name}")
            print(f"Música: {song_title}")
        else:
            print("Informações da música não encontradas.")
    else:
        print("Nenhuma música reconhecida.")
    
    os.remove(file_path)

def record_audio(device_index, duration, sample_rate, channels):
    print("Gravando áudio...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, device=device_index)
    sd.wait()  # Aguarda a gravação ser concluída
    return audio

# Listar dispositivos de áudio disponíveis
list_audio_devices()

# Selecionar dispositivo de áudio
device_index = select_audio_device()
if device_index is None:
    exit()

# Configurações de gravação de áudio
duration = 10  # Duração da gravação em segundos
sample_rate = 44100  # Taxa de amostragem do áudio
channels = 1  # Número de canais de entrada (estéreo)

# Gravar áudio do dispositivo selecionado
audio = record_audio(device_index, duration, sample_rate, channels)

# Salvar o áudio em um arquivo temporário
file_path = "temp_audio.wav"
write(file_path, sample_rate, audio)

# Identificar a música
asyncio.run(recognize_song(file_path))
