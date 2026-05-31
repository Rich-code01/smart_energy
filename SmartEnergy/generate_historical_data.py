import random
from datetime import datetime, timedelta

import psycopg2
from psycopg2.extras import execute_values

# PostgreSQL connection
conn = psycopg2.connect(
    host="127.0.0.1",
    database="smart_energy",
    user="postgres",
    password="postgres",
    port="5433"
)

cursor = conn.cursor()

print("Connected to PostgreSQL")

# Simulation settings
NUM_METERS = 1000
DAYS = 28
INTERVAL_MINUTES = 5
BATCH_SIZE = 10000

# Generate 1000 unique 10-digit meter IDs
meter_ids = [
    str(1000000000 + i)
    for i in range(NUM_METERS)
]

# Time range
end_time = datetime.utcnow()
start_time = end_time - timedelta(days=DAYS)

current_time = start_time

# Total rows counter
total_rows = 0

# Function for realistic usage patterns
def get_power_pattern(hour):

    # Night
    if 0 <= hour < 6:
        return random.uniform(0.3, 1.5)

    # Morning peak
    elif 6 <= hour < 10:
        return random.uniform(2.0, 5.5)

    # Daytime
    elif 10 <= hour < 17:
        return random.uniform(1.0, 3.5)

    # Evening peak
    elif 17 <= hour < 22:
        return random.uniform(3.0, 7.0)

    # Late evening
    else:
        return random.uniform(1.0, 2.5)


print("Generating historical data...")
print(f"Start Time: {start_time}")
print(f"End Time:   {end_time}")
print("-" * 60)

batch = []

while current_time < end_time:

    hour = current_time.hour

    for meter_id in meter_ids:

        power = round(get_power_pattern(hour), 2)

        voltage = round(random.uniform(220, 240), 2)

        current = round((power * 1000) / voltage, 2)

        frequency = round(random.uniform(49.8, 50.2), 2)

        # Simulated cumulative energy
        energy = round(random.uniform(100, 10000), 2)

        batch.append((
            meter_id,
            current_time,
            power,
            voltage,
            current,
            frequency,
            energy
        ))

        total_rows += 1

        # Insert batch into PostgreSQL
        if len(batch) >= BATCH_SIZE:

            execute_values(
                cursor,
                """
                INSERT INTO energy_readings
                (
                    meter_id,
                    timestamp,
                    power,
                    voltage,
                    current,
                    frequency,
                    energy
                )
                VALUES %s
                """,
                batch
            )

            conn.commit()

            print(f"Inserted rows: {total_rows}")

            batch = []

    # Move forward by 5 minutes
    current_time += timedelta(minutes=INTERVAL_MINUTES)

# Insert remaining rows
if batch:

    execute_values(
        cursor,
        """
        INSERT INTO energy_readings
        (
            meter_id,
            timestamp,
            power,
            voltage,
            current,
            frequency,
            energy
        )
        VALUES %s
        """,
        batch
    )

    conn.commit()

print("-" * 60)
print("Historical data generation completed")
print(f"Total rows inserted: {total_rows}")

cursor.close()
conn.close()