import requests
import os
import json
from datetime import datetime
from pydantic import BaseModel, field_validator
from dotenv import load_dotenv

load_dotenv()

class WeatherRecord(BaseModel):
    city: str
    country: str
    timestamp: datetime
    temp_celsius: float
    feels_like: float
    humidity_pct: int
    pressure_hpa: int
    wind_speed_ms: float
    weather_desc: str
    visibility_m: int

    @field_validator('humidity_pct')
    @classmethod
    def valid_humidity(cls, v):
        assert 0 <= v <= 100, "Humidity must be between 0 and 100"
        return v

def fetch_weather(city: str) -> WeatherRecord:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Check your .env file.")
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    record = WeatherRecord(
        city=data["name"],
        country=data["sys"]["country"],
        timestamp=datetime.utcnow(),
        temp_celsius=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        humidity_pct=data["main"]["humidity"],
        pressure_hpa=data["main"]["pressure"],
        wind_speed_ms=data["wind"]["speed"],
        weather_desc=data["weather"][0]["description"],
        visibility_m=data.get("visibility", 0)
    )
    return record

def save_raw_json(record: WeatherRecord, city: str):
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    folder = f"data/raw/{date_str}/"
    os.makedirs(folder, exist_ok=True)
    time_str = datetime.utcnow().strftime("%H%M%S")
    filename = f"{folder}{city.lower()}_{time_str}.json"
    with open(filename, "w") as f:
        json.dump(record.model_dump(), f, default=str)
    print(f"Saved raw JSON to {filename}")