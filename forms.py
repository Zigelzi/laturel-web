from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, DateTimeField, RadioField

class ChargerForm(FlaskForm):
    driveKmRadio = RadioField('How much do you drive daily?',
                              choices=[('50', '0 - 50 km'),
                                       ('100', '51 - 100 km')])
    stopTime = RadioField('When do you stop your driving?', choices=[('18:00', '18:00'), ('19:00', '19:00')])
    startTime = RadioField('When do you start driving?', choices=[('05:00', '05:00'), ('06:00', '06:00')])
    submit = SubmitField('Check how powerful charger I need!')

class CarSelectorForm(FlaskForm):
    carmodel = RadioField('Select car model to use as template:',
                          choices=[('Hyundai Kona', 'Hyundai Kona'),
                                   ('Kia Niro', 'Kia Niro')])

class eForm(FlaskForm):
    econsumption = IntegerField('Electric vehicle energy consumption:')
    eprice = IntegerField('Electricity price (incl. transmission):')
    edrivingpower = IntegerField('Car weight (approx.):') # Car driving power tax.
    etax = IntegerField('Car tax:') # Vehicle tax
    echarger = RadioField('Do you have EV charger already?',
                           choices=[('Yes', 'Yes'), ('No', 'No')])

class gForm(FlaskForm):
    gconsumption = IntegerField('Gasoline car consumption:')
    gprice = IntegerField('Gas price:')
    gtax = IntegerField('Car tax:')

class dForm(FlaskForm):
    dconsumption = IntegerField('Gasoline car consumption:')
    dprice = IntegerField('Gas price:')
    ddrivingpower = IntegerField('Car weight (approx.):') # Car driving power tax.
    dtax = IntegerField('Car tax:') # Vehicle tax

class driveForm(FlaskForm):
    drivekm = IntegerField('How much you drive yearly?')
