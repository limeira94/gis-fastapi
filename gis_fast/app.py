from fastapi import FastAPI

app = FastAPI()


@app.post('/upload/')
def upload_geo_data()