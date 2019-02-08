from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class ChargerForm(FlaskForm):
    name = StringField('Test Name')
    submit = SubmitField('Check how powerful charger I need!')