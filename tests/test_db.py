def test_database_connection(db_session):
    with db_session.begin():
        pass
    assert True
