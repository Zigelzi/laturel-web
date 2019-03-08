from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from laturel.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


from laturel import routes
