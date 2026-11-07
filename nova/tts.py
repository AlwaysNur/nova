from pathlib import Path
from piper import PiperVoice, SynthesisConfig
import sounddevice as sd
import numpy as np

MODEL = Path(__file__).parent.parent / "models" / "en_US-hfc_female-medium.onnx"

voice = PiperVoice.load(str(MODEL))


def speak(text):
    for chunk in voice.synthesize(text):
        audio = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)

        sd.play(
            audio,
            samplerate=chunk.sample_rate,
            blocking=True
        )