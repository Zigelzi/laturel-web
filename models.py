from db import db


class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maker = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    battery = db.Column(db.Float)
    driverange = db.Column(db.Integer)
    consumption = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Cars(maker='{self.maker}', model='{self.model}', price='{self.price}', battery='{self.battery}'," \
            f"range='{self.driverange}', consumption='{self.consumption}', weight='{self.weight}')>"