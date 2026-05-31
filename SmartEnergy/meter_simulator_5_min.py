import json
import random
import time
from datetime import datetime
import paho.mqtt.client as mqtt

# MQTT Broker Settings
BROKER = "localhost"
PORT = 1883

# Number of smart meters
NUM_METERS = 1000

# Generate 1000 unique 10-digit meter IDs
meter_ids = [str(1000000000 + i) for i in range(NUM_METERS)]

# Create MQTT client
client = mqtt.Client()

# Connect to EMQX
client.connect(BROKER, PORT, 60)

print("Connected to MQTT Broker")

# Function to simulate realistic power usage
def generate_power(hour):

    # Low usage at night
    if 0 <= hour < 6:
        return random.uniform(0.2, 1.5)

    # Morning peak
    elif 6 <= hour < 10:
        return random.uniform(2.0, 5.0)

    # Daytime moderate
    elif 10 <= hour < 17:
        return random.uniform(1.0, 3.0)

    # Evening peak
    elif 17 <= hour < 22:
        return random.uniform(3.0, 6.0)

    # Late evening
    else:
        return random.uniform(0.5, 2.0)

# Run simulation for 1 hour
# Every 5 minutes = 12 cycles
for cycle in range(12):

    current_time = datetime.now()
    current_hour = current_time.hour

    print(f"\nCycle {cycle + 1}/12")
    print("Timestamp:", current_time)

    for meter_id in meter_ids:

        power = round(generate_power(current_hour), 2)

        voltage = round(random.uniform(215, 240), 2)

        current = round(power / voltage * 1000, 2)

        frequency = round(random.uniform(49.8, 50.2), 2)

        energy = round(power * random.uniform(0.8, 1.5), 2)

        payload = {
            "meter_id": meter_id,
            "timestamp": current_time.isoformat(),
            "power": power,
            "voltage": voltage,
            "current": current,
            "frequency": frequency,
            "energy": energy
        }

        topic = f"energy/meters/{meter_id}"

        client.publish(topic, json.dumps(payload))

        print(f"Published -> {meter_id}")

    print("\nWaiting 5 minutes...\n")

    # Wait 5 minutes
    time.sleep(300)

print("Simulation completed")