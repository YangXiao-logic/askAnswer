import unittest

from flask import url_for

from askanswer.models import Question, Answer, Tag, User
from askanswer.extension import db
from askanswer import create_app


class AdminTestCase(unittest.TestCase):
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

        tag1 = Tag(name='flask', content='flask content')
        tag2 = Tag(name='html', content='html content')

        db.session.add_all([tag1, tag2])
        db.session.commit()
        self.login('admin', 'admin')

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

    def test_edit_tag_title(self):
        response = self.client.put(url_for('admin.edit_tag_name', tag_id=2), json=dict(name='new java'))
        data = response.get_json()
        self.assertEqual(data['message'], 'Tag name updated.')

    def test_edit_tag_content(self):
        response = self.client.put(url_for('admin.edit_tag_content', tag_id=2), json=dict(content='new java content'))
        data = response.get_json()
        self.assertEqual(data['message'], 'Tag content updated.')

    def test_delete_tag(self):
        response = self.client.delete(url_for('admin.delete_tag', tag_id=3))
        self.assertEqual(Tag.query.get(3), None)

    def test_delete_answer(self):
        response = self.client.delete(url_for('admin.delete_answer', answer_id=1))
        self.assertEqual(Answer.query.get(1), None)

    def test_delete_question(self):
        response = self.client.delete(url_for('admin.delete_question', question_id=1))
        self.assertEqual(Question.query.get(1), None)

    def test_delete_user(self):
        response = self.client.delete(url_for('admin.delete_user', user_id=1))
        self.assertEqual(User.query.get(1), None)

    def test_new_tag(self):
        response = self.client.get(url_for('admin.new_tag'))
        data = response.get_data(as_text=True)
        self.assertIn('Publish Tag', data)

        response = self.client.post(url_for('admin.new_tag'), data=dict(
            name='Vue',
            content='Vue content'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Tag submit success.', data)
        self.assertIn('Vue', data)
        self.assertIn('Vue content', data)
