from flask import flash, redirect, url_for, render_template, Blueprint, jsonify, request
from flask_login import login_required, current_user
from askanswer.forms import QuestionForm
from askanswer.models import Question, Tag, User
from askanswer.extension import db

personal_bp = Blueprint('personal', __name__)


@personal_bp.route('/edit_question')
@login_required
def edit_question():
    form = QuestionForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        tag = Tag.query.get(form.tag.data)
        question = Question(title=title, content=content, user=current_user, tag=tag)
        tag.question_num += 1
        db.session.add(question)
        db.session.commit()
    return render_template('personal/edit_question.html', form=form)


@personal_bp.route('/edit_answer')
def edit_answer():
    return render_template('')


@personal_bp.route('/show_personal_question/<int:user_id>')
def show_personal_question(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.with_parent(user).order_by(Question.timestamp.desc()).paginate(page, 10)
    questions = pagination.items
    return render_template('personal/show_personal_question.html', questions=questions, pagination=pagination,
                           user=user)


@personal_bp.route('/show_mine_question')
@login_required
def show_mine_question():
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.with_parent(current_user).order_by(Question.timestamp.desc()).paginate(page, 10)
    questions = pagination.items
    return render_template('personal/show_mine_question.html', questions=questions, pagination=pagination,
                           user=current_user)
