def test_root(client_fixture):
    res = client_fixture.get('/')
    assert res.json().get('message') == 'FastAPI is running'
    assert res.status_code == 200