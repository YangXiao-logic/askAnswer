from flask import render_template, flash, redirect, url_for, Blueprint, request
from askanswer.models import Question, Answer, User, Tag

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.order_by(Question.timestamp.desc()).paginate(page, 10)
    questions = pagination.items
    questions_num = Question.query.count()

    return render_template('home/index.html', questions=questions, pagination=pagination, questions_num=questions_num)


@home_bp.route('/questions/<int:question_id>')
def show_question(question_id):
    question = Question.query.get_or_404(question_id)
    answers = Answer.query.with_parent(question).order_by(Answer.timestamp.desc()).all()
    return render_template('home/show_question.html', answers=answers, question=question)


@home_bp.route('/tags')
def show_tags():
    tags = Tag.query.order_by(Tag.question_num).all()
    return render_template('home/show_tags.html', tags=tags)


@home_bp.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.with_parent(tag).order_by(Question.timestamp.desc()).paginate(page, 10)
    questions = pagination.items

    return render_template('home/show_tag.html', questions=questions, pagination=pagination, tag=tag)


@home_bp.route('/search_question')
def search_question():
    search = request.args.get('search_question', '')
    if search == '':
        flash('Please enter some words.', 'warning')
        return url_for('home.index')
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.whooshee_search(search).order_by(Question.timestamp.desc()).paginate(page, 10)
    questions = pagination.items
    return render_template('home/index.html', questions=questions, pagination=pagination)
