from faster_whisper import WhisperModel

print("Loading Whisper...")

model = WhisperModel(
    "small",
    device="cuda",
    compute_type="float16",
)

def transcribe(audio):
    segments, info = model.transcribe(
        audio,
        beam_size=5,
    )

    text = " ".join(segment.text for segment in segments)

    return text.strip()