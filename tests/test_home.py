import unittest

from flask import url_for

from askanswer.models import Question, Answer, Tag, User
from askanswer.extension import db
from askanswer import create_app


class HomeTestCase(unittest.TestCase):
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
        question = Question(title='test title', content='test content', user_id=1, tag_id=1)
        answer = Answer(content='test answer content', question=question, user_id=1)
        db.session.add(normal_user)
        db.session.add(admin_user)
        db.session.add_all([tag, question, answer])

        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('Home', data)
        self.assertIn('Tags', data)
        self.assertIn('Questions', data)
        self.assertIn('test title', data)

    def test_show_question(self):
        response = self.client.get(url_for('home.show_question', question_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('test answer content', data)

    def test_show_tags(self):
        response = self.client.get(url_for('home.show_tags'))
        data = response.get_data(as_text=True)
        self.assertIn('java', data)
        self.assertIn('java content', data)

    def test_show_tag(self):
        response = self.client.get(url_for('home.show_tag', tag_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('java', data)
        self.assertIn('test title', data)

    def test_search_question(self):
        response = self.client.get(url_for('home.search_question', search=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Please enter some words.', data)

        response = self.client.get(url_for('home.search_question', search='test'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('test', data)

    def test_show_personal_question(self):
        response = self.client.get(url_for('personal.show_personal_question', user_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('test title', data)
