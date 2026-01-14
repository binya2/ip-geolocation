from fastapi import APIRouter, HTTPException
from starlette import status

import storage
from shared.schemas import IpToCoordinates, Ip

router = APIRouter(tags=["Coordinates_api"])


@router.post("/redis", status_code=status.HTTP_201_CREATED)
async def post(ip_to_coordinates: IpToCoordinates):
    result = await storage.save_location(ip_to_coordinates)
    if result:
        return {"success": True, "message": "Saved Successfully"}

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to save to Redis"
    )

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
