import time
import wave
import numpy as np
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

SILENCE_THRESHOLD = 500
SILENCE_DURATION = 1.5


def record(file):
    OUTPUT_FILENAME = file
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    frames = []
    has_started_talking = False
    silence_start_time = None

    try:
        while True:

            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

            audio_data = np.frombuffer(data, dtype=np.int16)
            max_amplitude = np.max(np.abs(audio_data))

            # Phase 1: Wait for the speaker to start talking
            if not has_started_talking:
                if max_amplitude > SILENCE_THRESHOLD:
                    has_started_talking = True
                continue

            # Phase 2: Speaker is talking; look for the end of speech
            if max_amplitude < SILENCE_THRESHOLD:
                if silence_start_time is None:
                    silence_start_time = time.time()
                elif time.time() - silence_start_time >= SILENCE_DURATION:
                    break
            else:
                silence_start_time = None

    except KeyboardInterrupt:
        print("\nRecording stopped.")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    if frames:
        with wave.open(OUTPUT_FILENAME, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b"".join(frames))
    else:
        print("No audio recorded")
