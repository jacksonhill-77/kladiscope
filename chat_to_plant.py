import requests
from openai_api_key import get_api_key
from build_prompt import build_prompt
from speak import speak
from current_state_recorder import update_state

# === Chat to Plant Handler ===
def chat_to_plant(user_input):
    prompt, sensor = build_prompt(user_input)

    # GPT call setup
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
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]

        # Speak and update state
        speak(reply)
        update_state(last_spoken=reply, last_mood="neutral")  # You could infer mood from sensor or GPT response
        return reply

    except Exception as e:
        return f"Error talking to plant: {e}"

if __name__ == "__main__":
    response = chat_to_plant("How are you feeling today?")
    print("\n🌿 Kladiscope says:", response)

# Example use:
# chat_to_plant("How are you today?")
