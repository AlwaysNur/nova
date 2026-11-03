import openwakeword
from openwakeword.model import Model
import pyaudio
import numpy as np
from pathlib import Path

model = Model(wakeword_model_paths=[str(Path(__file__).parent.parent / "hey_nova_20261027_035353.onnx")], vad_threshold=0.5)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = 1280  # 1280 samples = exactly 80ms of audio

p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK_SIZE
)

try:
    while True:
        raw_data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
    
        audio_chunk = np.frombuffer(raw_data, dtype=np.int16)
    
        prediction = model.predict(audio_chunk)
        
        for name, confidence in prediction.items():
            if confidence >= 0.6:
                print(f"Wake word detected: {name}")
                model.reset()
            
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
