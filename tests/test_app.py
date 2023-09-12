from models import Users, db


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_register(client):
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpass',
        'confirm_password': 'testpass'
    }
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200


def test_login(client):
    response = client.get('/login')
    data = {
        'username': 'testuser',
        'password': 'testpass'
    }
    response = client.post('/login', data=data, follow_redirects=True)
    assert response.status_code == 200


def test_logout(client):
    response = client.post(
        '/login', data={'username': 'admin', 'password': 'admin'})
    response = client.get('/logout')
    response = client.get('/')
    assert response.status_code == 200
