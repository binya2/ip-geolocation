from fastapi import HTTPException, APIRouter

from services import *

router = APIRouter()


@router.get('/get-ip/{ip}')
def get_details_from_ip(ip:str):
    response = get_coordinates(ip)
    try:
        if response.get('connection'):
            clean_response = clean_data(response)
            coordinates = clean_response['coord']
            if coordinates.get('latitude') and coordinates.get('longitude'):
                is_saved = save_ip_data(clean_response)
            else:
                return {'message': 'No data found'}
        else:
            raise HTTPException(status_code=500, detail={'Error': 'error when trying to save ip in the DB.'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {'message': 'ip saved successfully', 'request details': is_saved, 'ip details': clean_response}


@router.get('/get-all-ips')
def get_all():
    try:
        print("get_all_ips1")
        data = get_all_data()
        print(data)
        if not data:
            return {'message': 'No data found'}
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
