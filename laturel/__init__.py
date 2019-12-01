import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

from laturel.config import Config, DevConfig

app = Flask(__name__)
if os.getenv['FLASK_ENV'] == 'development':
    app.config.from_object(DevConfig)
else:
    app.config.from_object(Config)
db = SQLAlchemy(app)
mail = Mail(app)

from laturel import routes