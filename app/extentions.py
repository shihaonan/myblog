from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
ckeditor = CKEditor()
toolbar = DebugToolbarExtension()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from app.models import Admin
    return Admin.query.get(int(user_id))


login_manager.login_view = 'auth.login'

