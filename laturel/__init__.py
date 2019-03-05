from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from laturel.forms import ChargerForm, Form
from laturel.config import Config
from laturel.helpers import round_hundreds, depr_oper

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from laturel import routes