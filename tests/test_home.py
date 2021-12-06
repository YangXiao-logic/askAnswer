from flask import url_for

from askanswer.models import Question, Answer, Tag
from askanswer.extension import db
from tests.base import BaseTestCase


class HomeTestCase(BaseTestCase):
    def setUp(self):
        super(HomeTestCase, self).setUp()
        tag = Tag(name='java')
        question = Question(title='test title', content='test content')
        answer = Answer(content='test answer content', question_id=1)

        db.session.add_all([tag, question, answer])
        db.session.commit()

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('Home', data)
        self.assertIn('Tags', data)
        self.assertIn('Questions', data)
        self.assertIn('test title', data)
        self.assertIn('test content', data)

    def test_show_question(self):
        response = self.client.get(url_for('home.show_question', question_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('test answer content', data)

    def test_show_tags(self):
        response = self.client.get(url_for('home.show_tags'))
        data = response.get_data(as_text=True)
        self.assertIn('java', data)
