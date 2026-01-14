import os

import httpx
import requests
from fastapi import HTTPException
from pydantic import IPvAnyAddress, ValidationError
from pydantic_extra_types.coordinate import Coordinate

from shared.schemas import IpToCoordinates, Ip

API_KEY = os.getenv('API_KEY', "5F67eMEeTFUlPaewp4z6JeMQsu83klkB")
ip2loc = 'https://api.ip2loc.com'
ip2loc_url = f'{ip2loc}/{API_KEY}'
service_b_ip = os.getenv('SERVICE_B_IP', "127.0.0.1")
# service_b_port = os.getenv('SERVICE_B_PORT', 38854)
service_b_port = 38854
service_b_url = f'http://{service_b_ip}:{service_b_port}/redis'


async def clean_data(data: dict) -> IpToCoordinates:
    connection_info = data.get('connection', {})
    location_info = data.get('location', {})
    longitude = location_info.get('longitude')
    latitude = location_info.get('latitude')
    ip_str = connection_info.get('ip')
    if not ip_str:
        raise ValueError("Missing IP address in data")
    try:
        current_ip: IPvAnyAddress = ip_str
        location = Coordinate(longitude=longitude, latitude=latitude)
        return IpToCoordinates(ip=current_ip, coord=location)

    except ValidationError as e:
        print(f"Validation error: {e}")
        raise e


async def get_all_data():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(service_b_url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as err:
            return err


async def get_coordinates(ip: Ip):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{ip2loc_url}/{ip}"
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as err:
            return err


async def save_ip_data(data: IpToCoordinates):
    if not (data.coord.latitude is None or data.coord.longitude is None):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(service_b_url, json=data.model_dump(mode='json'))
                response_data = response.json()
                if not response_data.get('success'):
                    raise requests.exceptions.HTTPError(response=response.json().get('message'))
                return response_data
            except httpx.HTTPError as err:
                return err
    else:
        raise HTTPException(status_code=400, detail={'Error': 'error when trying to save ip data'})
