import time
import requests
from openai_api_key import get_api_key
from build_prompt import build_prompt
from speak import speak
from current_state_recorder import update_state
from record_and_transcribe import record_and_transcribe, preload_model


# === Chat to Plant Handler ===
def chat_to_plant(user_input):
    prompt, sensor = build_prompt(user_input)

    api_key = get_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4.1-nano",
        "messages": [
            {"role": "system", "content": "You are a monstera plant. You speak gently, with a sense of stillness and natural wisdom."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        gpt_start = time.time()
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        gpt_end = time.time()
        print(f"⏱️ GPT response time: {gpt_end - gpt_start:.2f} seconds")

        # Speak
        speak_start = time.time()
        speak(reply)
        speak_end = time.time()
        print(f"⏱️ TTS + playback time: {speak_end - speak_start:.2f} seconds")

        update_state(last_spoken=reply, last_mood="neutral")
        return reply

    except Exception as e:
        return f"Error talking to plant: {e}"

if __name__ == "__main__":
    preload_model("tiny")
    full_start = time.time()
    print("🎙️ Listening...")
    record_start = time.time()
    user_input = record_and_transcribe()
    record_end = time.time()
    print(f"⏱️ Recording + STT time: {record_end - record_start:.2f} seconds")

    response = chat_to_plant(user_input)
    full_end = time.time()

    print("\n🌿 Kladiscope says:", response)
    print(f"⏱️ Total round trip time: {full_end - full_start:.2f} seconds")
