from schema import UserBase
import pytest

def test_create_user(client_fixture, create_user_fixture):
    res = client_fixture.post('/api/create/users/', json={"email": "test_user@gmail.com", "password": "test_user#1234"})
    new_user = UserBase(**res.json())

    assert new_user.email == "test_user@gmail.com"
    assert res.status_code == 201

def test_login(client_fixture, create_user_fixture):
    res = client_fixture.post('/login/', json={"email": create_user_fixture['email'], "password": create_user_fixture['password']})

    assert res.status_code == 200

@pytest.mark.parametrize("email, password", [
    ('test@gmail.com', 'test')
])
def test_incorrect_login(client_fixture, email, password):
    res = client_fixture.post('/login/', json={"email": email, "password": password})

    assert res.status_code == 403
    assert res.json().get('detail') == 'Invalid Credentials'