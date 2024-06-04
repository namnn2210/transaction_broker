import requests

def fetch_weather_openweathermap(city_name, api_key):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    response = requests.get(api_url)
    data = response.json()
    temperature = (data['main']['temp'] - 32) *5/9
    humidity = data['main']['humidity']
    return "openweathermap", temperature, humidity

def fetch_weather_weatherapi(city_name, api_key):
    api_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_name}"
    response = requests.get(api_url)
    data = response.json()
    temperature = data['current']['temp_c']
    humidity = data['current']['humidity']
    return "weatherapi", temperature, humidity

def fetch_user_data():
    api_url = 'https://randomapi.com/api/6de6abfedb24f889e0b5f675edc50deb?fmt=raw&sole'
    response = requests.get(api_url)
    data = response.json()
    return data

def fetch_product_data():
    product_url = 'https://fakestoreapi.com/products'
    response = requests.get(product_url)
    data = response.json()
    return data

def fetch_cart_data():
    cart_url = 'https://fakestoreapi.com/carts'
    response = requests.get(cart_url)
    data = response.json()
    return data