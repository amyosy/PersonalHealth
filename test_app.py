import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Personal Health Notion" in response.data


def test_register(client):
    response = client.post('/register', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful!' in response.data


def test_login(client):
    client.post('/register', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)
    response = client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Login successful!' in response.data
