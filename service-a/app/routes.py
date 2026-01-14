from fastapi import APIRouter, HTTPException

from services import get_coordinates, clean_data, save_ip_data, get_all_data

router = APIRouter()


@router.get('/get-ip/{ip}')
def get_details_from_ip(ip):
    response = get_coordinates(ip)
    try:
        if response.get('connection'):
            clean_response = clean_data(response)
            is_saved = save_ip_data(clean_response)
            print("is_saved", is_saved)
            return {'ip details': clean_response}
        else:
            raise HTTPException(status_code=500, detail={'Error': 'error when trying to save ip in the DB.'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/get-all-ips')
def get_all():
    try:
        data = get_all_data()
        if not data:
            return {'message': 'No data found'}
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
