# app/views.py
from flask import Blueprint, request, jsonify
import os
from .utils import save_audio_file, recognize_song
import asyncio  # necessário para executar a função assíncrona

views = Blueprint('views', __name__)

@views.route('/analyze', methods=['POST'])
def analyze_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    audio_path = save_audio_file(audio_file)

    # Executar recognize_song de forma assíncrona
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(recognize_song(audio_path))

    # Excluir o arquivo após a análise
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return jsonify(result)