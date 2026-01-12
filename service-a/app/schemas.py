from pydantic.networks import IPv4Address
from pydantic import BaseModel


ipv4_address = IPv4Address

class Coordinates(BaseModel):
    latitude: float
    longitude: float


class IpData(BaseModel):
    ip: IPv4Address
    coord: dict[Coordinates]
