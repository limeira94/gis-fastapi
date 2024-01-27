#!/bin/sh

dockerize -wait tcp://gisfast_db:5432 -timeout 60s

poetry run alembic upgrade head

poetry run uvicorn --host 0.0.0.0 --port 8000 gis_fast.app:app