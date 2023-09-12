def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200
