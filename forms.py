from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, DateTimeField, RadioField

class ChargerForm(FlaskForm):
    driveKmStr = IntegerField('How much do you drive daily?')
    driveKmRadio = RadioField('How much do you drive daily?',
                              choices=[('50', '0 - 50'),
                                       ('100', '51 - 100')])
    radio = RadioField('When do you stop your driving?', choices=[('18:00', '18:00'), ('19:00', '19:00')])
    radio2 = RadioField('When do you start driving?', choices=[('05:00', '05:00'), ('06:00', '06:00')])
    submit = SubmitField('Check how powerful charger I need!')