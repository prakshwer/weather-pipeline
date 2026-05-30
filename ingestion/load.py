import pandas as pd
from sqlalchemy import create_engine
from ingestion.extract import WeatherRecord

engine = create_engine("sqlite:///data/weather.db")

def load_to_database(record: WeatherRecord):
    df = pd.DataFrame([record.model_dump()])
    df['timestamp'] = df['timestamp'].astype(str)
    df.to_sql("raw_weather", engine, if_exists="append", index=False)
    print(f"Loaded {record.city}, {record.country} into database")