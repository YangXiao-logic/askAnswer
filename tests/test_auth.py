import unittest

from flask import url_for

from askanswer import create_app
from askanswer.extension import db
from askanswer.models import Question, Answer, Tag, User


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.app_context = app.test_request_context()
        self.app_context.push()
        db.create_all()
        self.client = app.test_client()
        admin_user = User(username='admin', is_admin=True)
        admin_user.set_password('admin')
        normal_user = User(username='Yang Xiao')
        normal_user.set_password('123456')

        tag = Tag(name='java', content='java content')
        question = Question(title='test title', content='test content', user_id=1)
        question.tags.append(tag)
        answer = Answer(content='test answer content', question=question, user_id=1)
        db.session.add(normal_user)
        db.session.add(admin_user)
        db.session.add_all([tag, question, answer])

        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def login(self, username=None, password=None):
        if username is None and password is None:
            username = 'Yang Xiao'
            password = '123456'

        return self.client.post(url_for('auth.login'), data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_redirects=True)

    def test_login_user(self):
        response = self.login()
        data = response.get_data(as_text=True)
        self.assertIn('Login success.', data)

    def test_login_admin_user(self):
        response = self.login(username='admin', password='admin')
        data = response.get_data(as_text=True)
        self.assertIn('Login success.', data)

    def test_fail_login(self):
        response = self.login(username='wrong-username', password='wrong-password')
        data = response.get_data(as_text=True)
        self.assertIn('No account.', data)
        response = self.login(username='Yang Xiao', password='wrong-password')
        data = response.get_data(as_text=True)
        self.assertIn('Invalid username or password.', data)

    def test_logout_user(self):
        self.login()
        response = self.logout()
        data = response.get_data(as_text=True)
        self.assertIn('Logout success.', data)
