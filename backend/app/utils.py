# app/utils.py
import os
from werkzeug.utils import secure_filename
from shazamio import Shazam

def save_audio_file(audio_file):
    filename = secure_filename(audio_file.filename)
    if not os.path.exists('uploads'):
        os.mkdir('uploads')
    audio_path = os.path.join('uploads', filename)
    audio_file.save(audio_path)
    return audio_path

async def recognize_song(file_path):
    shazam = Shazam()
    recognize_result = await shazam.recognize_song(file_path)
    
    if recognize_result.get('track'):
        track_info = recognize_result['track']
        song_title = track_info.get('title')
        artist_name = track_info.get('subtitle')
        
        return {
            'artist': artist_name,
            'title': song_title
        }
    
    return {'error': 'No song recognized'}