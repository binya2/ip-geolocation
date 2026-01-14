import os

import requests
from fastapi import HTTPException
from pydantic import IPvAnyAddress, ValidationError
from pydantic_extra_types.coordinate import Coordinate

from shared.schemas import IpToCoordinates, Ip

API_KEY = os.getenv('API_KEY', "5F67eMEeTFUlPaewp4z6JeMQsu83klkB")
ip2loc = 'https://api.ip2loc.com'
ip2loc_url = f'{ip2loc}/{API_KEY}'
service_b_ip = os.getenv('SERVICE_B_IP', "127.0.0.1")
service_b_port = os.getenv('SERVICE_B_PORT', 61982)
service_b_url = f'http://{service_b_ip}:{service_b_port}/redis'


def clean_data(data: dict) -> IpToCoordinates:
    connection_info = data.get('connection', {})
    location_info = data.get('location', {})
    ip_str = connection_info.get('ip')
    if not ip_str:
        raise ValueError("Missing IP address in data")
    try:
        current_ip:IPvAnyAddress = ip_str
        location = Coordinate(**location_info)
        return IpToCoordinates(ip=current_ip, coord=location)
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise e


def get_all_data():
    try:
        response = requests.get(service_b_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        return err


def get_coordinates(ip: Ip):
    try:
        response = requests.get(
            f"{ip2loc_url}/{ip}"
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        return err


def save_ip_data(data: IpToCoordinates):
    coordinates = data.get('coord')
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
