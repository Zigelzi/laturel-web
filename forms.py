from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, DateTimeField, RadioField, FloatField

class ChargerForm(FlaskForm):
    driveKmRadio = RadioField('How much do you drive daily?',
                              choices=[('50', '0 - 50 km'),
                                       ('100', '51 - 100 km')], default='50')
    stopTime = RadioField('When do you stop your driving?', choices=[('18:00', '18:00'), ('19:00', '19:00')], default='18:00')
    startTime = RadioField('When do you start driving?', choices=[('05:00', '05:00'), ('06:00', '06:00')], default='05:00')
    submit = SubmitField('Check how powerful charger I need!')

class CarSelectorForm(FlaskForm):
    carmodel = RadioField('Select car model to use as template:',
                          choices=[('Hyundai Kona', 'Hyundai Kona'),
                                   ('Kia Niro', 'Kia Niro')])

class eForm(FlaskForm):
    econsumption = FloatField('Electric vehicle energy consumption:')
    eprice = FloatField('Electricity price (incl. transmission):')
    eweight = IntegerField('Car weight (approx.):') # Car driving power tax.
    etax = FloatField('Car tax:') # Vehicle tax
    echarger = RadioField('Do you have EV charger already?',
                           choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes')

class gForm(FlaskForm):
    gconsumption = FloatField('Gasoline car consumption:')
    gprice = FloatField('Gas price:')
    gtax = FloatField('Car tax:')

class dForm(FlaskForm):
    dconsumption = FloatField('Diesel car consumption:')
    dprice = FloatField('Diesel price:')
    dweight = IntegerField('Car weight (approx.):') # Car driving power tax.
    dtax = FloatField('Car tax:') # Vehicle tax

class driveForm(FlaskForm):
    drivekm = IntegerField('How much you drive yearly?')
    submit = SubmitField('Compare cars')