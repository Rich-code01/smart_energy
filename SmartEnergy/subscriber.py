import json
import psycopg2
import paho.mqtt.client as mqtt

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="smart_energy",
    user="postgres",
    password="postgres",
    port="5433"
)

cursor = conn.cursor()

print("Connected to PostgreSQL")

# MQTT settings
BROKER = "localhost"
PORT = 1883
TOPIC = "energy/meters/#"

# MQTT connect callback
def on_connect(client, userdata, flags, reason_code, properties):

    if reason_code == 0:
        print("Connected to MQTT Broker!")

        client.subscribe(TOPIC)

        print(f"Subscribed to topic: {TOPIC}")

    else:
        print("Failed to connect")

# MQTT message callback
def on_message(client, userdata, msg):

    try:
        payload = msg.payload.decode()

        print("Received:", payload)

        data = json.loads(payload)

        query = """
        INSERT INTO energy_readings
        (meter_id, timestamp, power, voltage, current, frequency, energy)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            data["meter_id"],
            data["timestamp"],
            data["power"],
            data["voltage"],
            data["current"],
            data["frequency"],
            data["energy"]
        )

        cursor.execute(query, values)

        conn.commit()

        print("Data inserted successfully")

    except Exception as e:
        print("Error:", e)

# Create MQTT client (NEW API VERSION)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Attach callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker
client.connect(BROKER, PORT, 60)

print("Listening for MQTT messages...")

# Start loop
client.loop_forever()