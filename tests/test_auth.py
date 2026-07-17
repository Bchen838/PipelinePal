



def test_register_success(client):
    response = client.post('/register', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })

    assert response.status_code == 201


def test_register_existing_email(client):
    client.post('/register', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    response = client.post('/register', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    assert response.status_code == 400


def test_register_missing_fields(client):
    response = client.post('/register', json={
        'email': '',
        'password': 'testpassword'
    })
    assert response.status_code == 400

    response = client.post('/register', json={
        'email': 'testuser@example.com',
        'password': ''
    })
    assert response.status_code == 400


def test_login_success(client):
    client.post('/register', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })

    response = client.post('/login', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data.get('token')


def test_login_wrong_password(client):
    client.post('/register', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })

    response = client.post('/login', json={
        'email': 'testuser@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401


def test_login_nonexistent_user(client): 
    response = client.post('/login', json={
        'email': 'nonexistinguser@example.com',
        'password': 'notreal'
    })

    assert response.status_code == 401