from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class GeoData(Base):
    __tablename__ = 'geodata'

    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    geo_data = Column(Geometry('GEOMETRY'))
