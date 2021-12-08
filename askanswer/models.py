from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from askanswer.extension import whooshee
from askanswer.extension import db


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(128))

    questions = db.relationship('Question', back_populates='user')
    answers = db.relationship('Answer', back_populates='user')
    question_num = db.Column(db.Integer, default=0)
    answer_num = db.Column(db.Integer, default=0)

    # password protection
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


association_table = db.Table('association_table',
                             db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                             db.Column('question_id', db.Integer, db.ForeignKey('question.id'))
                             )


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    content = db.Column(db.String(512))
    questions = db.relationship('Question',
                                secondary=association_table,
                                back_populates='tags')
    question_num = db.Column(db.Integer, default=0)


@whooshee.register_model('title')
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='questions')

    tags = db.relationship('Tag',
                           secondary=association_table,
                           back_populates='questions')

    answers = db.relationship('Answer', back_populates='question')
    answer_num = db.Column(db.Integer, default=0)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='answers')

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question', back_populates='answers')
