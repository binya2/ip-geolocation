from fastapi import APIRouter
from starlette import status

from schemas import IpToCoordinates, Ip

router = APIRouter(tags=["Coordinates_api"])


@router.post("/redis", status_code=status.HTTP_201_CREATED)
async def redis(ip_to_coordinates: IpToCoordinates):
    pass


@router.get("/redis", )
async def redis():
    pass


@router.get("/redis/{ip}", status_code=status.HTTP_200_OK)
async def redis(ip: Ip):
    pass
