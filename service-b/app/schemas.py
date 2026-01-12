from pydantic import BaseModel, IPvAnyAddress, Field


class Ip(BaseModel):
    ip: IPvAnyAddress


class IpToCoordinates(Ip):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude (-180 to 180)")
