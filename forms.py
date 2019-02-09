from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, RadioField

class ChargerForm(FlaskForm):
    name = StringField('Test Name')
    date1 = DateTimeField('When do you stop your driging?', format='%H:%M')
    date2 = DateTimeField('When do you start driving?', format='%H:%M')
    radio = RadioField('Test radio')
    submit = SubmitField('Check how powerful charger I need!')