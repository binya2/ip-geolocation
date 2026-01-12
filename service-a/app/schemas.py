from pydantic.networks import IPv4Address
from pydantic import BaseModel


ipv4_address = IPv4Address

class IpData(BaseModel):
    ip: IPv4Address
    coord: dict[str, float]
