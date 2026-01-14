import os

import requests
from fastapi import HTTPException

from schemas import ipvany_address

API_KEY = os.getenv('API_KEY', "5F67eMEeTFUlPaewp4z6JeMQsu83klkB")
ip2loc = 'https://api.ip2loc.com'
ip2loc_url = f'{ip2loc}/{API_KEY}'
service_b_ip = os.getenv('SERVICE_B_IP', "127.0.0.1")
service_b_port = os.getenv('SERVICE_B_PORT', 61982)
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
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        return err


def get_coordinates(ip: str):
    try:
        ip = ipvany_address(ip)
        response = requests.get(
            f"{ip2loc_url}/{ip}"
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        return err


def save_ip_data(data: dict):
    coordinates = data['coord']
    if coordinates.get('latitude') and coordinates.get('longitude'):
        try:
            response = requests.post(service_b_url, json=data)
            if response.json().get('success'):
                raise requests.exceptions.HTTPError(response=response.json().get('message'))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            return err
    else:
        raise HTTPException(status_code=400, detail={'Error': 'error when trying to save ip data'})
