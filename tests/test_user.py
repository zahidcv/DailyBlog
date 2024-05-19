import pytest
from jose import jwt

from app import schemas
from app.config import settings


def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'Hello from Zahid'
    assert res.status_code == 200
    
def test_create_user(client):
    tmail = "ast@gmail.com"
    res = client.post(
        "/user/create",
        # headers={"X-Token": "coneofsilence"},
        json={"email": tmail, "password": "tpass"}
    )
    
    new_user = schemas.ShowUser(**res.json())
    assert new_user.email == tmail
    assert res.status_code == 201


def test_login(client, test_user):
    
    res = client.post(
        "/login",
        data={
            "username": test_user['email'] ,
            "password": test_user['password']
        }
    )
    # print(res.json())
    
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, settings.algorithm)
    
    assert payload.get('id') == test_user['id']
    assert payload.get('email') == test_user['email']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code",[
    ('wrongemail', 'testpass', 404),
    ('test@abc.com', 'wrongpass', 404),
    (None, 'testpass', 422),
    ('test@abc.com', None, 422),
    
])
def test_incorrect_login(client, test_user, email, password, status_code):
    
    res = client.post(
        "/login",
        data={
            "username": email,
            "password": password
        }
    )

    assert res.status_code == status_code