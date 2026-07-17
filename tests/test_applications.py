def test_get_applications(client, auth_headers):
    response = client.get('/applications', headers=auth_headers)

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_application(client, auth_headers):
    response = client.post('/applications', headers=auth_headers, json={
        'company': 'Google',
        'role': 'Software Engineer',
        'status': 'Applied',
        'date_applied': '7/16/2026'
    })
    data = response.get_json()
    assert data['company'] == 'Google'
    assert data['role'] == 'Software Engineer'
    assert data['status'] == 'Applied'
    assert data['date_applied'] == '7/16/2026'
    assert 'id' in data

    assert response.status_code == 201
    


def test_get_single_application(client, auth_headers):
    response = client.post('/applications', headers=auth_headers, json={
        'company': 'Google',
        'role': 'Software Engineer',
        'status': 'Applied',
        'date_applied': '7/16/2026'
    })

    data = response.get_json()
    app_id = data['id']
    
    response2 = client.get(f'/applications/{app_id}', headers=auth_headers)
    data2 = response2.get_json()
    assert response2.status_code == 200
    assert data2['company'] == 'Google'
    assert data2['role'] == 'Software Engineer'
    assert data2['status'] == 'Applied'
    assert data2['date_applied'] == '7/16/2026'
    assert 'id' in data2


def test_update_application(client, auth_headers):
    response = client.post('/applications', headers=auth_headers, json={
        'company': 'Google',
        'role': 'Software Engineer',
        'status': 'Applied',
        'date_applied': '7/16/2026'
    })

    data = response.get_json()
    app_id = data['id']

    response2 = client.put(f'/applications/{app_id}', headers=auth_headers, json={
        'status': 'Interviewing'
    })

    data2 = response2.get_json()
    assert response2.status_code == 200
    assert data2['status'] == 'Interviewing'
    


def test_delete_application(client, auth_headers):
    response = client.post('/applications', headers=auth_headers, json={
        'company': 'Google',
        'role': 'Software Engineer',
        'status': 'Applied',
        'date_applied': '7/16/2026'
    })

    data = response.get_json()
    app_id = data['id']

    response2 = client.delete(f'/applications/{app_id}', headers=auth_headers)
    assert response2.status_code == 204

    response3 = client.get(f'/applications/{app_id}', headers=auth_headers)
    assert response3.status_code == 404


def test_unauthorized_access(client, auth_headers):
    user1 = client.post('/applications', headers=auth_headers, json={
        'company': 'Google',
        'role': 'Software Engineer',
        'status': 'Applied',
        'date_applied': '7/16/2026'
    })

    user1_id = user1.get_json()['id']

    client.post('/register', json={
        'email': 'testuser2@example.com',
        'password': 'testpassword2'
    })

    response1 = client.post('/login', json={
        'email': 'testuser2@example.com',
        'password': 'testpassword2'
    })
    data = response1.get_json()
    token = data.get('token')

    response2 = client.get(f'/applications/{user1_id}', headers={'Authorization': f'Bearer {token}'})
    assert response2.status_code == 403
