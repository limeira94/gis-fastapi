import json
from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from gis_fast.app import app
from gis_fast.models import GeoData

client = TestClient(app)


@pytest.fixture
def prepare_data(db_session):
    test_record = GeoData(
        file_name='test.geojson',
        geo_data=from_shape(Point(-46.625290, -23.533773)),
    )
    db_session.add(test_record)
    db_session.commit()
    return test_record.id


def test_upload_geo_data():
    geojson_data = {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [-46.625290, -23.533773],
                },
                'properties': {'name': 'Sample Point'},
            }
        ],
    }
    geojson_str = json.dumps(geojson_data)
    geojson_bytes = geojson_str.encode('utf-8')
    geojson_file = BytesIO(geojson_bytes)

    data = {'file': ('test.geojson', geojson_file, 'application/geo+json')}
    response = client.post('/upload/', files=data)

    assert response.status_code == 201
    response_json = response.json()
    assert 'id' in response_json
    assert response_json['file_name'] == 'test.geojson'


def test_delete_all_data():
    response = client.delete('/delete-all/')
    assert response.status_code == 200
    assert response.json() == {'detail': 'All data deleted successfully.'}


def test_get_all_data():
    response = client.get('/get-all/')
    assert response.status_code == 200
    assert response.json() == []


def test_update_name_not_found():
    response = client.put('/update-name/', json={'id': 1, 'name': 'New Name'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_update_name_found(prepare_data):
    test_id = prepare_data

    update_data = {'new_name': 'Lims'}

    response = client.put(f'/update-name/{test_id}/', json=update_data)

    assert response.status_code == 200
    assert response.json() == {'detail': 'Name updated successfully.'}
