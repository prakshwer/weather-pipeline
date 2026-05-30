import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.extract import fetch_weather, save_raw_json
from ingestion.load import load_to_database

st.set_page_config(page_title="Weather Pipeline", page_icon="🌦", layout="wide")

st.title("Weather Data Pipeline Dashboard")
st.caption("Powered by OpenWeatherMap API | ELT pipeline with dbt")

engine = create_engine("sqlite:///data/weather.db")

st.subheader("Fetch live weather")
city_input = st.text_input("Enter a city name", placeholder="e.g. Mumbai, London, Tokyo")

if st.button("Fetch and save to database"):
    if city_input.strip() == "":
        st.warning("Please enter a city name.")
    else:
        with st.spinner(f"Fetching weather for {city_input}..."):
            try:
                record = fetch_weather(city_input)
                save_raw_json(record, city_input)
                load_to_database(record)
                st.success(f"Data saved for {record.city}, {record.country}")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Temperature", f"{record.temp_celsius}°C", f"Feels like {record.feels_like}°C")
                col2.metric("Humidity", f"{record.humidity_pct}%")
                col3.metric("Wind Speed", f"{record.wind_speed_ms} m/s")
                col4.metric("Pressure", f"{record.pressure_hpa} hPa")
                st.info(f"Condition: {record.weather_desc.title()}")
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()

st.subheader("Historical data from database")

try:
    df = pd.read_sql("SELECT * FROM raw_weather ORDER BY timestamp DESC LIMIT 500", engine)
    if df.empty:
        st.info("No data yet. Fetch some cities above to get started.")
    else:
        st.write(f"Total records: {len(df)}")

        tab1, tab2, tab3 = st.tabs(["Temperature", "Humidity", "Raw data"])

        with tab1:
            fig = px.line(df, x="timestamp", y="temp_celsius", color="city",
                          title="Temperature over time by city",
                          labels={"temp_celsius": "Temp (°C)", "timestamp": "Time"})
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            fig2 = px.scatter(df, x="temp_celsius", y="humidity_pct", color="city",
                              title="Humidity vs Temperature",
                              labels={"temp_celsius": "Temp (°C)", "humidity_pct": "Humidity %"},
                              hover_data=["weather_desc", "timestamp"])
            st.plotly_chart(fig2, use_container_width=True)

        with tab3:
            st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Could not load database: {e}")