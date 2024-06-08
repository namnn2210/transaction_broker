import requests

def cart_service():
    response = requests.get('https://fakestoreapi.com/carts')
    data = response.json()
    return data

def weather_service(city_name, api_key):
    api_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_name}"
    response = requests.get(api_url)
    data = response.json()
    temperature = data['current']['temp_c']
    humidity = data['current']['humidity']
    return "weatherapi", temperature, humidity

def user_service():
    api_url = 'https://fakerapi.it/api/v1/users'
    response = requests.get(api_url)
    data = response.json()
    return data