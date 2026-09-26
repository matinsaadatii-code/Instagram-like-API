from schema import PostSchemaResponse, Post
import pytest

def test_get_published_posts(authorized_user_fixture, create_post_fixture):
    res = authorized_user_fixture.get('/api/get/posts/')

    def validate(post):
        return PostSchemaResponse(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    sorted_posts = sorted(posts_list, key=lambda post:post.id)
    sorted_posts2 = sorted(create_post_fixture, key=lambda post:post.id)

    assert len(res.json()) == len(create_post_fixture)
    assert res.status_code == 200
    assert sorted_posts[0].id == sorted_posts2[0].id
    
def test_get_all_posts(authorized_user_fixture, create_post_fixture):
    res = authorized_user_fixture.get('/api/get/all/posts/')

    def validate(post):
        return PostSchemaResponse(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    sorted_posts = sorted(posts_list, key=lambda post:post.id)
    sorted_posts2 = sorted(create_post_fixture, key=lambda post:post.id)

    assert len(res.json()) == len(create_post_fixture)
    assert res.status_code == 200
    assert sorted_posts[0].id == sorted_posts2[0].id

def test_get_your_posts(authorized_user_fixture, create_post_fixture):
    res = authorized_user_fixture.get('/api/get/your/posts/')

    def validate(post):
        return PostSchemaResponse(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    sorted_posts = sorted(posts_list, key=lambda post:post.id)
    sorted_posts2 = sorted(create_post_fixture, key=lambda post:post.id)
    user_posts = [p for p in create_post_fixture if p.user_id == create_post_fixture[0].id]

    assert len(res.json()) == len(user_posts)
    assert res.status_code == 200
    assert sorted_posts[0].id == sorted_posts2[0].id

def test_get_unauthorized_user_get_your_posts(client_fixture, create_post_fixture):
    res = client_fixture.get('/api/get/your/posts/')

    assert res.status_code == 401

def test_get_one_post(authorized_user_fixture, create_post_fixture):
    res = authorized_user_fixture.get(f'/api/get/posts/{create_post_fixture[0].id}/')
    post = PostSchemaResponse(**res.json())

    assert res.status_code == 200
    assert post.id == create_post_fixture[0].id
    assert post.title == create_post_fixture[0].title
    assert post.content == create_post_fixture[0].content

def test_get_one_post_not_exists(authorized_user_fixture):
    res = authorized_user_fixture.get('/api/get/post/456487/')

    assert res.status_code == 404

@pytest.mark.parametrize("title, content, published", [
    ('test title 3', 'this is test content 3', True),
    ('test title 4', 'this is test content 4', False),
    ('test title 5', 'this is test content 5', True),
    ('test title 6', 'this is test content 6', False),
])
def test_create_post(authorized_user_fixture, create_user_fixture, create_post_fixture, title, content, published):
    res = authorized_user_fixture.post('/api/create/posts/', json={'title': title, 'content': content, 'published': published})
    created_post = Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published

def test_get_unauthorized_user_create_post(client_fixture, create_post_fixture):
    res = client_fixture.post('/api/create/posts/', json={'title': 'test title 7', 'content': 'this is test content 7', 'published': True})

    assert res.status_code == 401

def test_get_unauthorized_user_delete_post(client_fixture, create_post_fixture):
    res = client_fixture.delete(f'/api/delete/posts/{create_post_fixture[0].id}/')

    assert res.status_code == 401

def test_delete_post(authorized_user_fixture, create_post_fixture):
    res = authorized_user_fixture.delete(f'/api/delete/posts/{create_post_fixture[0].id}/')

    assert res.status_code == 204

def test_delete_non_exist_post(authorized_user_fixture):
    res = authorized_user_fixture.delete('/api/delete/posts/4597/')

    assert res.status_code == 404

def test_delete_other_user_post(authorized_user_fixture, create_post_fixture):
    res = authorized_user_fixture.delete(f'/api/delete/posts/{create_post_fixture[1].id}')

    assert res.status_code == 403

def test_update_post(authorized_user_fixture, create_post_fixture):
    data = {
        'title': 'test title 8 (updated)',
        'content': 'this is test title 8 (updated)',
        'id': create_post_fixture[0].id
    }
    res = authorized_user_fixture.put(f'/api/update/posts/{create_post_fixture[0].id}/', json=data)
    updated_post = Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_get_unauthorized_user_update_post(client_fixture, create_post_fixture):
    data = {
        'title': 'test title 8 (updated)',
        'content': 'this is test title 8 (updated)',
        'id': create_post_fixture[0].id
    }
    res = client_fixture.put(f'/api/update/posts/{create_post_fixture[0].id}/', json=data)

    assert res.status_code == 401

def test_update_non_exist_post(authorized_user_fixture, create_post_fixture):
    data = {
        'title': 'test title 8 (updated)',
        'content': 'this is test title 8 (updated)',
        'id': create_post_fixture[0].id
    }
    res = authorized_user_fixture.put(f'/api/update/posts/4654987/', json=data)

    assert res.status_code == 404

def test_update_other_user_post(authorized_user_fixture, create_post_fixture):
    data = {
        'title': 'test title 8 (updated)',
        'content': 'this is test title 8 (updated)',
        'id': create_post_fixture[0].id
    }
    res = authorized_user_fixture.put(f'/api/update/posts/{create_post_fixture[1].id}/', json=data)

    assert res.status_code == 403