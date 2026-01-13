from pydantic.networks import IPvAnyAddress
from pydantic import BaseModel


ipvany_address = IPvAnyAddress

class Coordinates(BaseModel):
    latitude: float
    longitude: float


class IpData(BaseModel):
    ip: ipvany_address
    coord: dict[Coordinates]
