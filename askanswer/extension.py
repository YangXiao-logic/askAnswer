from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_whooshee import Whooshee

db = SQLAlchemy()
login_manager = LoginManager()
moment = Moment()
csrf = CSRFProtect()
migrate = Migrate()
bootstrap = Bootstrap()
ckeditor = CKEditor()
whooshee = Whooshee()


@login_manager.user_loader
def load_user(user_id):
    from askanswer.models import User
    user = User.query.get(int(user_id))
    return user
