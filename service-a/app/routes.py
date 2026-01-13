from fastapi import FastAPI
from schemas import ipvany_address, IpData
from services import *


app = FastAPI()



@app.get('/{ip}')
def get_details_from_ip(ip: ipvany_address):

    response = get_coordinates(ip)
    
    clean_response = clean_data(response)

    coordinates = save_ip_data(IpData(**clean_response))

    return {'ip': ip, 'details': coordinates}


@app.get('/get-all-ips')
def get_all():
    data = get_all_data()
    return data
