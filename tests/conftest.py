import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql+psycopg2://postgres:1234@localhost/db-fastgis'


@pytest.fixture
def db_engine():
    return create_engine(DATABASE_URL)


@pytest.fixture
def db_session(db_engine):
    SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=db_engine
    )
    session = SessionLocal()
    yield session
    session.close()
