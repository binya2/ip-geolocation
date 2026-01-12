import requests
import os
from fastapi import HTTPException, status
from dotenv import load_dotenv
from schemas import ipv4_address, IpData



load_dotenv()

API_KEY = os.getenv('API_KEY', None)
ip2loc_url = 'https://api.ip2loc.com'
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
        
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        if response['status'] != True:
            raise HTTPException(status_code=400, detail=response['message'])

    
    except HTTPException as err:
        return err

    return response.json()



def get_coordinates(ip: ipv4_address) -> dict:
    try:
        response = requests.get(
        f"{ip2loc_url}/{API_KEY}/{ip}"
        )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    
    except HTTPException as err:
        return err

    clean_response = clean_data(response.json())


    is_saved = save_ip_data(IpData(**clean_response))

    return is_saved


def save_ip_data(data : IpData):
    try:    
        response = requests.post(service_b_url, json=data.model_dump())
        
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        if response['status'] != True:
            raise HTTPException(status_code=400, detail=response['message'])

    except HTTPException as err:
        return err
    
    return response.json()

