import json

from fastapi.testclient import TestClient

from gis_fast.app import app

client = TestClient(app)


def test_upload_geo_data():
    geojson_data = {
        'type': 'Feature',
        'properties': {},
        'geometry': {'type': 'Point', 'coordinates': [-23.533773, -46.625290]},
    }

    response = client.post(
        '/upload/',
        json={
            'file_name': 'test.geojson',
            'geo_data': json.dumps(geojson_data),
        },
    )

    assert response.status_code == 200
    assert 'id' in response.json()
