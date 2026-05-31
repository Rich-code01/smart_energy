import json
import random
import time
from datetime import datetime, timedelta

import paho.mqtt.client as mqtt

# MQTT Broker Settings
BROKER = "localhost"
PORT = 1883

# Simulation Settings
NUM_METERS = 1000
INTERVAL_MINUTES = 5
SIMULATION_HOURS = 1

# Generate 1000 smart meter IDs (10-digit numbers)
meter_ids = [
    str(random.randint(1000000000, 9999999999))
    for _ in range(NUM_METERS)
]

# MQTT Client
client = mqtt.Client()
client.connect(BROKER, PORT, 60)

print("Connected to EMQX MQTT Broker")


def get_power_pattern(hour):
    """
    Simulate realistic power usage patterns:
    - Low usage at night
    - High usage morning and evening
    """

    # Night
    if 0 <= hour < 6:
        return random.uniform(0.3, 1.5)

    # Morning peak
    elif 6 <= hour < 10:
        return random.uniform(2.0, 5.5)

    # Daytime moderate
    elif 10 <= hour < 17:
        return random.uniform(1.0, 3.5)

    # Evening peak
    elif 17 <= hour < 22:
        return random.uniform(3.0, 7.0)

    # Late evening
    else:
        return random.uniform(1.0, 2.5)


# Number of intervals for 1 hour
intervals = int((SIMULATION_HOURS * 60) / INTERVAL_MINUTES)

# Simulation Start Time
current_time = datetime.utcnow()

print(f"Starting simulation for {NUM_METERS} meters...")
print(f"Total intervals: {intervals}")
print("-" * 50)

total_messages = 0

for interval in range(intervals):

    print(f"Interval {interval + 1}/{intervals}")

    for meter_id in meter_ids:

        hour = current_time.hour

        # Realistic power usage
        power = round(get_power_pattern(hour), 2)

        voltage = round(random.uniform(220, 240), 2)

        current = round(power * 1000 / voltage, 2)

        frequency = round(random.uniform(49.8, 50.2), 2)

        # Simulated cumulative energy usage
        energy = round(random.uniform(100, 5000), 2)

        payload = {
            "meter_id": meter_id,
            "timestamp": current_time.isoformat() + "Z",
            "power": power,
            "voltage": voltage,
            "current": current,
            "frequency": frequency,
            "energy": energy
        }

        topic = f"energy/meters/{meter_id}"

        client.publish(topic, json.dumps(payload))

        total_messages += 1

    print(f"Published {NUM_METERS} messages")
    print(f"Total messages so far: {total_messages}")

    # Move simulation time forward by 5 minutes
    current_time += timedelta(minutes=INTERVAL_MINUTES)

    # Wait before next batch
    time.sleep(2)

print("-" * 50)
print("Simulation completed")
print(f"Total messages published: {total_messages}")

client.disconnect()