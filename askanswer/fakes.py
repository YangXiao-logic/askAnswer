from faker import Faker
import random
from sqlalchemy.exc import IntegrityError

from askanswer.extension import db
from askanswer.models import User, Tag, Question, Answer

fake = Faker()


def fake_users(count=15):
    for i in range(count):
        user = User(username=fake.name())
        user.set_password('123456')
        try:
            db.session.add(user)
        except IntegrityError:
            db.session.rollback()
    user = User(username='admin', is_admin=True)
    user.set_password('admin')
    db.session.add(user)
    db.session.commit()


def fake_tags():
    tags = ['python', 'c', 'c++', 'java', 'html', 'javaScript', 'css']
    for name in tags:
        tag = Tag(name=name, content=fake.paragraph())
        db.session.add(tag)
    db.session.commit()


def fake_questions(count=100):
    for i in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        tag1 = Tag.query.get(random.randint(1, Tag.query.count()))
        tag2 = Tag.query.get(random.randint(1, Tag.query.count()))
        if tag1 != tag2:
            question = Question(title=fake.sentence(),
                                content=fake.paragraph(),
                                timestamp=fake.date_time_this_century(),
                                user=user
                                )
            question.tags.append(tag1)
            tag1.question_num += 1
            question.tags.append(tag2)
            tag2.question_num += 1
            user.question_num += 1
            db.session.add(question)
    db.session.commit()


def fake_answers(count=300):
    for i in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        question = Question.query.get(random.randint(1, Question.query.count()))
        answer = Answer(content=fake.paragraph(nb_sentences=20),
                        timestamp=fake.date_time_this_century(),
                        question=question,
                        user=user
                        )
        user.answer_num += 1
        question.answer_num += 1
        db.session.add(answer)
    db.session.commit()
