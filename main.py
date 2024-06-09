import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database_connection import get_database
from models.model import Weather, Base, User
from applications.cart import fetch_cart_data
from applications.weather import fetch_weather_openweathermap
from applications.user import fetch_user_data
from applications.suitecrm import fetch_account_data, fetch_contact_data, fetch_project_data
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/fetch-weather", tags=["Weather Data"])
async def fetch_and_save_weather(city: str):
    db = get_database()

    weather_api = "ff21eefb67ec4db7938193753243005"

    # Fetch weather data from both APIs
    weather_data = [
        fetch_weather_openweathermap(city, weather_api),
    ]

    # Save the weather data to the database
    for api_name, temperature, humidity in weather_data:
        db['weather'].insert_one({
            "api_name": api_name,
            "temperature": temperature,
            "city": city,
            "humidity": humidity,
            "created_at": datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
        })

    # Return a success message
    return {"status": 200, "message": "Weather data fetched and saved successfully!"}


@app.get("/weather", tags=["Weather Data"])
async def get_weather():
    db = get_database()

    # Fetch the weather data from the database
    weather_data = list(db['weather'].find({}, {'_id': 0}))

    # Return the weather data as a dictionary
    return {
        "status": 200,
        "data": weather_data,
        "message": "Weather data fetched successfully!"
    }

@app.get("/fetch-user-data", tags=["User Data"])
def fetch_user():
    # Create a database engine and session
    db = get_database()

    # Fetch user data from the API
    data = fetch_user_data()

    for item in data['data']:
        db['user'].insert_one({
            "id": item['id'],
            "uuid": item['uuid'],
            "first_name": item['firstname'],
            "last_name": item['lastname'],
            "username": item['username'],
            "password": item['password'],
            "email": item['email'],
            "ip_address": item['ip'],
            "mac_address": item['macAddress'],
            "website": item['website'],
            "image": item['image'],
            "created_at": datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
        })
    # Return a success message
    return {"status": 200, "message": "User data fetched and saved successfully!"}

@app.get("/user", tags=["User Data"])
def get_user(limit: int = 10, offset: int = 0):
    # Create a database engine and session
    db = get_database()

    # Fetch the total count of users in the database
    total_count = db.user.count_documents({})

    # Calculate the total number of pages based on the limit
    total_pages = (total_count // limit) + (total_count % limit > 0)

    # Fetch the user data from the database with limit and offset
    user_data = db.user.find({}, {'_id': 0}).skip(offset).limit(limit)

    # Return the user data as a dictionary along with pagination information
    return {
        "status": 200,
        "data": list(user_data),
        "pagination": {
            "limit": limit,
            "offset": offset,
            "total_count": total_count,
            "total_pages": total_pages
        },
        "message": "User data fetched successfully!"
    }

@app.get("/fetch-cart-data", tags=["Cart Data"])
async def fetch_cart():
    db = get_database()
    cart = fetch_cart_data()
    db['cart'].insert_many(cart)
    return {"status": 200, "message": "Cart data fetched and saved successfully!"}

@app.get("/cart", tags=["Cart Data"])
async def get_cart(limit: int = 10, offset: int = 0):
    db = get_database()
    cart = db['cart'].find({}, {'_id': 0}).skip(offset).limit(limit)
    print(cart)
    return {"status": 200, "data": list(cart), "message": "Cart data fetched successfully!"}

@app.get("/fetch-account-data", tags=["Account Data"])
async def fetch_account():
    db = get_database()
    account = fetch_account_data()
    db['account'].insert_many(account)
    return {"status": 200, "message": "Account data fetched and saved successfully!"}

@app.get("/account", tags=["Account Data"])
async def get_account(limit: int = 10, offset: int = 0):
    db = get_database()
    account = db['account'].find({}, {'_id': 0}).skip(offset).limit(limit)
    return {"status": 200, "data": list(account), "message": "Account data fetched successfully!"}

@app.get("/fetch-contact-data", tags=["Contact Data"])
async def fetch_contact():
    db = get_database()
    contact = fetch_contact_data()
    db['contact'].insert_many(contact)
    return {"status": 200, "message": "Contact data fetched and saved successfully!"}

@app.get("/contact", tags=["Contact Data"])
async def get_contact(limit: int = 10, offset: int = 0):
    db = get_database()
    account = db['contact'].find({}, {'_id': 0}).skip(offset).limit(limit)
    return {"status": 200, "data": list(account), "message": "Contact data fetched successfully!"}

@app.get("/fetch-project-data", tags=["Project Data"])
async def fetch_project():
    db = get_database()
    project = fetch_project_data()
    db['project'].insert_many(project)
    return {"status": 200, "message": "Project data fetched and saved successfully!"}

@app.get("/project", tags=["Project Data"])
async def get_project(limit: int = 10, offset: int = 0):
    db = get_database()
    account = db['project'].find({}, {'_id': 0}).skip(offset).limit(limit)
    return {"status": 200, "data": list(account), "message": "Project data fetched successfully!"}

    
def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()