from flask import flash, redirect, url_for, render_template, Blueprint, jsonify, request
from flask_login import login_required, current_user

ask_bp = Blueprint('ask', __name__)


@ask_bp.route('/ask')
def ask():
    return render_template('edit/ask.html')


@ask_bp.route('/answer')
def answer():
    return render_template('')
