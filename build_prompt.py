import json
import os
from datetime import datetime
from openai_api_key import get_api_key
from summarise_log import summarise_log  # assume you saved the summariser separately
from speak import speak  # assume you’ve imported the speak() function
from current_state_recorder import load_state, update_state  # load/update JSON memory

# === Simulated sensor snapshot for now ===
def get_current_sensor_data():
    return {
        "moisture": 34,
        "light": 470,
        "temperature": 22.5,
        "humidity": 60
    }

# === Load today's summary (if exists) ===
def get_today_summary():
    today = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join("sensor_logs", f"{today}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            log_data = json.load(f)
        return summarise_log(log_data)
    return "No sensor summary is available yet."

# === Build the full prompt for GPT ===
def build_prompt(user_input):
    state = load_state()
    sensor = get_current_sensor_data()
    summary = get_today_summary()

    prompt = f"""
You are Kladiscope, a friendly and slightly whimsical monstera plant. You speak in short, warm phrases, with a sense of stillness and natural wisdom.

Today's environmental summary:
{summary}

Current sensor readings:
- Soil moisture: {sensor['moisture']}%
- Light level: {sensor['light']} lux
- Temperature: {sensor['temperature']}°C
- Humidity: {sensor['humidity']}%

Last spoken: "{state['last_spoken']}" (Mood: {state['last_mood']}, Time: {state['last_prompt_time']})

Now the user asks: "{user_input}"

Respond like a living thing. Be gentle, observational, and brief—but not robotic.
"""

    return prompt, sensor

# Test builder with simulated input
prompt, sensor = build_prompt("How are you today?")
prompt[:1000]  # show a preview
