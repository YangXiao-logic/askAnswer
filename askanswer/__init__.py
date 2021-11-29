import os
from flask import Flask

from askanswer.extension import db, login_manager, moment, csrf, migrate
from askanswer.setting import config
from askanswer.blueprints.auth import auth_bp
from askanswer.blueprints.home import home_bp
from askanswer.blueprints.ask import ask_bp
import click


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('askAnswer')
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    register_command(app)
    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)


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

    # @app.cli.command()
    # @click.option('--user', default=5, help='Quantity of categories, default is 5.')
    # @click.option('--category', default=30, help='Quantity of posts, default is 30.')
    # @click.option('--task', default=100, help='Quantity of comments, default is 100.')
    # @click.option('--comment', default=50, help='Quantity of comments, default is 50.')
    # def forge(user, category, task, comment):
    #     """Generate fake data."""
