import os
# import json

#with open('/etc/laturel_config.json') as config_file:
        #config = json.load(config_file)

class Config(object):
    #  Flask configs
    SECRET_KEY = os.getenv(f'SECRET_KEY', 'debugging')
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS=1
    SERVER_NAME = 'laturel.test'
    MAIL_USERNAME = os.getenv(f'MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv(f'MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv(f'MAIL_USERNAME')
    
    # Using SQLite DB for now
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/' + os.getenv('DB_NAME', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    STATIC_FOLDER = f'{os.getenv("APP_FOLDER")}/static'