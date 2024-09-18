from app import schemas

def test_get_a_post(client, test_posts):
    res = client.get("/posts")
    print(res.json())
    assert res.status_code == 200

def test_create_post(authorized_client, test_user):
    res = authorized_client.post("/posts", json={"title": "test", "content": "test content", "published": True})
    print(res.json())
    assert res.status_code == 201
    assert res.json()["title"] == "test"
    assert res.json()["content"] == "test content"
    assert res.json()["published"] == True
    assert res.json()["owner_id"] == test_user["id"]

def test_get_all_post(authorized_client, test_posts):
    res = authorized_client.get("/posts")
    print(res.json())
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


# def test_get_one_post_not_found(client, test_user):
# def test_create_post(client, test_user):
# def test_update_post(client, test_user):
# def test_delete_post(client, test_user):