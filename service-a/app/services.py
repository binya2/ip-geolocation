import requests
import os
from dotenv import load_dotenv
from schemas import ipv4_address



load_dotenv()

API_KEY = os.getenv('API_KEY', None)
ip2loc_url = 'https://api.ip2loc.com'
service_b_url = 'http://'




def clean_data(data: dict) -> dict:
    ip = data.get('connection').get('ip')
    location = data.get('location')
    latitude = location.get('latitude')
    longitude = location.get('longitude')

    cleaned_data = {
        'ip': ip,
        'latitude': latitude,
        'longitude': longitude
        }

    return cleaned_data




def get_coordinates(ip: ipv4_address) -> dict:
    
    response = requests.get(
    f"{ip2loc_url}/{API_KEY}/{ip}"
    )

    clean_response = clean_data(response.json())

    return clean_response


def post_h(data : dict):
    response = requests.post(f'{service_b_url}', json=data)
