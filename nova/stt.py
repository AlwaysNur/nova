import torch
from transformers import pipeline

print("Loading Whisper...")

device = "cuda" if torch.cuda.is_available() else "cpu"

transcriber = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base.en",
    device=device,
)

def transcribe(audio_file):
    result = transcriber(audio_file)
    return result["text"].strip()