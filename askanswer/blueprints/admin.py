from flask import render_template, flash, redirect, url_for, Blueprint, jsonify, request
from flask_login import current_user, login_required
from askanswer.extension import db
from askanswer.models import User, Question, Answer, Tag
from askanswer.forms import TagForm
from askanswer.decorators import admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/user')
@login_required
@admin_required
def admin_user():
    users = User.query.order_by(User.username).all()
    return render_template('admin/admin_user.html', users=users)


@admin_bp.route('/tag/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_tag():
    form = TagForm()
    if form.validate_on_submit():
        name = form.name.data
        content = form.content.data

        tag = Tag(name=name, content=content)
        db.session.add(tag)
        db.session.commit()
        flash('Tag submit success.', ' Info')
        return redirect(url_for('home.show_tags'))
    return render_template('admin/edit_tag.html', form=form)


@admin_bp.route('/tag/<int:tag_id>/edit_name', methods=['PUT'])
@login_required
@admin_required
def edit_tag_name(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    data = request.get_json()
    if data is None or data['name'].strip() == '':
        return jsonify(message='Invalid item body.'), 400
    tag.name = data['name']
    db.session.commit()
    return jsonify(message='Tag name updated.')


@admin_bp.route('/tag/<int:tag_id>/edit_content', methods=['PUT'])
@login_required
@admin_required
def edit_tag_content(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    data = request.get_json()
    if data is None or data['content'].strip() == '':
        return jsonify(message='Invalid item body.'), 400
    tag.content = data['content']
    db.session.commit()
    return jsonify(message='Tag content updated.')


@admin_bp.route('/question/<int:question_id>/delete', methods=['DELETE'])
@login_required
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    if current_user.is_admin == False:
        return jsonify(message='Permission denied')
    for answer in question.answers:
        db.session.delete(answer)
    db.session.delete(question)
    question.user.question_num -= 1
    question.tag.question_num -= 1
    db.session.commit()
    return jsonify(message='question deleted')


@admin_bp.route('/answer/<int:answer_id>/delete', methods=['DELETE'])
@login_required
@admin_required
def delete_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if current_user.is_admin == False:
        return jsonify(message='Permission denied')
    db.session.delete(answer)
    answer.question.answer_num -= 1
    answer.user.answer_num -= 1
    db.session.commit()
    return jsonify(message='answer deleted')


@admin_bp.route('/tag/<int:tag_id>/delete', methods=['DELETE'])
@login_required
@admin_required
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    if current_user.is_admin == False:
        return jsonify(message='Permission denied')
    for question in tag.questions:
        for answer in question:
            db.session.delete(answer)
        db.session.delete(question)
    db.session.delete(tag)
    db.session.commit()
    return jsonify(message='tag deleted')


@admin_bp.route('/user/<int:user_id>/delete', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.is_admin == False:
        return jsonify(message='Permission denied')
    for question in user.questions:
        for answer in question.answers:
            db.session.delete(answer)
    for answer in user.answers:
        db.session.delete(answer)
    db.session.delete(user)
    db.session.commit()
    return jsonify(message='user deleted')
