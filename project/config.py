import os

BASE_DIR = os.path.abspath(os.path.dirname(__name__))

class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '59af93ea593df66e9878818c08ac69e5fb5d77efe0943492'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True

class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + '/tmp/test.db'
