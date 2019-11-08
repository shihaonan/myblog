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
    login_manager.init_app(app)

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

def register_commands(app):
    @app.cli.command()
    @click.option('--username', prompt=True)
    @click.option('--password', prompt=True, confirmation_prompt=True)
    def init(username,password):
        click.echo('正在初始化数据库……')
        db.create_all()

        admin = Admin.query.first()
        if admin:
            click.echo('管理员已经存在了，修改中……')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('创建新的管理员账户……')
            admin = Admin(username = username)
            admin.set_password(password)
            db.session.add(admin)

        bloginfo = Bloginfo.query.first()
        if bloginfo is None:
            click.echo('创建默认博客信息……')
            bloginfo = Bloginfo(
                blog_title='默认标题',
                blog_sub_title="这是默认子标题",
                name='浩楠',
                about='Anything about you.'
            )
            db.session.add(bloginfo)

        category = Category.query.first()
        if category is None:
            click.echo('创建默认分类……')
            category = Category(name='默认')
            db.session.add(category)

        db.session.commit()
        click.echo('初始化完成！')