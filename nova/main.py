from openwakeword.model import Model
import pyaudio
import numpy as np
from pathlib import Path
from agent import run_agent
from tts import speak
from stt import transcribe
from record import record
from playsound3 import playsound


model = Model(wakeword_model_paths=[str(Path(__file__).parent.parent / "models" / "hey_nova_20261027_035353.onnx")], vad_threshold=0.5)

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

                playsound(str(Path(__file__).parent.parent / "fxs" / "started.wav"),block=False)

                record("/tmp/nova_output.wav")

                playsound(str(Path(__file__).parent.parent / "fxs" / "stopped.wav"))

                text = transcribe("/tmp/nova_output.wav")

                print(text)
                response = run_agent(text)
                speak(response)
                print(response)
                
                model.reset()
            
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
