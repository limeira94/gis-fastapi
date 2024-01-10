from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GeoData(Base):
    __tablename__ = 'geodata'

    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    geo_data = Column(Geometry('GEOMETRY'))