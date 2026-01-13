from fastapi import HTTPException, APIRouter

from services import *

router = APIRouter()


@router.get('/{ip}')
def get_details_from_ip(ip: ipvany_address):
    response = get_coordinates(ip)

    try:
        print(response)
        if response.get('connection'):
            clean_response = clean_data(response)
            save_ip_data(IpData(**clean_response))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {'ip': ip, 'details': clean_response}


@router.get('/get-all-ips')
def get_all():
    try:
        data = get_all_data()

        if not data:
            return {'message': 'No data found'}

        if data.get('ip'):
            return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
