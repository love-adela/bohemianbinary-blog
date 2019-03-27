import os

import pytest
import json

from app import create_app, db
from config import basedir
from io import BytesIO


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'The delicious way to count movie cookies!' in str(response.data)


def test_populate_dummy_admin(client):
    data = dict(username="admin", password="1234", password2="1234", email="test@test.com")
    return client.post("/bb-admin/register", data=data, follow_redirects=True)


def test_log_in_dummy_admin(client, username="admin", password="1234"):
    test_populate_dummy_admin(client)
    data = dict(username=username, password=password)
    return client.post("/bb-admin/login", data=data, follow_redirects=True)


# post : html이나 json 문자열로 반환
# client.post / get / delete /put 모두  http 헤더를 주고 resopnse를 얻는 형태.


def test_register(client):
    response = test_populate_dummy_admin(client)
    assert 'Congratulations, you are now a registered user!' in str(response.data)


def test_log_in_success(client):
    result = test_log_in_dummy_admin(client, username="admin", password="1234")
    assert 'Hi!' in str(result.data)


def test_log_in_fail(client):
    result = test_log_in_dummy_admin(client, username="notadmin", password="abcd")
    assert 'Invalid username or password' in str(result.data)


def from_register_to_log_out_dummy(client):
    test_populate_dummy_admin(client)
    test_log_in_dummy_admin(client)
    data = dict(username="admin", password='1234')
    return client.get("/bb-admin/logout", data=data, follow_redirects=True)


def test_log_out(client):
    response = from_register_to_log_out_dummy(client)
    assert 'Please log in to access this page.' in str(response.data)
    response = client.get("/bb-admin/movie", follow_redirects=True)
    assert "movie/new" not in str(response.data)


def test_login_with_auth(client):
    test_log_in_dummy_admin(client)
    response = client.get("/bb-admin/login", follow_redirects=True)
    assert response.status_code == 200
    assert "Hi!" in str(response.data)


def test_register_with_auth(client):
    test_log_in_dummy_admin(client)
    response = client.get("bb-admin/register", follow_redirects=True)
    assert response.status_code == 200
    assert "Hi!" in str(response.data)


def test_add_director(client):
    test_log_in_dummy_admin(client)
    photo = (BytesIO(b'my file contents'), "for-test.jpg")
    # TODO: for-test.jpg 파일을 삭제하라.
    data = dict(director_kr_name="장진", director_en_name="Jang Jin", photo=photo)
    response = client.post("bb-admin/director/new", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert '/director/new' in str(response.data)
    response = client.get("bb-admin/api/director")
    assert response.status_code == 200
    assert 'Jang Jin' in str(response.data)


def test_director_data_validation_on_submit_fail(client):
    test_log_in_dummy_admin(client)
    photo = (BytesIO(b'my file contents'), "for-test.jpg")
    test_add_director(client)
    data = dict(director_kr_name="", director_en_name="", photo=photo)
    response = client.post("bb-admin/director/new", data=data)
    assert "This field is required." in response.data.decode("utf-8", "strict")


def test_search_director_success(client):
    test_log_in_dummy_admin(client)
    test_add_director(client)
    response = client.get("/bb-admin/director/1", follow_redirects=True)
    assert '감독 영화 리스트에서 제거' in response.data.decode("utf-8", "strict")


def test_search_director_fail(client):
    test_log_in_dummy_admin(client)
    test_add_director(client)
    response = client.get("bb-admin/director/2", follow_redirects=True)
    assert "Director 2 not found" in response.data.decode("utf-8", "strict")


def test_edit_director(client):
    test_log_in_dummy_admin(client)
    test_add_director(client)

    response = client.get("bb-admin/api/director", follow_redirects=True)
    parsed_data = json.loads(response.data)
    assert "Jang Jin" in [x["name_en"] for x in parsed_data["directors"]]

    photo = (BytesIO(b'my file contents'), "for-test.jpg")
    data = dict(director_kr_name="장면", director_en_name="Jang Myeon", photo=photo)
    response = client.post("/bb-admin/director/edit/1", data=data, follow_redirects=True)
    print(response.data.decode("utf-8", "strict"))
    assert "감독 항목을 수정하시겠습니까?" in response.data.decode("utf-8", "strict")

    response = client.get("/bb-admin/api/director", follow_redirects=True)
    parsed_data = json.loads(response.data)
    print(parsed_data)
    assert not ("Jang Jin" in [x["name_en"] for x in parsed_data["directors"]])


def test_delete_director(client):
    pass


def test_add_actor(client):
    test_log_in_dummy_admin(client)
    photo = (BytesIO(b'my file contents'), "for-test.jpg")
    data = dict(actor_kr_name='브리라슨', movie_en_name='Brie Larson', photo=photo)
    response = client.post("/bb-admin/actor/new", data=data, follow_redirects=True)
    assert response.status_code == 200


def test_actor_data_validation_on_submit_fail(client):
    test_log_in_dummy_admin(client)
    photo = (BytesIO(b'my file contents'), "for-test.jpg")
    test_add_actor(client)
    data = dict(actor_kr_name="", actor_en_name="", photo=photo)
    response = client.post("bb-admin/actor/new", data=data)
    assert "This field is required." in response.data.decode("utf-8", "strict")


def test_edit_actor(client):
    pass


def test_delete_actor(client):
    pass


def test_search_actor_success(client):
    test_log_in_dummy_admin(client)
    test_add_actor(client)
    response = client.get("/bb-admin/actor/1", follow_redirects=True)
    assert '배우 영화 리스트에서 제거' in response.data.decode("utf-8", "strict")


def test_search_actor_fail(client):
    test_log_in_dummy_admin(client)
    test_add_actor(client)
    response = client.get("bb-admin/actor/2", follow_redirects=True)
    assert "Actor 2 not found." in response.data.decode("utf-8", "strict")


def test_add_movie(client):
    test_log_in_dummy_admin(client)
    photo = (BytesIO(b'my file contents'), "for-test.jpg")
    data = dict(movie_kr_name='캡틴마블', movie_en_name='Captain Marvel', photo=photo)
    response = client.post("/bb-admin/movie/new", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert '/movie/new' in str(response.data)
    response = client.get('/bb-admin/api/movie')
    assert response.status_code == 200
    assert 'Captain Marvel' in str(response.data)


def test_edit_movie(client):
    test_log_in_dummy_admin(client)
    test_add_movie(client)
    response = client.get("/bb-admin/api/movie/1", follow_redirects=True)
    parsed_data = json.loads(response.data)
    assert "캡틴마블" == parsed_data["name_kr"]

    photo = (BytesIO(b'my file contents'), "for-test.jpg")
    data = dict(movie_kr_name="캡틴마블링", movie_en_name="Captain Marveling", photo=photo)
    response = client.post("/bb-admin/movie/edit/1", data=data, follow_redirects=True)
    assert "새 영화 등록하기" in response.data.decode("utf-8", "strict")

    response = client.get("/bb-admin/api/movie/1", follow_redirects=True)
    parsed_data = json.loads(response.data)
    assert "캡틴마블링" == parsed_data["name_kr"]


def test_movie_data_validation_on_submit_fail(client):
    test_log_in_dummy_admin(client)
    photo = (BytesIO(b'my file contents'), "for-test.jpg")
    test_add_movie(client)
    data = dict(movie_kr_name="", movie_en_name="", photo=photo)
    response = client.post("bb-admin/movie/new", data=data)
    assert "This field is required." in response.data.decode("utf-8", "strict")


def test_delete_movie(client):
    pass


