from services.data_fetcher import weather_service
def fetch_weather_openweathermap(city_name, api_key):
    return weather_service(city_name, api_key)