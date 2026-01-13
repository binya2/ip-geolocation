from pydantic.networks import IPvAnyAddress
from pydantic import BaseModel
from pydantic_extra_types.coordinate import Coordinate

ipvany_address = IPvAnyAddress

class IpData(BaseModel):
    ip: IPvAnyAddress
    coord: Coordinate
