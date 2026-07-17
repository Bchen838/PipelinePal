import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


@pytest.fixture
def auth_headers(client):
    client.post('/register', json={
        'email': 'testuser@email.com',
        'password': 'testpassword'
    })

    response = client.post('/login', json={
        'email': 'testuser@email.com',
        'password': 'testpassword'
    })

    data = response.get_json()
    token = data.get('token')
    return {'Authorization': f'Bearer {token}'}