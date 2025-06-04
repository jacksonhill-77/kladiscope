import whisper
import sounddevice as sd
import soundfile as sf

duration = 5  # seconds
samplerate = 16000
filename = "test_input.wav"

print("Recording...")
audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1)
sd.wait()

sf.write(filename, audio, samplerate)
print("Recording complete. Transcribing...")

model = whisper.load_model("base")
result = model.transcribe(filename)
print("Transcription:", result["text"])