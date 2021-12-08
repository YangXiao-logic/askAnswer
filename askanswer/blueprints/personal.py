from flask import flash, redirect, url_for, render_template, Blueprint, request, current_app
from flask_login import login_required, current_user
from askanswer.forms import QuestionForm, AnswerForm
from askanswer.models import Question, Tag, User, Answer
from askanswer.extension import db

personal_bp = Blueprint('personal', __name__)


@personal_bp.route('/edit_question', methods=['GET', 'POST'])
def edit_question():
    if not current_user.is_authenticated:
        flash('Please Ask Question after Login', 'warning')
        current_app.logger.warning('Please Ask Question after Login')
        return redirect(url_for('auth.login'))
    form = QuestionForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        tag1 = Tag.query.get(form.tag.data)
        tag2 = Tag.query.get(form.tag2.data)
        if tag1 == tag2:
            flash("Tag1 can not equal to tag2", 'warning')
            current_app.logger.warning('Tag1 can not equal to tag2')
            return redirect(url_for('personal.edit_question'))
        question = Question(title=title, content=content, user=current_user)
        question.tags.append(tag1)
        question.tags.append(tag2)
        tag1.question_num += 1
        tag2.question_num += 1
        current_user.question_num += 1
        db.session.add(question)
        db.session.commit()
        flash('Ask question success', ' Info')
        current_app.logger.info('Ask question success')
        return redirect(url_for('home.index'))
    return render_template('personal/edit_question.html', form=form)


@personal_bp.route('/edit_answer/<int:question_id>', methods=['GET', 'POST'])
def edit_answer(question_id):
    if not current_user.is_authenticated:
        flash('Please Answer Question after Login', 'warning')
        current_app.logger.warning('Please Answer Question after Login')
        return redirect(url_for('auth.login'))
    form = AnswerForm()
    if form.validate_on_submit():
        content = form.content.data
        question = Question.query.get_or_404(question_id)
        answer = Answer(content=content, question=question, user=current_user)
        question.answer_num += 1
        current_user.answer_num += 1
        db.session.add(answer)
        db.session.commit()
        flash('Answer submit success', ' Info')
        current_app.logger.info('Answer submit success')
        return redirect(url_for('home.show_question', question_id=question_id))
    return render_template('personal/edit_answer.html', form=form)


@personal_bp.route('/show_personal_question/<int:user_id>')
def show_personal_question(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    question_filter = request.args.get('filter', default='newest', type=str)
    pagination = Question.query.with_parent(user).order_by(Question.timestamp.desc()).paginate(page, 10)
    if question_filter == 'newest':
        pagination = Question.query.with_parent(user).order_by(Question.timestamp.desc()).paginate(page, 10)
    elif question_filter == 'active':
        pagination = Question.query.with_parent(user).order_by(Question.answer_num.desc()).paginate(page, 10)
    questions = pagination.items
    return render_template('personal/show_personal_question.html', questions=questions, pagination=pagination,
                           user=user)


@personal_bp.route('/show_mine_question')
@login_required
def show_mine_question():
    page = request.args.get('page', 1, type=int)
    question_filter = request.args.get('filter', default='newest', type=str)
    pagination = Question.query.with_parent(current_user).order_by(Question.timestamp.desc()).paginate(page, 10)
    if question_filter == 'newest':
        pagination = Question.query.with_parent(current_user).order_by(Question.timestamp.desc()).paginate(page, 10)
    elif question_filter == 'active':
        pagination = Question.query.with_parent(current_user).order_by(Question.answer_num.desc()).paginate(page, 10)
    questions = pagination.items
    return render_template('personal/show_mine_question.html', questions=questions, pagination=pagination,
                           user=current_user)
