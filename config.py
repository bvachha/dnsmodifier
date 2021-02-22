import os

basedir = os.path.abspath(os.path.dirname(__name__))


class Config(object):
    """ Contains the configuration parameters for the web application"""
    SECRET_KEY = os.environ.get('APP_SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("Please set the Application secret key value in the environment")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("Please set the DNS db path in the environment")
    API_KEY = os.environ.get('API_KEY')
    if not API_KEY:
        raise ValueError("Please set the API_KEY in the environment")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
