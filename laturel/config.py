import os

class Config(object):
    # Production config that is loaded as default
    SECRET_KEY = os.getenv(f'SECRET_KEY', 'debugging')
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS=1
    SERVER_NAME = f'laturel.fi:{os.getenv("APP_PORT")}'
    MAIL_USERNAME = os.getenv(f'MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv(f'MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv(f'MAIL_USERNAME')
    STATIC_FOLDER = f'{os.getenv("APP_FOLDER")}/laturel/static'
    
    # Using SQLite DB for now
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/' + os.getenv('DB_NAME', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

class DevConfig(Config):
    # Development config 
    DEBUG = True
    SERVER_NAME = f'laturel.test:{os.getenv("APP_PORT")}'

class StageConfig(Config):
    # Stage config to replicate production locally
    DEBUG = False
    SERVER_NAME = f'laturel.stage:{os.getenv("APP_PORT")}'