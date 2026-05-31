import json
import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "localhost"
PORT = 1883
TOPIC = "energy/meters/1234567890"

client = mqtt.Client()

client.connect(BROKER, PORT, 60)

data = {
    "meter_id": "1234567890",
    "timestamp": datetime.now().isoformat(),
    "power": 250.5,
    "voltage": 220.0,
    "current": 1.14,
    "frequency": 50.0,
    "energy": 1250.7
}

client.publish(TOPIC, json.dumps(data))

print("Test data published successfully")