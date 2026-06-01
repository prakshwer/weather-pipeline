# 🌦️ Weather Data Pipeline

An end-to-end data engineering pipeline that ingests live weather 
data from an API, orchestrates transformations using Airflow and dbt, 
and visualizes KPIs on an interactive Streamlit dashboard.

## 🏗️ Architecture

OpenWeatherMap API--> Ingestion(Python)-->AirFlow DAG-->dbt Transformation-->Database-->Streamlit Dashboard

## 🛠️ Tech Stack

| Layer | Tool |
|-------|------|
| Ingestion | Python, Requests |
| Orchestration | Apache Airflow |
| Transformation | dbt |
| Storage | SQLite / PostgreSQL |
| Visualization | Streamlit |
| API | OpenWeatherMap |

## 📊 Features

- Live weather data ingestion via OpenWeatherMap API
- Automated pipeline scheduling and orchestration with Airflow DAGs
- dbt models for clean, tested transformation layer
- Pipeline logging for monitoring and debugging
- Interactive Streamlit dashboard with weather trends and KPIs

## 🚀 How to Run

1. Clone the repository
   git clone https://github.com/prakshwer/weather-pipeline.git

2. Install dependencies
   pip install -r requirements.txt

3. Add your OpenWeatherMap API key in a .env file
   WEATHER_API_KEY=your_api_key_here

4. Trigger the Airflow DAG or run ingestion manually
   python ingestion/ingest.py

5. Launch the Streamlit app
   streamlit run app/app.py

## 🌐 Live Demo

https://weather-pipeline-wzebvqqgn8e35rjmvc3wmh.streamlit.app

## 📁 Project Structure

weather-pipeline/
├── app/              # Streamlit dashboard
├── dags/             # Airflow DAG definitions
├── ingestion/        # API ingestion scripts
├── logs/             # Pipeline logs
├── weather_dbt/      # dbt transformation models
└── requirements.txt  # Python dependencies
