import json

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from geoalchemy2 import WKTElement
from shapely.geometry import shape
from sqlalchemy.orm import Session

from gis_fast.database import get_session
from gis_fast.models import GeoData
from gis_fast.schemas import GeoDataResponse

app = FastAPI()


@app.post('/upload/', response_model=GeoDataResponse)
async def upload_geo_data(
    file: UploadFile = File(...), session: Session = Depends(get_session)
):
    geojson_data = await file.read()
    geojson = json.loads(geojson_data.decode('utf-8'))

    file_name = file.filename
    new_data = None

    if geojson.get('type') == 'FeatureCollection':
        for feature in geojson.get('features', []):
            geometry = shape(feature['geometry'])
            wkt_geometry = WKTElement(geometry.wkt)

            new_data = GeoData(
                file_name=file_name,
                geo_data=wkt_geometry,
            )
            session.add(new_data)

        session.commit()
        session.refresh(new_data)
    if new_data is not None:
        return GeoDataResponse(id=new_data.id, file_name=new_data.file_name)
    else:
        raise HTTPException(status_code=400, detail='No valid features found')
