import os

class Config(object):

    #  Environment variables

    #  Flask configs
    SECRET_KEY = os.environ.get(f'secret') or 'debugging'
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS=1
    MAIL_USERNAME = os.environ.get(f'mail_username')
    MAIL_PASSWORD = os.environ.get(f'mail_password')
    MAIL_DEFAULT_SENDER = os.environ.get(f'mail_username')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SERVER_NAME = 'laturel.fi:5000'