import json

from fastapi import Depends, FastAPI
from geoalchemy2 import WKTElement
from shapely.geometry import shape
from sqlalchemy.orm import Session

from gis_fast.database import get_session
from gis_fast.models import GeoData
from gis_fast.schemas import GeoDataCreate, GeoDataResponse

app = FastAPI()


@app.post('/upload/', response_model=GeoDataResponse)
def upload_geo_data(
    geo_data: GeoDataCreate, session: Session = Depends(get_session)
):
    geojson = json.loads(geo_data.geo_data)

    geometry = shape(geojson['geometry'])

    wkt_geometry = WKTElement(geometry.wkt)

    new_data = GeoData(
        file_name=geo_data.file_name,
        geo_data=wkt_geometry,
    )
    session.add(new_data)
    session.commit()
    session.refresh(new_data)

    return GeoDataResponse(id=new_data.id, file_name=new_data.file_name)
