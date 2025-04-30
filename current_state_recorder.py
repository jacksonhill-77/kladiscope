import json
import os
from datetime import datetime

STATE_FILE = "current_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "last_spoken": None,
            "last_mood": None,
            "last_prompt_time": None
        }

def update_state(last_spoken=None, last_mood=None):
    state = load_state()
    if last_spoken:
        state["last_spoken"] = last_spoken
    if last_mood:
        state["last_mood"] = last_mood
    state["last_prompt_time"] = datetime.now().isoformat()

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    return state

# Test
update_state(last_spoken="The light is soft today.", last_mood="content")
