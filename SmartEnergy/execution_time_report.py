import psycopg2
import time
conn = psycopg2.connect(
    host="127.0.0.1",
    database="smart_energy",
    user="postgres",
    password="postgres",
    port="5433"
)
cursor = conn.cursor()
tables = [
    "energy_readings_3h",
    "energy_readings_day",
    "energy_readings_week"
]

query = """
SELECT meter_id, SUM(energy)
FROM {}
WHERE timestamp >= NOW() - INTERVAL '7 days'
GROUP BY meter_id;
"""

results = []

for table in tables:
    start = time.time()
    cursor.execute(query.format(table))
    cursor.fetchall()
    end = time.time()

    results.append((table, round((end - start) * 1000, 2)))

print("\nExecution Times (ms)")
print("--------------------")
for r in results:
    print(r[0], ":", r[1], "ms")

cursor.close()
conn.close()