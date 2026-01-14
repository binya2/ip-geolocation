from fastapi import APIRouter
from starlette import status

import storage
from shared.schemas import IpToCoordinates, Ip

router = APIRouter(tags=["Coordinates_api"])


@router.post("/redis", status_code=status.HTTP_201_CREATED)
async def post(ip_to_coordinates: IpToCoordinates):
    if await storage.save_location(ip_to_coordinates):
        return {"success": True,
                "message": "Redis Saved Successfully"}
    else:
        return {"success": False,
                "message": "Redis Not Saved Successfully"}


@router.get("/redis", status_code=status.HTTP_200_OK)
async def get_all():
    try:
        data = await storage.get_all_locations()
        return data
    except Exception as e:
        return {"message": str(e)}


@router.get("/redis/{ip}", status_code=status.HTTP_200_OK)
async def get_py_ip(ip):
    try:
        data = await storage.get_location_by_ip(ip.__str__())
        return data
    except Exception as e:
        return {"message": str(e)}
