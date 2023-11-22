# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small")

audio = "audio1.wav"

result = pipe(audio)

print(result["text"])