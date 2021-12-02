from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
login_manager = LoginManager()
moment = Moment()
csrf = CSRFProtect()
migrate = Migrate()
bootstrap = Bootstrap()


@login_manager.user_loader
def load_user(user_id):
    from askanswer.models import User
    user = User.query.get(int(user_id))
    return user
