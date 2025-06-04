import requests
import subprocess
import os
import time
from datetime import datetime
from openai_api_key import get_api_key

TTS_MODEL = "tts-1"
VOICE = "alloy"
MPV_PATH = "mpv"  # Assume mpv is globally available
LOG_DIR = "spoken_log"
os.makedirs(LOG_DIR, exist_ok=True)

def speak(text, log=True, play_audio=True):
    api_key = get_api_key()
    filename = "/tmp/response.mp3"  # Use temp path for faster I/O

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": TTS_MODEL,
        "input": text,
        "voice": VOICE
    }

    try:
        t0 = time.time()

        # Send request to OpenAI
        response = requests.post("https://api.openai.com/v1/audio/speech", headers=headers, json=data)
        response.raise_for_status()

        # Save audio file
        with open(filename, "wb") as f:
            f.write(response.content)

        t1 = time.time()

        # Log if required
        if log:
            with open(os.path.join(LOG_DIR, "spoken_log.txt"), "a", encoding="utf-8") as log_file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] {text}\n")

        # Play if needed
        if play_audio:
            print("🔊 Playing audio...")
            subprocess.run([MPV_PATH, "--no-terminal", filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        t2 = time.time()
        print(f"🕒 TTS time: {t1 - t0:.2f}s | Playback time: {t2 - t1:.2f}s")

        return filename

    except Exception as e:
        return f"Error during TTS: {e}"
