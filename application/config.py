import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base Config"""

    # MONGODB_DB = os.environ['MONGODB_SETTINGS']
    # MONGODB_ALIAS = os.environ['MONGODB_ALIAS']
    # MONGODB_HOST = os.environ['MONGODB_HOST']
    # MONGODB_PORT = os.environ['MONGODB_PORT']
    # MONGODB_USERNAME = os.environ['MONGODB_USERNAME']
    # MONGODB_PASSWORD = os.environ['MONGODB_PASSWORD']
    
    # Mongodb connection dict
    MONGODB_SETTINGS = os.environ['MONGODB_SETTINGS']

    # Flask-user settings

    USER_ENABLE_EMAIL = eval(os.environ['USER_ENABLE_EMAIL'])
    USER_APP_NAME = os.environ['USER_APP_NAME']
    USER_ENABLE_CHANGE_USERNAME = eval(os.environ['USER_ENABLE_CHANGE_USERNAME'])
    USER_REQUIRE_RETYPE_PASSWORD = eval(os.environ['USER_REQUIRE_RETYPE_PASSWORD'])
    USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL = eval(os.environ['USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL'])


class ProductionConfig(Config):
    """Production Config"""


class DevelopmentConfig(Config):
    """Dev Config"""


class TestingConfig(Config):
    """Testing Config"""

    TESTING = True
    # WTF_CSRF_ENABLED = False
    # CSRF_ENABLED = False
