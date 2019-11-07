import os
from flask import Flask,render_template, request
from app.config import config

from app.blueprints.auth import auth_bp
from app.blueprints.admin import admin_bp
from app.blueprints.blog import blog_bp
from app.extentions import *
from flask_migrate import Migrate
from app.models import *
from app.commands import *


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG','development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extentions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)

    return app

def register_logging(app):
    pass

def register_extentions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    migrate = Migrate(app,db)
    toolbar.init_app(app)

def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

def register_shell_context(app):
    pass

def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        bloginfo = Bloginfo.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin,bloginfo=bloginfo,categories=categories)

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

# def register_commands(app):
#     pass