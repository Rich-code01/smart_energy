from flask import Flask, render_template, jsonify
from db import get_connection

app = Flask(__name__)

# ---------------- DASHBOARD ----------------
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# ---------------- REAL TIME ----------------
@app.route("/api/realtime")
def realtime():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT meter_id, power, energy
        FROM energy_readings
        WHERE timestamp >= NOW() - INTERVAL '1 hour'
        ORDER BY timestamp DESC;
    """)

    data = cur.fetchall()
    conn.close()
    return jsonify(data)


# ---------------- DAILY ----------------
@app.route("/api/daily")
def daily():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            SUM(CASE WHEN timestamp::date = CURRENT_DATE THEN energy ELSE 0 END),
            SUM(CASE WHEN timestamp::date = CURRENT_DATE - INTERVAL '1 day' THEN energy ELSE 0 END)
        FROM energy_readings_day;
    """)

    row = cur.fetchone()
    conn.close()

    return jsonify({
        "today": row[0] or 0,
        "yesterday": row[1] or 0
    })


# ---------------- WEEKLY ----------------
@app.route("/api/weekly")
def weekly():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT time_bucket('1 day', timestamp), SUM(energy)
        FROM energy_readings_week
        WHERE timestamp >= NOW() - INTERVAL '7 days'
        GROUP BY 1
        ORDER BY 1;
    """)

    data = cur.fetchall()
    conn.close()
    return jsonify(data)


# ---------------- REGION ----------------
@app.route("/api/region")
def region():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT LEFT(meter_id::text, 1), SUM(energy)
        FROM energy_readings
        WHERE timestamp >= NOW() - INTERVAL '1 month'
        GROUP BY 1
        ORDER BY 1;
    """)

    data = cur.fetchall()
    conn.close()
    return jsonify(data)


# ---------------- PERFORMANCE ----------------
@app.route("/api/performance")
def performance():
    return jsonify({
        "query": {
            "raw": 288.82,
            "3h": 209.50,
            "day": 111.88,
            "week": 252.24
        }
    })


if __name__ == "__main__":
    app.run(debug=True)