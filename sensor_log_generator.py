import os
import json
import random
from datetime import datetime, timedelta

LOG_DIR = "sensor_logs"
os.makedirs(LOG_DIR, exist_ok=True)

def generate_fake_day(date, mood="neutral"):
    log = []
    for i in range(0, 10):  # from 8 AM to 5 PM (hour = 8–17)
        hour = 8 + i
        timestamp = datetime(date.year, date.month, date.day, hour).isoformat()

        # Generate variation depending on mood/season
        if mood == "bright_dry":
            temp = round(random.uniform(24, 30), 1)
            light = round(random.uniform(700, 1000), 1)
            humidity = round(random.uniform(30, 45), 1)
            moisture = round(random.uniform(25, 35), 1)

        elif mood == "stormy_humid":
            temp = round(random.uniform(18, 22), 1)
            light = round(random.uniform(100, 300), 1)
            humidity = round(random.uniform(75, 90), 1)
            moisture = round(random.uniform(40, 60), 1)

        elif mood == "cool_dim_to_warm":
            light = round(100 + (i * 50), 1)
            temp = round(16 + (i * 0.6), 1)
            humidity = round(60 - (i * 1.2), 1)
            moisture = round(random.uniform(35, 45), 1)

        elif mood == "autumn_dry":
            temp = round(random.uniform(14, 20), 1)
            light = round(random.uniform(200, 500), 1)
            humidity = round(random.uniform(30, 50), 1)
            moisture = round(random.uniform(20, 35), 1)

        elif mood == "winter_damp":
            temp = round(random.uniform(8, 14), 1)
            light = round(random.uniform(100, 300), 1)
            humidity = round(random.uniform(70, 90), 1)
            moisture = round(random.uniform(45, 60), 1)

        elif mood == "spring_grow":
            temp = round(random.uniform(18, 24), 1)
            light = round(random.uniform(500, 800), 1)
            humidity = round(random.uniform(55, 70), 1)
            moisture = round(random.uniform(35, 50), 1)

        elif mood == "summer_peak":
            temp = round(random.uniform(28, 34), 1)
            light = round(random.uniform(850, 1000), 1)
            humidity = round(random.uniform(30, 45), 1)
            moisture = round(random.uniform(20, 30), 1)

        else:  # default neutral
            temp = round(random.uniform(18, 26), 1)
            light = round(random.uniform(300, 700), 1)
            humidity = round(random.uniform(40, 65), 1)
            moisture = round(random.uniform(30, 50), 1)

        log.append({
            "timestamp": timestamp,
            "temperature": temp,
            "light": light,
            "humidity": humidity,
            "moisture": moisture
        })

    filename = os.path.join(LOG_DIR, f"{date.strftime('%Y-%m-%d')}.json")
    with open(filename, "w") as f:
        json.dump(log, f, indent=2)

# Generate logs for the last 7 days
today = datetime.today()
moods_7day = ["bright_dry", "stormy_humid", "cool_dim_to_warm", "neutral", "bright_dry", "stormy_humid", "neutral"]
for i in range(7):
    date = today - timedelta(days=i + 1)
    generate_fake_day(date, mood=moods_7day[i % len(moods_7day)])

# Generate logs for one day in each month, 12 months ago
monthly_moods = [
    "summer_peak", "summer_peak", "autumn_dry", "autumn_dry",
    "winter_damp", "winter_damp", "winter_damp", "spring_grow",
    "spring_grow", "spring_grow", "summer_peak", "summer_peak"
]
for month_offset in range(12):
    month = (month_offset % 12) + 1
    year = today.year - 1
    date = datetime(year=year, month=month, day=15)
    generate_fake_day(date, mood=monthly_moods[month_offset])
