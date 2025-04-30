import requests
from openai_api_key import get_api_key

def transcribe_audio(filepath="input.wav"):
    api_key = get_api_key()
    with open(filepath, "rb") as audio_file:
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": audio_file},
            data={"model": "whisper-1"}
        )
    response.raise_for_status()
    return response.json()["text"]

# Test:
if __name__ == "__main__":
    text = transcribe_audio()
    print("🎧 Transcribed Input:", text)