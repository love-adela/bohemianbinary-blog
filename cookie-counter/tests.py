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
        assert 'The delicious way to count movie cookies!' in str(res.data)
