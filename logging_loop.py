import os
import json
from datetime import datetime
import random  # used to simulate sensor values for now

# === Settings ===
LOG_DIR = "sensor_logs"
os.makedirs(LOG_DIR, exist_ok=True)

def simulate_sensor_data():
    # Simulated readings (replace with real sensor calls later)
    return {
        "timestamp": datetime.now().isoformat(),
        "moisture": round(random.uniform(25, 40), 1),
        "light": round(random.uniform(200, 800), 1),
        "temperature": round(random.uniform(18, 28), 1),
        "humidity": round(random.uniform(40, 70), 1)
    }

def append_log_entry():
    today = datetime.now().strftime("%Y-%m-%d")
    logfile = os.path.join(LOG_DIR, f"{today}.json")

    data = simulate_sensor_data()

    if os.path.exists(logfile):
        with open(logfile, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(data)

    with open(logfile, "w") as f:
        json.dump(logs, f, indent=2)

    return data

# Run once for testing
append_log_entry()
