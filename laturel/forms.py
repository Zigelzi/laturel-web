from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField, RadioField, FloatField
from laturel.models import get_cars

class ValidatedFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('No a valid float value'))


class ChargerForm(FlaskForm):
    driveKmRadio = RadioField('How much do you drive daily?',
                              choices=[('50', '0 - 50 km'),
                                       ('100', '51 - 100 km')], default='50')
    stopTime = RadioField('When do you stop your driving?', choices=[('18:00', '18:00'), ('19:00', '19:00')], default='18:00')
    startTime = RadioField('When do you start driving?', choices=[('05:00', '05:00'), ('06:00', '06:00')], default='05:00')
    submit = SubmitField('Check how powerful charger I need!')


class CarSelectorForm(FlaskForm):
    ecars, gcars, dcars = get_cars()
    ecar_model = SelectField('Select electric vehicle', choices=ecars)
    gcar_model = SelectField('Select gasoline vehicle', choices=gcars)
    dcar_model = SelectField('Select diesel vehicle', choices=dcars)


class CostForm(FlaskForm):
    ecarprice = ValidatedFloatField('Car purchase price', default=40000)
    edepr = ValidatedFloatField('Yearly depreciation rate', default=17.5)
    esubsidy = ValidatedFloatField('Available subsidy for EV:s', default=2000)
    econsumption = ValidatedFloatField('Car consumption', default=15.1)
    eprice = ValidatedFloatField('Electricity price', default=0.14)
    eweight = IntegerField('Car weight (approx.)', default=2100) # Car driving power tax.
    etax = ValidatedFloatField('Car tax:', default=53) # Vehicle tax
    echarger = RadioField('Do you have EV charger already?',
                           choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes')
    gcarprice = ValidatedFloatField('Car purchase price', default=32000)
    gdepr = ValidatedFloatField('Yearly depreciation rate', default=15.5)
    gconsumption = ValidatedFloatField('Car consumption', default=6)
    gprice = ValidatedFloatField('Gas price', default=1.43)
    gtax = ValidatedFloatField('Car tax', default=230)
    dcarprice = ValidatedFloatField('Car purchase price', default=32000)
    ddepr = ValidatedFloatField('Yearly depreciation rate', default=15.5)
    dconsumption = ValidatedFloatField('Car consumption', default=5.5)
    dprice = ValidatedFloatField('Diesel price', default=1.4)
    dweight = ValidatedFloatField('Car weight (approx.)', default=1800)  # Car driving power tax.
    dtax = ValidatedFloatField('Car tax', default=143)  # Vehicle tax
    drivekm = ValidatedFloatField('How much you drive yearly?', default=30000)
    owntime = IntegerField('How long will you own the car?', default=5)
    submit = SubmitField('Compare cars')
