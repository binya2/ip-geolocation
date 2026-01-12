from fastapi import FastAPI
from schemas import ipv4_address
from services import *


app = FastAPI()



@app.get('/{ip}')
def get_details_from_ip(ip: ipv4_address):
    coordinates = get_coordinates(ip)




@app.get('/get-all-ips')
def get_all():
    pass
