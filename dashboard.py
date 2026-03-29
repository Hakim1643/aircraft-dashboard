import streamlit as st
import sqlite3
import pandas as pd
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt

st.title("Aircraft Monitoring Over Perak")

# ============================
# LOAD DATA
# ============================

conn = sqlite3.connect("flights.db")

df = pd.read_sql_query(
    "SELECT * FROM flights",
    conn
)

conn.close()

# ============================
# SUMMARY METRICS
# ============================

st.header("Flight Summary")

if not df.empty:

    total_flights = len(df)
    highest_altitude = df["altitude"].max()
    average_altitude = df["altitude"].mean()

    st.write("Total Flights:", total_flights)
    st.write("Highest Altitude:", round(highest_altitude, 2))
    st.write("Average Altitude:", round(average_altitude, 2))

    st.info(
        "Insight: The summary shows overall aircraft activity. "
        "Higher average altitude usually indicates cruising aircraft, "
        "while extreme values show peak flight levels."
    )

else:

    st.warning("No flight data available yet.")

# ============================
# MAP 
# ============================

st.header("Aircraft Locations Map")

map = folium.Map(
    location=[4.6, 101.1],
    zoom_start=7
)

for _, row in df.iterrows():

    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=3
    ).add_to(map)

folium_static(map)

st.info(
    "Insight: This map displays aircraft positions across Perak. "
    "Clusters of markers indicate areas with higher flight activity."
)


# ============================
# ALTITUDE DISTRIBUTION 
# ============================

st.header("Altitude Distribution")

if not df.empty:

    # Remove missing altitude values
    altitude_data = df["altitude"].dropna()

    # Create altitude bins (height ranges)
    bins = pd.cut(
        altitude_data,
        bins=20
    )

    # Count flights per height range
    altitude_counts = (
        bins.value_counts()
        .sort_index()
    )

    plt.figure()

    plt.plot(
        range(len(altitude_counts)),
        altitude_counts.values,
        marker='o'
    )

    plt.title("Aircraft Distribution by Altitude Height")
    plt.xlabel("Altitude Height Range")
    plt.ylabel("Number of Flights")

    st.pyplot(plt)

    st.info(
        "Insight: This graph shows how aircraft are distributed "
        "across different altitude heights. Peaks indicate the "
        "most common flight cruising levels."
    )

else:

    st.warning("No altitude data available.")

# ============================
# FLIGHTS PER HOUR
# ============================

st.header("Flights Per Hour")

if not df.empty:

    if "timestamp" in df.columns:

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        df["hour"] = df["timestamp"].dt.hour

        flights_per_hour = df["hour"].value_counts().sort_index()

        plt.figure()

        plt.bar(
            flights_per_hour.index,
            flights_per_hour.values
        )

        plt.title("Flights Per Hour")
        plt.xlabel("Hour of Day")
        plt.ylabel("Number of Flights")

        st.pyplot(plt)

        st.info(
            "Insight: This chart shows peak aircraft activity times. "
            "Higher bars indicate hours with more air traffic."
        )

    else:

        st.warning("Timestamp column not found.")

else:

    st.warning("No time data available.")

# ============================
# TOP AIRCRAFT FREQUENCY
# ============================

st.header("Top 10 Most Frequent Aircraft")

if not df.empty:

    if "icao24" in df.columns:

        top_aircraft = (
            df.groupby("icao24")
            .size()
            .sort_values(ascending=False)
            .head(10)
        )

        plt.figure()

        plt.bar(
            top_aircraft.index,
            top_aircraft.values
        )

        plt.title("Top 10 Aircraft by Frequency")
        plt.xlabel("Aircraft ICAO")
        plt.ylabel("Number of Records")

        plt.xticks(rotation=45)

        st.pyplot(plt)

        st.info(
            "Insight: This chart identifies aircraft that appear "
            "most frequently in the monitored region."
        )

    else:

        st.warning("icao24 column not found.")

else:

    st.warning("No aircraft data available.")