import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Weather, Base, User
from fetch import fetch_weather_openweathermap, fetch_weather_weatherapi, fetch_user_data

app = FastAPI()


@app.post("/fetch-weather", tags=["Weather Data"])
def fetch_and_save_weather(city: str):
    """
    Fetches weather data from OpenWeatherMap and WeatherAPI for a given city, and saves it to a SQLite database.

    Args:
        city (str): The name of the city to fetch weather data for.

    Returns:
        dict: A dictionary with a status code and a success message.
    """
    # Create a database engine and session
    engine = create_engine('sqlite:///./weather.db')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # API keys for OpenWeatherMap and WeatherAPI
    openweathermap_api_key = "00e8309422c3c7099d1e50d04d2ea62c"  # replace with your API key
    weather_api = "ff21eefb67ec4db7938193753243005"

    # Fetch weather data from both APIs
    weather_data = [
        fetch_weather_openweathermap(city, openweathermap_api_key),
        fetch_weather_weatherapi(city, weather_api),
    ]

    # Save the weather data to the database
    for api_name, temperature, humidity in weather_data:
        db.add(Weather(api_name=api_name, temperature=temperature, city=city, humidity=humidity))

    db.commit()

    # Return a success message
    return {"status": 200, "message": "Weather data fetched and saved successfully!"}


@app.get("/weather", tags=["Weather Data"])
def get_weather():
    """
    Gets the weather data from the SQLite database and returns it as a dictionary.

    Returns:
        dict: A dictionary with a status code, the weather data, and a success message.
    """
    # Create a database engine and session
    engine = create_engine('sqlite:///./weather.db')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # Fetch the weather data from the database
    weather_data = db.query(Weather).all()

    # Convert the created_at field to a string in a specific format
    for weather in weather_data:
        weather.created_at = weather.created_at.strftime("%m-%d-%Y %H:%M:%S")

    # Return the weather data as a dictionary
    return {
        "status": 200,
        "data": weather_data,
        "message": "Weather data fetched successfully!"
    }

@app.get("/fetch-user-data", tags=["User Data"])
def fetch_user():
    """
    Fetches user data from an API and saves it to a SQLite database.

    Returns:
        dict: A dictionary with a status code and a success message.
    """
    # Create a database engine and session
    engine = create_engine('sqlite:///./user.db')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Fetch user data from the API
    data = fetch_user_data()

    for item in data:
        db.add(User(first = item['first'], last = item['last'], address = item['address'], email = item['email'], balance = item['balance']))

    db.commit()
    # Return a success message
    return {"status": 200, "message": "User data fetched and saved successfully!"}

@app.get("/user", tags=["User Data"])
def get_user(limit: int = 10, offset: int = 0):
    """
    Fetches user data from the SQLite database and returns it as a dictionary.

    Args:
        limit (int, optional): The maximum number of users to fetch. Defaults to 10.
        offset (int, optional): The number of users to skip before fetching. Defaults to 0.

    Returns:
        dict: A dictionary with a status code, the user data, and a success message.
    """
    # Create a database engine and session
    engine = create_engine('sqlite:///./user.db')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # Fetch the total count of users in the database
    total_count = db.query(User).count()

    # Calculate the total number of pages based on the limit
    total_pages = (total_count // limit) + (total_count % limit > 0)

    # Fetch the user data from the database with limit and offset
    user_data = db.query(User).offset(offset).limit(limit).all()

    # Return the user data as a dictionary along with pagination information
    return {
        "status": 200,
        "data": user_data,
        "pagination": {
            "limit": limit,
            "offset": offset,
            "total_count": total_count,
            "total_pages": total_pages
        },
        "message": "User data fetched successfully!"
    }
def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()