from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField, RadioField, FloatField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email

from laturel.models import get_cars

class ValidatedFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('No a valid float value'))


class CarSelectorForm(FlaskForm):
    ecars, gcars, dcars = get_cars()
    ecar_model = SelectField('Select electric vehicle', choices=ecars)
    gcar_model = SelectField('Select gasoline vehicle', choices=gcars)
    dcar_model = SelectField('Select diesel vehicle', choices=dcars)


class CostForm(FlaskForm):
    ecar_price = FloatField('Car purchase price', default=40000)
    ecar_depr = FloatField('Yearly depreciation rate', default=17.5)
    ecar_subsidy = FloatField('Available subsidy for EV:s', default=2000)
    ecar_consumption = FloatField('Car consumption', default=15.1)
    ecar_eprice = FloatField('Electricity price', default=0.14)
    ecar_weight = IntegerField('Car weight (approx.)', default=2100) # Car driving power tax.
    ecar_charger = RadioField('Do you have EV charger already?',
                           choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes')
    ecar_co2 = IntegerField('Car tax per year', default=106)  # Vehicle tax in €/year

    gcar_price = FloatField('Car purchase price', default=32000)
    gcar_depr = FloatField('Yearly depreciation rate', default=15.5)
    gcar_consumption = FloatField('Car consumption', default=6)
    gcar_gprice = FloatField('Gas price', default=1.43)
    gcar_co2 = IntegerField('Car tax per year', default=210)  # Vehicle tax in €/year

    dcar_price = FloatField('Car purchase price', default=32000)
    dcar_depr = FloatField('Yearly depreciation rate', default=15.5)
    dcar_consumption = FloatField('Car consumption', default=5.5)
    dcar_dprice = FloatField('Diesel price', default=1.4)
    dcar_weight = FloatField('Car weight (approx.)', default=1800)  # Car driving power tax.
    dcar_co2 = IntegerField('Car tax per year', default=196)  # Vehicle tax in €/year

    drivekm = FloatField('How much you drive yearly?', default=30000)
    owntime = IntegerField('How long will you own the car?', default=5)
    submit = SubmitField('Compare cars')


class ContactForm(FlaskForm):
    # Contact form for Laturel Web section
    name = StringField('Nimi', validators=[DataRequired(message='Pakollinen kenttä')])
    email = StringField('Sähköposti', validators=[Email(message='Syötä sähköpostiosoite')])
    phone = StringField('Puhelinnumero')
    description = TextAreaField('Lisätiedot')
    preferred_contact = RadioField('Haluan yhteydenoton mieluiten',
                                    validators=[DataRequired(message='Valitse yksi vaihtoehdoista')],
                                    choices=[('email', 'Sähköpostilla'),
                                             ('phone', 'Puhelimitse')],
                                    default='email')
    submit = SubmitField('Lähetä')