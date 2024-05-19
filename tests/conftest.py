import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.routers import auth
from app.config import settings

# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgrepass@localhost:5432/fastapidb_test"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind = engine, autocommit = False, autoflush = False)


def override_get_db():
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)

@pytest.fixture()
def client():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    user_data = {
        'email': 'test@abc.com',
        'password': 'testpass'
    }
    res = client.post('/user/create/', json = user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = 'testpass'
    # print(new_user)
    return new_user

@pytest.fixture()
def token(test_user):
    # print(test_user)
    return auth.create_access_token(id= test_user['id'], email= test_user['email'])

@pytest.fixture()
def authorized_client(client, token):
    # print(token)
    client.headers = {
        **client.headers, 
        "Authorization": f"Bearer {token}"
    }
    return client