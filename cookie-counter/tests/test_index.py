import os
import pytest

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
    res = client.get('/')
    assert res.status_code == 200
    assert 'The delicious way to count movie cookies!' in str(res.data)


def populate_dummy_admin(client):
    data = dict(username="admin", password="1234", password2="1234", email="test@test.com")
    return client.post("/bb-admin/register", data=data, follow_redirects=True)


def log_in_dummy_admin(client):
    populate_dummy_admin(client)
    data = dict(username="admin", password="1234")
    return client.post("/bb-admin/login", data=data, follow_redirects=True)


def test_register(client):
    res = populate_dummy_admin(client)
    assert 'Congratulations, you are now a registered user!' in str(res.data)


def test_log_in(client):
    res = log_in_dummy_admin(client)
    assert 'Hi!' in str(res.data)


def test_director_new_post(client):
    log_in_dummy_admin(client)
    photo = (BytesIO(b'my file contents'), "for-test.jpg")
    # TODO: for-test.jpg 파일을 삭제하라.
    data = dict(director_kr_name="장진", director_en_name="Jang Jin", photo=photo)
    res = client.post("/bb-admin/director/new", data=data, follow_redirects=True)
    assert res.status_code == 200
    assert '/director/new' in str(res.data)
    res = client.get("/bb-admin/api/director")
    assert res.status_code == 200
    assert 'Jang Jin' in str(res.data)
