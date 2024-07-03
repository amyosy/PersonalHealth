import pytest
from app import app, db
from models import User


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


def register_user(client, username='testuser', email='test@example.com', password='password'):
    return client.post('/register', data=dict(
        username=username,
        email=email,
        password=password,
        confirm_password=password
    ), follow_redirects=True)


def login_user(client, username='testuser', password='password'):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Personal Health Notion" in response.data


def test_register(client):
    response = register_user(client)
    assert response.status_code == 200
    assert b'Registration successful!' in response.data


def test_register_existing_user(client):
    register_user(client)
    response = register_user(client)
    assert response.status_code == 200
    assert b'Username already exists.' in response.data


def test_login(client):
    register_user(client)
    response = login_user(client)
    assert response.status_code == 200
    assert b'Login successful!' in response.data


def test_login_invalid_credentials(client):
    register_user(client)
    response = login_user(client, password='wrongpassword')
    assert response.status_code == 200
    assert b'Invalid credentials.' in response.data


def test_logout(client):
    register_user(client)
    login_user(client)
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged out.' in response.data


def test_input_data(client):
    register_user(client)
    login_user(client)
    response = client.post('/input_data', data=dict(
        blood_pressure='120/80',
        heart_rate=70,
        weight=70.5,
        height=175.0,
        sleep='8',
        stress='3'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Data submitted successfully!' in response.data


def test_reminders(client):
    register_user(client)
    login_user(client)
    response = client.post('/reminders', data=dict(
        reminder='Take medication at 8 PM'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Reminder added successfully!' in response.data


def test_dashboard(client):
    register_user(client)
    login_user(client)
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Your Health Data' in response.data
    assert b'Your Reminders' in response.data


def test_plots(client):
    register_user(client)
    login_user(client)
    # Add some health data for plotting
    client.post('/input_data', data=dict(
        blood_pressure='120/80',
        heart_rate=70,
        weight=70.5,
        height=175.0,
        sleep='8',
        stress='3'
    ), follow_redirects=True)
    response = client.get('/plots?page=1')
    assert response.status_code == 200
    assert b'Weight Over Time' in response.data
