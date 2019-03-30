from io import BytesIO
from fixtures import *

import json


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
    data = dict(director_kr_name="장진", director_en_name="Jang Jin", photo=photo)
    response = client.post("/bb-admin/director/new", data=data, follow_redirects=True)
    assert response.status_code == 200


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

    photo = ([p.decode('utf-8') for p in BytesIO(b'my file contents')], "for-test.jpg")
    data = json.dumps({'name_kr': "장면", 'name_en': "Jang Myeon", 'photo': photo})
    response = client.post("/bb-admin/api/director/1", data=data, content_type='application/json')
    parsed_data = json.loads(response.data)
    assert not ("Jang Jin" in [x["name_en"] for x in parsed_data["directors"]])
    assert ("Jang Myeon" in [x["name_en"] for x in parsed_data["directors"]])


def test_edit_movie_of_director(client):
    test_log_in_dummy_admin(client)
    test_add_director(client)

    response = client.get("bb-admin/api/movie-with-director/1", follow_redirects=True)
    parsed_data = json.loads(response.data)
    print(parsed_data)
    assert "Captain Marvel" in [x["name_en"] for x in parsed_data["directors"]]

    photo = ([p.decode('utf-8') for p in BytesIO(b'my file contents')], "for-test.jpg")
    data = json.dumps({'name_kr': "캡틴마블링", 'name_en': "Captain Marveling", 'photo': photo})
    response = client.post("/bb-admin/api/director/1", data=data, content_type='application/json')
    parsed_data = json.loads(response.data)
    assert not ("Captain Marvel" in [x["name_en"] for x in parsed_data["directors"]])
    assert ("Captain Marveling" in [x["name_en"] for x in parsed_data["directors"]])


def test_delete_director(client):
    test_log_in_dummy_admin(client)
    test_add_director(client)
    response = client.get("bb-admin/api/director", follow_redirects=True)
    parsed_data = json.loads(response.data)
    assert "Jang Jin" in [x["name_en"] for x in parsed_data["directors"]]

    response = client.delete("bb-admin/api/director/1", follow_redirects=True)
    parsed_data = json.loads(response.data)
    assert not "Jang Jin" in [x["name_en"] for x in parsed_data["directors"]]


def test_add_actor(client):
    test_log_in_dummy_admin(client)
    photo = (BytesIO(b'my file contents'), "for-test.jpg")
    data = dict(actor_kr_name='브리라슨', actor_en_name='Brie Larson', photo=photo)
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
    test_log_in_dummy_admin(client)
    test_add_actor(client)

    response = client.get("bb-admin/api/actor", follow_redirects=True)
    parsed_data = json.loads(response.data)
    assert "Brie Larson" in [x["name_en"] for x in parsed_data["actors"]]

    photo = ([p.decode('utf-8') for p in BytesIO(b'my file contents')], "for-test.jpg")
    data = json.dumps({'name_kr': "주열매", 'name_en': "Ju Yeol Mae", 'photo': photo})
    response = client.post("/bb-admin/api/actor/1", data=data, content_type='application/json')
    parsed_data = json.loads(response.data)
    assert not ("Brie Larson" in [x["name_en"] for x in parsed_data["actors"]])
    assert "Ju Yeol Mae" in [x["name_en"] for x in parsed_data["actors"]]


def test_delete_actor(client):
    test_log_in_dummy_admin(client)
    test_add_actor(client)
    response = client.get("bb-admin/api/actor", follow_redirects=True)
    parsed_data = json.loads(response.data)
    assert "Brie Larson" in [x["name_en"] for x in parsed_data["actors"]]

    response = client.delete("bb-admin/api/actor/1", follow_redirects=True)
    parsed_data = json.loads(response.data)
    assert not "Brie Larson" in [x["name_en"] for x in parsed_data["actors"]]


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


def test_if_this_movie_exits(client):
    test_log_in_dummy_admin(client)
    test_add_movie(client)
    response = client.get('/bb-admin/api/movie', follow_redirects=True)
    assert response.status_code == 200
    assert 'Captain Marvel' in str(response.data)


def test_if_cookie_exists_in_this_movie(client):
    test_log_in_dummy_admin(client)
    test_add_movie(client)
    response = client.get('/bb-admin/api/movie/1/cookie', follow_redirects=True)
    assert response.status_code == 200
    parsed_data = json.loads(response.data)
    assert parsed_data["number_of_cookies"] is None

    photo = ([p.decode('utf-8') for p in BytesIO(b'my file contents')], 'for-test.jpg')
    data = json.dumps({'name_kr': '캡틴마블링', 'name_en': 'Captain Marveling', 'photo': photo, 'number_of_cookies': 5})
    response = client.post('/bb-admin/api/movie/1/cookie', data=data, follow_redirects=True)
    parsed_data = json.loads(response.data)
    print(parsed_data)
    assert parsed_data["movie"]["number_of_cookies"] == 5


def test_edit_movie(client):
    test_log_in_dummy_admin(client)
    test_add_movie(client)
    response = client.get("/bb-admin/api/movie", follow_redirects=True)
    parsed_data = json.loads(response.data)
    assert "캡틴마블" in [x["name_kr"] for x in parsed_data["movies"]]

    photo = ([p.decode('utf-8') for p in BytesIO(b'my file contents')], 'for-test.jpg')
    data = json.dumps({'name_kr': '캡틴마블링', 'name_en': 'Captain Marveling', 'photo': photo})
    response = client.post("/bb-admin/api/movie/1", data=data, content_type='application/json')
    parsed_data = json.loads(response.data)
    assert not ("Captain Marvel" in [x["name_en"] for x in parsed_data["movies"]])
    assert "Captain Marveling" in [x["name_en"] for x in parsed_data["movies"]]


def test_movie_data_validation_on_submit_fail(client):
    test_log_in_dummy_admin(client)
    photo = (BytesIO(b'my file contents'), "for-test.jpg")
    test_add_movie(client)
    data = dict(movie_kr_name="", movie_en_name="", photo=photo)
    response = client.post("bb-admin/movie/new", data=data)
    assert "This field is required." in response.data.decode("utf-8", "strict")


def test_delete_movie(client):
    pass


def test_match_movie_with_actor(client):
    test_log_in_dummy_admin(client)
    test_add_actor(client)
    test_add_movie(client)

    response = client.get("/bb-admin/api/movie-with-actor/1", content_type='application/json')
    parsed_data = json.loads(response.data)
    assert not ("Monster" in [x["name_en"] for x in parsed_data["movies"]])
    assert ("Captain Marvel" in [x["name_en"] for x in parsed_data["movies"]])

    response = client.get("/bb-admin/api/movie-with-actor/1?keyword=Ca", content_type='application/json')
    parsed_data = json.loads(response.data)
    assert ("Captain Marvel" in [x["name_en"] for x in parsed_data["movies"]])

    response = client.get("/bb-admin/api/movie-with-actor/1?keyword=Ka", content_type='application/json')
    parsed_data = json.loads(response.data)
    assert not ("Captain Marvel" in [x["name_en"] for x in parsed_data["movies"]])


def test_match_movie_with_director(client):
    test_log_in_dummy_admin(client)
    test_add_director(client)
    test_add_movie(client)

    response = client.get("/bb-admin/api/movie-with-director/1", content_type='application/json')
    parsed_data = json.loads(response.data)
    assert not ("Monster" in [x["name_en"] for x in parsed_data["movies"]])
    assert ("Captain Marvel" in [x["name_en"] for x in parsed_data["movies"]])

    response = client.get("/bb-admin/api/movie-with-actor/1?keyword=Ca", content_type='application/json')
    parsed_data = json.loads(response.data)
    assert ("Captain Marvel" in [x["name_en"] for x in parsed_data["movies"]])

    response = client.get("/bb-admin/api/movie-with-actor/1?keyword=Ka", content_type='application/json')
    parsed_data = json.loads(response.data)
    assert not ("Captain Marvel" in [x["name_en"] for x in parsed_data["movies"]])
