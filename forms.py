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
    ecarprice = FloatField('Car purchase price:', default=40000)
    edepr = FloatField('Yearly deprecation rate:', default=17.5)
    esubsidy = FloatField('Available subsidy for EV:s', default=2000)
    econsumption = FloatField('Car consumption:', default=15.1)
    eprice = FloatField('Electricity price (incl. transmission):', default=0.14)
    eweight = IntegerField('Car weight (approx.):', default=2100) # Car driving power tax.
    etax = FloatField('Car tax:', default=53) # Vehicle tax
    echarger = RadioField('Do you have EV charger already?',
                           choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes')

class gForm(FlaskForm):
    gcarprice = FloatField('Car purchase price:', default=32000)
    gdepr = FloatField('Yearly deprecation rate:', default=15.5)
    gconsumption = FloatField('Car consumption:', default=7.7)
    gprice = FloatField('Gas price:', default=1.43)
    gtax = FloatField('Car tax:', default=230)

class dForm(FlaskForm):
    dcarprice = FloatField('Car purchase price:', default=32000)
    ddepr = FloatField('Yearly deprecation rate:', default=15.5)
    dconsumption = FloatField('Car consumption:', default=5.5)
    dprice = FloatField('Diesel price:', default=1.4)
    dweight = FloatField('Car weight (approx.):', default=1800) # Car driving power tax.
    dtax = FloatField('Car tax:', default=143) # Vehicle tax

class driveForm(FlaskForm):
    drivekm = FloatField('How much you drive yearly?', default=30000)
    owntime = IntegerField('How long will you own the car?',default=5)
    submit = SubmitField('Compare cars')
