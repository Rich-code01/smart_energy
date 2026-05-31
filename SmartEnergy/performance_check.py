import psycopg2
import time

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
conn = psycopg2.connect(
    host="localhost",
    database="smart_energy",
    user="postgres",
    password="postgres",
    port="5433"
)

cur = conn.cursor()

# -----------------------------
# QUERIES
# -----------------------------
raw_query = """
SELECT meter_id,
       time_bucket('15 minutes', timestamp) AS bucket,
       AVG(power) as avg_power
FROM energy_readings
WHERE timestamp >= NOW() - INTERVAL '1 day'
AND meter_id = '123'
GROUP BY meter_id, bucket
ORDER BY bucket;
"""

agg_query = """
SELECT meter_id, bucket, avg_power
FROM energy_readings_15min
WHERE bucket >= NOW() - INTERVAL '1 day'
AND meter_id = '123'
ORDER BY bucket;
"""

# -----------------------------
# FUNCTION TO MEASURE TIME
# -----------------------------
def measure(query, runs=5):
    times = []

    for i in range(runs):
        start = time.time()

        cur.execute(query)
        cur.fetchall()   # force execution

        end = time.time()

        duration_ms = (end - start) * 1000
        times.append(duration_ms)

        print(f"Run {i+1}: {duration_ms:.2f} ms")

    avg = sum(times) / len(times)
    return avg


# -----------------------------
# RUN BENCHMARK
# -----------------------------
print("\n RAW QUERY PERFORMANCE")
raw_avg = measure(raw_query)

print("\n AGGREGATED VIEW PERFORMANCE")
agg_avg = measure(agg_query)

# -----------------------------
# RESULTS SUMMARY
# -----------------------------
print("\n==============================")
print("FINAL PERFORMANCE COMPARISON")
print("==============================")

print(f"Raw Query Avg:        {raw_avg:.2f} ms")
print(f"Aggregated View Avg:  {agg_avg:.2f} ms")

improvement = ((raw_avg - agg_avg) / raw_avg) * 100

print(f"Improvement:          {improvement:.2f}% faster")