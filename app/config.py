import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY','haonan')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_POST_PER_PAGE = 10
    APP_MANEGE_POST_PER_PAGE = 15
    APP_COMMENT_PER_PAGE = 15

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@localhost:3306/myblog?charset=utf8'

    DEBUG_TB_INTERCEPT_REDIRECTS = False

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@localhost:3306/myblog?charset=utf8'

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_UrL','mysql+mysqlconnector://root:123456@localhost:3306/myblog?charset=utf8')

config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig
}