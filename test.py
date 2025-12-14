import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def get_token(client):
    r = client.post('/login', json={
        'username': 'admin',
        'password': 'admin'
    })
    return r.get_json()['token']

def test_health(client):
    r = client.get('/health')
    assert r.status_code == 200

def test_get_flowers(client):
    token = get_token(client)
    r = client.get('/flowers', headers={'x-access-token': token})
    assert r.status_code == 200

def test_create_flower(client):
    token = get_token(client)
    r = client.post('/flowers',
        headers={'x-access-token': token},
        json={
            "name":"TestFlower",
            "color":"Blue",
            "season":"Spring",
            "seedling_cost":10,
            "planting_month":"January",
            "watering_schedule":"Daily",
            "description":"Test flower"
        }
    )
    assert r.status_code == 201

def test_update_flower(client):
    token = get_token(client)
    r = client.put('/flowers/1',
        headers={'x-access-token': token},
        json={"color":"Dark Red"}
    )
    assert r.status_code == 200

def test_delete_flower(client):
    token = get_token(client)
    r = client.delete('/flowers/1', headers={'x-access-token': token})
    assert r.status_code == 200
