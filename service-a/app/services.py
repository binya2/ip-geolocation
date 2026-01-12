import requests
import os
from dotenv import load_dotenv
from schemas import ipv4_address



load_dotenv()

API_KEY = os.getenv('API_KEY')
ip2loc_url = 'https://api.ip2loc.com'


def clean_data(data: dict) -> dict:
    pass



def get_coordinates(ip: ipv4_address) -> dict:
    
    response = requests.get(
    f"{ip2loc_url}/{API_KEY}/{ip}"
    )

    clean_response = clean_data(response.json())

    return clean_response



def post_h(data : dict):
    response = requests.post(f'http://db-host/redis', json=data)


# response.status_code
