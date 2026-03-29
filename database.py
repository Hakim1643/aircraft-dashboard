import sqlite3

def create_database():
    conn = sqlite3.connect("flights.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        icao24 TEXT,
        callsign TEXT,
        latitude REAL,
        longitude REAL,
        altitude REAL,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database created successfully.")