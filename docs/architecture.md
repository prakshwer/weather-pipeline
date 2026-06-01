# Pipeline Architecture

## Data Flow
1. Ingestion: Python script calls OpenWeatherMap API every hour
2. Storage: Raw data stored in database via Airflow DAG
3. Transformation: dbt models clean and aggregate raw data
4. Visualization: Streamlit reads transformed data and renders dashboard

## Airflow DAG Schedule
- Frequency: Hourly
- Tasks: extract → validate → load → transform

## dbt Models
- staging: raw API response cleaned
- reporting: aggregated metrics for dashboard
