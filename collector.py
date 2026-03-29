import requests
import sqlite3
import schedule
import time
from datetime import datetime

# Perak area boundaries
MIN_LAT = 3.5
MAX_LAT = 5.8
MIN_LON = 100.0
MAX_LON = 101.8

def get_aircraft_data():

    url = "https://opensky-network.org/api/states/all"

    try:

        response = requests.get(
            url,
            timeout=10
        )

        # ============================
        # SUCCESS RESPONSE
        # ============================

        if response.status_code == 200:

            data = response.json()

            states = data.get("states", [])

            print("API Success:", len(states), "records received")

            save_to_database(states)

        # ============================
        # RATE LIMIT ERROR
        # ============================

        elif response.status_code == 429:

            print(
                "ERROR 429: Too many requests."
            )

            print(
                "Waiting 60 seconds before retry..."
            )

            time.sleep(60)

        # ============================
        # OTHER ERRORS
        # ============================

        else:

            print(
                "API ERROR:",
                response.status_code,
                response.reason
            )

    except requests.exceptions.Timeout:

        print("ERROR: Request timed out")

    except requests.exceptions.ConnectionError:

        print("ERROR: Connection failed")

    except Exception as e:

        print("Unexpected Error:", e)

def save_to_database(states):

    conn = sqlite3.connect("flights.db")

    cursor = conn.cursor()

    inserted_count = 0

    for state in states:

        if state[6] and state[5]:

            lat = state[6]
            lon = state[5]

            # Filter Perak aircraft
            if (
                MIN_LAT <= lat <= MAX_LAT and
                MIN_LON <= lon <= MAX_LON
            ):

                icao24 = state[0]
                callsign = state[1]
                altitude = state[7]

                timestamp = datetime.now()

                cursor.execute("""
                INSERT INTO flights (
                    icao24,
                    callsign,
                    latitude,
                    longitude,
                    altitude,
                    timestamp
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    icao24,
                    callsign,
                    lat,
                    lon,
                    altitude,
                    timestamp
                ))

                inserted_count += 1

    conn.commit()
    conn.close()

    print(
        "Saved",
        inserted_count,
        "Perak aircraft at",
        datetime.now()
    )

def start_collection():

    # Keep 30 seconds but adjustable
    schedule.every(10).seconds.do(get_aircraft_data)

    print("Aircraft data collection started...")

    while True:

        schedule.run_pending()

        time.sleep(1)

if __name__ == "__main__":

    start_collection()