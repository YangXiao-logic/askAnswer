import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, request
from flask_login import current_user

from askanswer.extension import db, login_manager, moment, csrf, migrate, bootstrap
from askanswer.setting import config
from askanswer.blueprints.auth import auth_bp
from askanswer.blueprints.home import home_bp
from askanswer.blueprints.ask import ask_bp
import click

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('askanswer')
    app.config.from_object(config[config_name])
    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_command(app)
    return app


def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/askanswer.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)


def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(ask_bp, url_prefix='/ask')



def register_command(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--user', default=5, help='Quantity of users, default is 5.')
    @click.option('--question', default=30, help='Quantity of questions, default is 30.')
    @click.option('--answer', default=100, help='Quantity of answers, default is 100.')
    def forge(user, question, answer):
        from askanswer.fakes import fake_users, fake_questions, fake_answers, fake_tags
        """Generate fake data."""
        db.drop_all()
        db.create_all()

        click.echo('Generating %d users...' % user)
        fake_users(user)

        click.echo('Generating tags..')
        fake_tags()

        click.echo('Generating %d questions...' % question)
        fake_questions(question)

        click.echo('Generating %d answers...' % answer)
        fake_answers(answer)
