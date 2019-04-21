import os

class Config(object):

    #  Environment variables

    #  Flask configs
    SECRET_KEY = os.environ.get(f'secret') or 'debugging'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'