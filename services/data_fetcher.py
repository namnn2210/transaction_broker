import requests
from config import *
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

def access_token_service():
    suitecrm_url = 'http://localhost:8080'

    token_url = f'{suitecrm_url}/Api/access_token'
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(token_url, data=token_data)
    if response.status_code == 200:
        data = response.json()
        return data['access_token']

    return None


def account_service():
    suitecrm_url = 'http://localhost:8080'

    token = access_token_service()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    api_url = f'{suitecrm_url}/Api/V8/module/Accounts?fields[Accounts]=name,account_type,phone_office,email1,website,date_entered'
    response = requests.get(api_url, headers=headers)
    final_data = []
    if response.status_code == 200:
        data = response.json()
        list_data = data['data']
        for item in list_data:
            final_data.append(item['attributes'])
        return final_data

    return None

def contact_service():
    suitecrm_url = 'http://localhost:8080'

    token = access_token_service()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    api_url = f'{suitecrm_url}/Api/V8/module/Contacts?fields[Contacts]=first_name,last_name,title,phone_mobile,primary_address_street,email1,account_name,account_id,date_entered'
    response = requests.get(api_url, headers=headers)
    final_data = []
    if response.status_code == 200:
        data = response.json()
        list_data = data['data']
        for item in list_data:
            final_data.append(item['attributes'])
        return final_data

    return None

def project_service():
    suitecrm_url = 'http://localhost:8080'

    token = access_token_service()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    api_url = f'{suitecrm_url}/Api/V8/module/Project?fields[Project]=name,description,status,priority,date_entered'
    response = requests.get(api_url, headers=headers)
    final_data = []
    if response.status_code == 200:
        data = response.json()
        list_data = data['data']
        for item in list_data:
            final_data.append(item['attributes'])
        return final_data

    return None