import pytest
import jwt
from app import app, key_store

def test_jwks():
    client = app.test_client()
    response = client.get('/jwks')
    assert response.status_code == 200
    keys = response.get_json()['keys']
    assert len(keys) > 0  # Ensure keys are returned

def test_auth():
    client = app.test_client()
    response = client.post('/auth')
    assert response.status_code == 200
    token = response.get_json()['token']
    assert token is not None

def test_expired_auth():
    client = app.test_client()
    response = client.post('/auth?expired=true')
    assert response.status_code == 200
    token = response.get_json()['token']
    assert token is not None
