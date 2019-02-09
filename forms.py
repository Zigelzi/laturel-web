from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField

class ChargerForm(FlaskForm):
    name = StringField('Test Name')
    date1 = DateTimeField('Departure time', format='%Y-%m')
    submit = SubmitField('Check how powerful charger I need!')