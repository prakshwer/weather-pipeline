import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.extract import fetch_weather, save_raw_json
from ingestion.load import load_to_database

DB_PATH = "data/weather.db"
os.makedirs("data", exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}")

def ensure_table():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS raw_weather (
                city TEXT, country TEXT, timestamp TEXT,
                temp_celsius REAL, feels_like REAL,
                humidity_pct INTEGER, pressure_hpa INTEGER,
                wind_speed_ms REAL, weather_desc TEXT,
                visibility_m INTEGER
            )
        """))
        conn.commit()

ensure_table()

st.set_page_config(
    page_title="Weather Pipeline",
    page_icon="🌦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .block-container { padding-top: 2rem; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #2d3250);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #3d4266;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #8b92b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #5cb8e4;
        margin-top: 6px;
    }
    .weather-icon {
        font-size: 2.5rem;
        margin-bottom: 8px;
    }
    .city-header {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
    }
    .condition-badge {
        background: #2d3250;
        border-radius: 20px;
        padding: 4px 16px;
        color: #5cb8e4;
        font-size: 0.9rem;
        border: 1px solid #3d4266;
        display: inline-block;
        margin-top: 8px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #5cb8e4, #3d8fc4);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #3d8fc4, #2d6fa4);
        transform: translateY(-2px);
    }
    .stTextInput > div > div > input {
        background-color: #1e2130;
        border: 1px solid #3d4266;
        border-radius: 10px;
        color: white;
        padding: 0.6rem 1rem;
        font-size: 1rem;
    }
    div[data-testid="stTab"] {
        background-color: #1e2130;
        border-radius: 10px;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3d4266;
    }
</style>
""", unsafe_allow_html=True)

def get_weather_icon(description):
    desc = description.lower()
    if "thunderstorm" in desc: return "⛈️"
    elif "rain" in desc or "drizzle" in desc: return "🌧️"
    elif "snow" in desc: return "❄️"
    elif "mist" in desc or "fog" in desc or "haze" in desc: return "🌫️"
    elif "cloud" in desc: return "☁️"
    elif "clear" in desc: return "☀️"
    else: return "🌤️"

def get_temp_color(temp):
    if temp < 0: return "#a8d8ff"
    elif temp < 10: return "#7ec8e3"
    elif temp < 20: return "#90ee90"
    elif temp < 30: return "#ffd700"
    else: return "#ff6b6b"

with st.sidebar:
    st.markdown("## 🌦 Weather Pipeline")
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    A **data engineering** portfolio project:
    - Live API ingestion
    - Pydantic validation
    - SQLite warehouse
    - dbt transformation
    - Interactive dashboard
    """)
    st.markdown("---")
    st.markdown("**Tech Stack**")
    st.markdown("`Python` `SQL` `dbt` `Streamlit`")
    st.markdown("---")
    st.markdown("[View on GitHub](https://github.com/prakshwer/weather-pipeline)")
    st.caption("Built for data engineering interview")

st.markdown("<h1 style='text-align:center; color:white;'>🌍 Weather Data Pipeline</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8b92b8;'>Live weather data powered by OpenWeatherMap API</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col_input, col_btn = st.columns([3, 1])
with col_input:
    city_input = st.text_input("", placeholder="Enter city name — e.g. Mumbai, London, Tokyo, Kolkata")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    fetch_btn = st.button("Fetch Weather")

if fetch_btn:
    if city_input.strip() == "":
        st.warning("Please enter a city name.")
    else:
        with st.spinner(f"Fetching weather for {city_input}..."):
            try:
                record = fetch_weather(city_input)
                save_raw_json(record, city_input)
                load_to_database(record)

                icon = get_weather_icon(record.weather_desc)
                temp_color = get_temp_color(record.temp_celsius)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style='text-align:center; padding: 10px;'>
                    <div class='weather-icon'>{icon}</div>
                    <div class='city-header'>{record.city}, {record.country}</div>
                    <div class='condition-badge'>{record.weather_desc.title()}</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2, c3, c4, c5 = st.columns(5)

                with c1:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='weather-icon'>🌡️</div>
                        <div class='metric-value' style='color:{temp_color}'>{record.temp_celsius}°C</div>
                        <div class='metric-label'>Temperature</div>
                        <div class='metric-sub'>Feels like {record.feels_like}°C</div>
                    </div>""", unsafe_allow_html=True)

                with c2:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='weather-icon'>💧</div>
                        <div class='metric-value' style='color:#5cb8e4'>{record.humidity_pct}%</div>
                        <div class='metric-label'>Humidity</div>
                        <div class='metric-sub'>Relative humidity</div>
                    </div>""", unsafe_allow_html=True)

                with c3:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='weather-icon'>💨</div>
                        <div class='metric-value' style='color:#90ee90'>{record.wind_speed_ms}</div>
                        <div class='metric-label'>Wind Speed</div>
                        <div class='metric-sub'>metres per second</div>
                    </div>""", unsafe_allow_html=True)

                with c4:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='weather-icon'>🔵</div>
                        <div class='metric-value' style='color:#ffd700'>{record.pressure_hpa}</div>
                        <div class='metric-label'>Pressure</div>
                        <div class='metric-sub'>hPa</div>
                    </div>""", unsafe_allow_html=True)

                with c5:
                    vis_km = round(record.visibility_m / 1000, 1)
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='weather-icon'>👁️</div>
                        <div class='metric-value' style='color:#da70d6'>{vis_km}</div>
                        <div class='metric-label'>Visibility</div>
                        <div class='metric-sub'>kilometres</div>
                    </div>""", unsafe_allow_html=True)

                st.success(f"Data saved to database successfully!")

            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Historical Weather Data</div>", unsafe_allow_html=True)

try:
    df = pd.read_sql("SELECT * FROM raw_weather ORDER BY timestamp DESC LIMIT 500", engine)
    if df.empty:
        st.info("No historical data yet. Fetch some cities above to get started.")
    else:
        st.markdown(f"<p style='color:#8b92b8;'>Total records in database: {len(df)}</p>", unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["Temperature Trends", "Humidity Analysis", "Raw Data"])

        with tab1:
            fig = px.line(df, x="timestamp", y="temp_celsius", color="city",
                          title="Temperature Over Time",
                          labels={"temp_celsius": "Temperature (°C)", "timestamp": "Time"},
                          template="plotly_dark",
                          color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_layout(
                plot_bgcolor="#1e2130",
                paper_bgcolor="#1e2130",
                font_color="white",
                title_font_size=16,
                legend=dict(bgcolor="#2d3250", bordercolor="#3d4266")
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            fig2 = px.scatter(df, x="temp_celsius", y="humidity_pct", color="city",
                              size="wind_speed_ms",
                              title="Humidity vs Temperature",
                              labels={"temp_celsius": "Temperature (°C)", "humidity_pct": "Humidity %"},
                              template="plotly_dark",
                              hover_data=["weather_desc", "timestamp"],
                              color_discrete_sequence=px.colors.qualitative.Set2)
            fig2.update_layout(
                plot_bgcolor="#1e2130",
                paper_bgcolor="#1e2130",
                font_color="white",
                title_font_size=16
            )
            st.plotly_chart(fig2, use_container_width=True)

        with tab3:
            st.dataframe(
                df.style.background_gradient(subset=["temp_celsius"], cmap="RdYlBu_r"),
                use_container_width=True
            )

except Exception as e:
    st.error(f"Could not load database: {e}")