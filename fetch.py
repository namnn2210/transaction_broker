import requests

def fetch_weather_openweathermap(city_name, api_key):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    response = requests.get(api_url)
    data = response.json()
    temperature = (data['main']['temp'] - 32) *5/9
    humidity = data['main']['humidity']
    return "openweathermap", temperature, humidity

def fetch_weather_weatherstack(city_name, api_key):
    api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city_name}"
    response = requests.get(api_url)
    data = response.json()
    temperature = data['current']['temperature']
    humidity = data['current']['humidity']
    return "weatherstack", temperature, humidity

def fetch_weather_weatherapi(city_name, api_key):
    api_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_name}"
    response = requests.get(api_url)
    data = response.json()
    temperature = data['current']['temp_c']
    humidity = data['current']['humidity']
    return "weatherapi", temperature, humidity