from fastapi import FastAPI, HTTPException

from services import *

app = FastAPI()


@app.get('/{ip}')
def get_details_from_ip(ip: ipvany_address):
    response = get_coordinates(ip)

    try:
        print(response)
        if response.get('connection'):
            clean_response = clean_data(response)
            is_saved = save_ip_data(clean_response)
        else:
            raise HTTPException(status_code=500, detail={'Error': 'error when trying to save ip in the DB.'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {'message': 'ip saved successfully', 'request details': is_saved, 'ip details': clean_response}


@app.get('/get-all-ips')
def get_all():
    try:
        data = get_all_data()

        if not data:
            return {'message': 'No data found'}

        if data.get('ip'):
            return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
