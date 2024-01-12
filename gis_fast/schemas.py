from pydantic import BaseModel


class GeoDataCreate(BaseModel):
    file_name: str
    geo_data: str


class DataResponse(BaseModel):
    id: int
    file_name: str


class GeoDataResponse(BaseModel):
    id: int
    file_name: str
    geo_data:str
    

class UpdateName(BaseModel):
    new_name: str
    