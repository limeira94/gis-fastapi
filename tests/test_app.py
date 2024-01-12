import json
from io import BytesIO

from fastapi.testclient import TestClient

from gis_fast.app import app

client = TestClient(app)


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

    assert response.status_code == 200
    response_json = response.json()
    assert 'id' in response_json
    assert response_json['file_name'] == 'test.geojson'
