from faker import Faker
import random
from sqlalchemy.exc import IntegrityError

from askanswer.extension import db
from askanswer.models import User, Tag, Question, Answer

fake = Faker()


def fake_users(count=5):
    for i in range(count):
        user = User(username=fake.name())
        user.set_password('123456')
        try:
            db.session.add(user)
        except IntegrityError:
            db.session.rollback()
    db.session.commit()


def fake_tags():
    tags = ['python', 'c', 'c++', 'java', 'html', 'javaScript', 'css']
    for name in tags:
        tag = Tag(name=name)
        db.session.add(tag)
    db.session.commit()


def fake_questions(count=30):
    for i in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        tag = Tag.query.get(random.randint(1, Tag.query.count()))
        question = Question(title=fake.sentence(),
                            content=fake.paragraph(),
                            timestamp=fake.date_time_this_century(),
                            tag=tag,
                            user=user
                            )
        db.session.add(question)
    db.session.commit()


def fake_answers(count=100):
    for i in range(count):
        question = Question.query.get(random.randint(1, Question.query.count()))
        answer = Answer(content=fake.paragraph(nb_sentences=20),
                        timestamp=fake.date_time_this_century(),
                        question=question
                        )
        db.session.add(answer)
    db.session.commit()
