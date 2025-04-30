import json
from datetime import datetime
import os

def load_today_log():
    today = datetime.now().strftime("%Y-%m-%d")
    logfile = os.path.join("sensor_logs", f"{today}.json")
    if not os.path.exists(logfile):
        return []

    with open(logfile, "r") as f:
        return json.load(f)

def summarise_log(log_entries):
    if not log_entries:
        return "There is no data for today yet."

    temps = [entry["temperature"] for entry in log_entries]
    humidities = [entry["humidity"] for entry in log_entries]
    lights = [entry["light"] for entry in log_entries]
    moistures = [entry["moisture"] for entry in log_entries]

    def describe_trend(values, label):
        start = values[0]
        end = values[-1]
        diff = end - start
        if abs(diff) < 1:
            return f"{label} stayed fairly stable"
        elif diff > 0:
            return f"{label} increased over the day"
        else:
            return f"{label} decreased gradually"

    summary_parts = [
        f"Today began with a temperature of {temps[0]}°C and ended at {temps[-1]}°C.",
        describe_trend(temps, "Temperature"),
        describe_trend(humidities, "Humidity"),
        describe_trend(lights, "Light levels"),
        describe_trend(moistures, "Soil moisture")
    ]

    return " ".join(summary_parts)

