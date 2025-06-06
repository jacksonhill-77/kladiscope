# record_and_transcribe.py
import sounddevice as sd
import numpy as np
import whisper
import tempfile
import scipy.io.wavfile
import time
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU*")

fs = 44100
model_size = "base"  # try "tiny.en" next
model = whisper.load_model(model_size)  # ⬅️ Load ONCE here

def record_and_transcribe(seconds=5):
    print("🎙️ Listening...")

    # 🎙️ RECORD AUDIO
    record_start = time.time()
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()
    record_end = time.time()
    print(f"⏱️ Mic recording time: {record_end - record_start:.2f} seconds")

    # 💾 SAVE TO TEMP FILE
    save_start = time.time()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        scipy.io.wavfile.write(tmpfile.name, fs, recording)
        save_end = time.time()

        # 🧠 TRANSCRIBE
        transcribe_start = time.time()
        result = model.transcribe(tmpfile.name)
        transcribe_end = time.time()

    print(f"⏱️ Save to disk time: {save_end - save_start:.2f} seconds")
    print(f"⏱️ Whisper transcribe time: {transcribe_end - transcribe_start:.2f} seconds")
    print(f"🗣️ Transcript: {result['text'].strip()}")

    return result["text"].strip()
