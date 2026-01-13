import requests
import os
from schemas import ipvany_address, IpData




API_KEY = os.getenv('API_KEY')
ip2loc = 'https://api.ip2loc.com'
ip2loc_url = f'{ip2loc}/{API_KEY}'
service_b_ip = os.getenv('SERVICE_B_IP', None)
service_b_port = os.getenv('SERVICE_B_PORT', None)
service_b_url = f'http://{service_b_ip}:{service_b_port}/redis'


def clean_data(data: dict) -> dict:
    ip = data.get('connection').get('ip')
    location = data.get('location')
    latitude = location.get('latitude')
    longitude = location.get('longitude')

    cleaned_data = {
        'ip': ip,
        'coord': {
            'latitude': latitude,
            'longitude': longitude
            }
        }

    return cleaned_data



def get_all_data():
    try:
        response = requests.get(service_b_url)
        
        if response.get('status') != True:
            raise requests.exceptions.HTTPError(response=response['message'])
        response.raise_for_status()

    except requests.exceptions.HTTPError as err:
        return err

    return response.json()



def get_coordinates(ip: ipvany_address) -> dict:
    try:
        response = requests.get(
        f"{ip2loc_url}/{ip}"
        )

        response.raise_for_status()
    
    except requests.exceptions.HTTPError as err:
        return err

    return response.json()



def save_ip_data(data : dict):
    try:    
        response = requests.post(service_b_url, json=data)
        if response.get('status') != True:
            raise requests.exceptions.HTTPError(response=response.get('message'))
        requests.raise_for_status()

    except requests.exceptions.HTTPError as err:
        return err
    
    return response.json()

