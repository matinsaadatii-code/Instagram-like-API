from fastapi.testclient import TestClient
from main import api
from database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from database import Base
from oauth2 import create_access_token
from model import PostModel
import pytest

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_ip}:{settings.db_port}/{settings.db_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope='function')
def db_fixture():
    Base.metadata.create_all(bind=engine)
    db = test_session()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function') 
def client_fixture(db_fixture):
    def override_get_db():
        yield db_fixture

    api.dependency_overrides[get_db] = override_get_db
    yield TestClient(api)
    del api.dependency_overrides[get_db]

@pytest.fixture
def create_user_fixture(client_fixture):
    user_data = {
        "email": "test_user@gmail.com",
        "password": "test_user#1234"
    }
    res = client_fixture.post('/api/create/users/', json=user_data)
    new_user_data = res.json()
    new_user_data['password'] = user_data['password']

    assert res.status_code == 201
    return new_user_data

@pytest.fixture
def create_user_fixture2(client_fixture):
    user_data = {
        "email": "test_user2@gmail.com",
        "password": "test_user2#1234"
    }
    res = client_fixture.post('/api/create/users/', json=user_data)
    new_user_data = res.json()
    new_user_data['password'] = user_data['password']

    assert res.status_code == 201
    return new_user_data

@pytest.fixture
def create_access_token_fixture(create_user_fixture):
    return create_access_token({"user_id": create_user_fixture['id']})

@pytest.fixture
def authorized_user_fixture(client_fixture, create_access_token_fixture):
    client_fixture.headers = {
        **client_fixture.headers,
        "Authorization": f"Bearer {create_access_token_fixture}"
    }

    return client_fixture

@pytest.fixture
def create_post_fixture(create_user_fixture, create_user_fixture2, db_fixture):
    posts_entry = [
        {
            'title': 'test title 1',
            'content': 'this is test content 1',
            'user_id': create_user_fixture['id'],
        },  
        {
            'title': 'test title 2',
            'content': 'this is test content 2',
            'user_id': create_user_fixture2['id'],
        },
    ]

    def create_post_model(post):
        return PostModel(**post)

    posts_map = map(create_post_model, posts_entry)
    posts = list(posts_map)

    db_fixture.add_all(posts)
    db_fixture.commit()

    posts = db_fixture.query(PostModel).all()
    return posts