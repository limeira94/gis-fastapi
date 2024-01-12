import json
from typing import List

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from geoalchemy2 import WKTElement
from shapely.geometry import shape
from shapely.wkb import loads
from sqlalchemy.orm import Session

from gis_fast.database import get_session
from gis_fast.models import GeoData
from gis_fast.schemas import DataResponse, GeoDataResponse, UpdateName

app = FastAPI()


@app.post('/upload/', response_model=DataResponse)
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
        return DataResponse(id=new_data.id, file_name=new_data.file_name)
    else:
        raise HTTPException(status_code=400, detail='No valid features found')


@app.delete('/delete-all/')
def clear_database(session: Session = Depends(get_session)):
    try:
        session.query(GeoData).delete()
        session.commit()
        return {'detail': 'All data deleted successfully.'}
    except Exception:
        session.rollback()
        raise HTTPException(tatus_code=500, detail='An error ocurred')


@app.get('/get-all/', response_model=List[GeoDataResponse])
def get_all_data(session: Session = Depends(get_session)):
    try:
        data = session.query(GeoData).all()
        result = []
        for d in data:
            geometry = loads(bytes(d.geo_data.data))
            geo_data_str = geometry.wkt
            result.append(GeoDataResponse(id=d.id, file_name=d.file_name, geo_data=geo_data_str))
            
        return result
    except Exception:
        raise HTTPException(status_code=500, detail='An error ocurred')


@app.put('/update-name/{item_id}')
def update_name(item_id: int, update_name: UpdateName, session: Session = Depends(get_session)):
    try:
        record = session.query(GeoData).filter(GeoData.id == item_id).first()
        
        if record is None:
            raise HTTPException(status_code=404, detail='Item not found')
        
        record.file_name = update_name.new_name
        session.commit()
        
        return {'detail': 'Name updated successfully.'}
    
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail='An error ocurred')        
        