import os
import json

with open('/etc/laturel_config.json') as config_file:
        config = json.load(config_file)

class Config(object):
    #  Flask configs
    SECRET_KEY = config.get(f'SECRET_KEY') or 'debugging'
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS=1
    SERVER_NAME = 'laturel.test:3000'
    MAIL_USERNAME = os.environ.get(f'mail_username')
    MAIL_PASSWORD = os.environ.get(f'mail_password')
    MAIL_DEFAULT_SENDER = os.environ.get(f'mail_username')
    
    # Using SQLite DB for now
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/' + os.getenv('DB_NAME', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    STATIC_FOLDER = f'{os.getenv("APP_FOLDER")}/static'