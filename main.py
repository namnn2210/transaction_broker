import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Weather, Base
from fetch import fetch_weather_openweathermap, fetch_weather_weatherstack, fetch_weather_weatherapi

app = FastAPI()

@app.post("/fetch-weather")
def fetch_and_save_weather():
    engine = create_engine('sqlite:///./weather.db')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    city_name = "London"  # replace with your city name
    openweathermap_api_key = "00e8309422c3c7099d1e50d04d2ea62c"  # replace with your API key
    weather_api = "ff21eefb67ec4db7938193753243005"

    weather_data = [
        fetch_weather_openweathermap(city_name, openweathermap_api_key),
        # fetch_weather_weatherstack(city_name, api_key),
        fetch_weather_weatherapi(city_name, weather_api),
    ]

    for api_name, temperature, humidity in weather_data:
        db.add(Weather(api_name=api_name, temperature=temperature, humidity=humidity))

    db.commit()

    return {"status":200,"message": "Weather data fetched and saved successfully!"}

@app.get("/weather")
def get_weather():
    engine = create_engine('sqlite:///./weather.db')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    weather_data = db.query(Weather).all()
    for weather in weather_data:
        weather.created_at = weather.created_at.strftime("%m-%d-%Y %H:%M:%S")

    return {"status":200,"data": weather_data, "message": "Weather data fetched successfully!"}

def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()