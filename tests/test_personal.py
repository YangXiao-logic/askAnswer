import unittest

from flask import url_for
from flask_login import current_user
from askanswer.models import Question, Answer, Tag, User
from askanswer.extension import db
from askanswer import create_app


class PersonalTestCase(unittest.TestCase):
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
        tag2 = Tag(name='python', content='python content')
        question = Question(title='test title', content='test content', user_id=1)
        question.tags.append(tag)
        answer = Answer(content='test answer content', question=question, user_id=1)
        db.session.add(normal_user)
        db.session.add(admin_user)
        db.session.add_all([tag, tag2, question, answer])

        db.session.commit()
        self.login()

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

    def test_show_mine_question(self):
        response = self.client.get(url_for('personal.show_mine_question'))
        data = response.get_data(as_text=True)
        self.assertIn('test title', data)

    def test_edit_question(self):
        response = self.client.get(url_for('personal.edit_question'))
        data = response.get_data(as_text=True)
        self.assertIn('Publish Question', data)

        response = self.client.post(url_for('personal.edit_question'), data=dict(
            title='test question edit',
            content='test question edit content',
            tag=1,
            tag2=2,
            user=current_user
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Ask question success', data)
        self.assertIn('test question edit', data)

        response = self.client.get(url_for('home.show_question', question_id=2))
        data = response.get_data(as_text=True)
        self.assertIn('test question edit content', data)

    def test_edit_answer(self):
        response = self.client.get(url_for('personal.edit_answer', question_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('Publish Answer', data)

        response = self.client.post(url_for('personal.edit_answer', question_id=1), data=dict(
            content='test answer edit content',
            user=current_user
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Answer submit success', data)
        self.assertIn('test answer edit content', data)
