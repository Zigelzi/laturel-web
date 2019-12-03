import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

from laturel.config import Config, DevConfig, StageConfig

app = Flask(__name__)
if os.getenv('FLASK_ENV') == 'development':
    app.config.from_object(DevConfig)
elif os.getenv('FLASK_ENV') == 'stage':
    app.config.from_object(StageConfig)
else:
    app.config.from_object(Config)
db = SQLAlchemy(app)
mail = Mail(app)

from laturel import routes