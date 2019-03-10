#!/usr/bin/env python

import os
import unittest

from app import create_app, db
from config import basedir


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

    # Register

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

    # Login

    # New Director
