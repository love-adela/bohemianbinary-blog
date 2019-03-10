#!/usr/bin/env python

import os
import unittest

from app import create_app, db
from config import basedir
from io import BytesIO


class TestCase(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app
        self.client = app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('The delicious way to count movie cookies!', str(res.data))

    def populate_dummy_admin(self):
        data = dict(username="admin", password="1234", password2="1234", email="test@test.com")
        return self.client.post("/bb-admin/register", data=data, follow_redirects=True)

    def log_in_dummy_admin(self):
        self.populate_dummy_admin()
        data = dict(username="admin", password="1234")
        return self.client.post("/bb-admin/login", data=data, follow_redirects=True)

    def test_register(self):
        res = self.populate_dummy_admin()
        self.assertIn('Congratulations, you are now a registered user!', str(res.data))

    def test_log_in(self):
        res = self.log_in_dummy_admin()
        self.assertIn('Hi!', str(res.data))

    def test_director_new_post(self):
        self.log_in_dummy_admin()
        photo = (BytesIO(b'my file contents'), "for-test.jpg")
        # TODO: for-test.jpg 파일을 삭제하라.
        data = dict(director_kr_name="장진", director_en_name="Jang Jin", photo=photo)
        res = self.client.post("/bb-admin/director/new", data=data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('/director/new', str(res.data))
        res = self.client.get("/bb-admin/api/director")
        self.assertEqual(res.status_code, 200)
        self.assertIn('Jang Jin', str(res.data))
