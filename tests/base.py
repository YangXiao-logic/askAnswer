import unittest

from flask import url_for

from askanswer import create_app
from askanswer.extension import db
from askanswer.models import Admin


class BaseTestCase(unittest.TestCase):

    def setup(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()
        user = Admin(admin_name='YangXiao')
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def login(self, username=None, password=None):
        if username is None and password is None:
            username = 'YangXiao'
            password = '123456'

    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_rediects=True)
