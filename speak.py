import requests
import subprocess
import os
from datetime import datetime
from openai_api_key import get_api_key

TTS_MODEL = "tts-1"
VOICE = "alloy"
MPV_PATH = r"mpv"
LOG_DIR = "spoken_log"
os.makedirs(LOG_DIR, exist_ok=True)

def speak(text, log=True, play_audio=True):
    api_key = get_api_key()
    filename = "response.mp3"  # Always overwritten

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
        response = requests.post("https://api.openai.com/v1/audio/speech", headers=headers, json=data)
        response.raise_for_status()

        with open(filename, "wb") as f:
            f.write(response.content)

        if log:
            with open(os.path.join(LOG_DIR, "spoken_log.txt"), "a", encoding="utf-8") as log_file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] {text}\n")

        if play_audio:
            print("🔊 Playing audio via mpv...")
            subprocess.run(["mpv", filename])

        return filename

    except Exception as e:
        return f"Error during TTS: {e}"
