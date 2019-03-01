from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,  String, Float

Base = declarative_base()

class Cars(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    maker = Column(String)
    model = Column(String)
    price = Column(Integer)
    battery = Column(Float)
    driverange = Column(Integer)
    consumption = Column(Float)
    weight = Column(Integer)

    def __repr__(self):
        return f"<Cars(title='{maker}', model='{model}', price='{price}', battery='{battery}'," \
            f"range='{driverange}', consumption='{consumption}', weight='{weight}')>"