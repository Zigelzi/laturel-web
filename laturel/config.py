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
    MAIL_USERNAME = config.get(f'MAIL_USERNAME')
    MAIL_PASSWORD = config.get(f'MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = config.get(f'MAIL_USERNAME')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SERVER_NAME = 'laturel.fi:5000'