def test_index(client):
    response = client.get('/')
    assert b"<title>PreFlight</title>" in response.data
    assert response.status_code == 200
    