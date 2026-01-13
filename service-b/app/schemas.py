from pydantic import BaseModel, IPvAnyAddress
from pydantic_extra_types.coordinate import Coordinate


class Ip(BaseModel):
    ip: IPvAnyAddress


class IpToCoordinates(Ip):
    coord: Coordinate
