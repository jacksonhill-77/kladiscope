# record_and_transcribe.py
import sounddevice as sd
import numpy as np
import whisper
import tempfile
import scipy.io.wavfile

def record_and_transcribe(seconds=5, model_size="base"):
    print("🎙️ Listening...")

    fs = 44100
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        scipy.io.wavfile.write(tmpfile.name, fs, recording)
        model = whisper.load_model(model_size)
        result = model.transcribe(tmpfile.name)
        return result["text"]
