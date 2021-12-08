from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, ValidationError
from askanswer.models import User, Tag


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20),
                                                   Regexp('^[a-zA-Z0-9]*$',
                                                          message='Username should only contain numbers and letters')])
    password = PasswordField('Password', validators=[DataRequired(), Length(3, 128), EqualTo('password2')])

    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_name(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Name already in use.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class QuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    content = CKEditorField('Content', validators=[DataRequired()])
    tag = SelectField('Tag', coerce=int, default=1)
    publish = SubmitField('Publish Question')

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.tag.choices = [(tag.id, tag.name)
                            for tag in Tag.query.order_by(Tag.question_num).all()]


class AnswerForm(FlaskForm):
    content = CKEditorField('Content', validators=[DataRequired()])
    publish = SubmitField('Publish Answer')


class TagForm(FlaskForm):
    name = StringField('Tag name', validators=[DataRequired(), Length(1, 128)])
    content = TextAreaField('Tag introduction', validators=[DataRequired(), Length(1, 512)])
    publish = SubmitField('Publish Tag')
