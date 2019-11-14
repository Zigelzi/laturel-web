from flask.cli import FlaskGroup

from laturel import app, db
from laturel.models import Cars

cli = FlaskGroup(app)

@cli.command('create_db')
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('seed_db')
def seed_db():
    ev = Cars(type='ev', maker='audi', model='e-tron', body_type='suv', price=87023, battery=83.6, driverange=375, consumption=22.6, weight=2565,fullmodel='e-tron 55 quattro 265 kw',co2=0.0)
    gasoline = Cars(type='gasoline', maker='bmw', model='330i', body_type='sedan', price=49249, battery=None, driverange=None, consumption=6.8, weight=2060,fullmodel='330i sedan',co2=154.0)
    diesel = Cars(type='diesel', maker='bmw', model='320d', body_type='sedan', price=43088, battery=None, driverange=None, consumption=6.1, weight=2085,fullmodel='320d sedan',co2=138.0)
    db.session.add(ev)
    db.session.add(gasoline)
    db.session.add(diesel)
    db.session.commit()

if __name__ == "__main__":
    cli()
