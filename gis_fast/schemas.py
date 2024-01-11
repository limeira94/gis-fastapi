from pydantic import BaseModel


class GeoDataCreate(BaseModel):
    file_name: str
    geo_data: str


class GeoDataResponse(BaseModel):
    id: int
    file_name: str
