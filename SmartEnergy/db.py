import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="smart_energy",
        user="postgres",
        password="postgres",
        port="5433"
    )