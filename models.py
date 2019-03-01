from flask_sqlalchemy import SQLAlchemy
from db import db

class Cars(db.model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    maker = db.Column(db.String, nullable=False)
    model = db.Column(db., nullable=False)
    price = db.Column(db.Integer, nullable=False)
    battery = db.Column(db.Float)
    driverange = db.Column(db.Integer)
    consumption = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Cars(title='{maker}', model='{model}', price='{price}', battery='{battery}'," \
            f"range='{driverange}', consumption='{consumption}', weight='{weight}')>"