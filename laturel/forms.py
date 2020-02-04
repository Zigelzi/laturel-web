from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (IntegerField, SubmitField, SelectField, 
                    RadioField, FloatField, StringField,
                    TextAreaField)
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
    ecar_model = SelectField('Valitse täyssähköauto', choices=ecars)
    gcar_model = SelectField('Valitse bensiiniauto', choices=gcars)
    dcar_model = SelectField('Valitse dieselauto', choices=dcars)


class CostForm(FlaskForm):
    ecar_price = FloatField('Auton ostohinta', default=40000)
    ecar_depr = FloatField('Vuosittainen arvonalenema', default=17.5)
    ecar_subsidy = FloatField('Saatavilla oleva tuki auton hankintaan', default=2000)
    ecar_consumption = FloatField('Auton kulutus', default=15.1)
    ecar_eprice = FloatField('Sähkön hinta', default=0.14)
    ecar_weight = IntegerField('Auton kokonaispaino (arvio)', default=2100) # Car driving power tax.
    ecar_charger = RadioField('Onko sinulla kotilatausasema?',
                           choices=[('Yes', 'Kyllä'), ('No', 'Ei')], default='Yes')
    ecar_co2 = IntegerField('Vuosittainen ajoneuvovero', default=106)  # Vehicle tax in €/year

    gcar_price = FloatField('Auton ostohinta', default=32000)
    gcar_depr = FloatField('Vuosittainen arvonalenema', default=15.5)
    gcar_consumption = FloatField('Auton kulutus', default=6)
    gcar_gprice = FloatField('Bensiinin price', default=1.43)
    gcar_co2 = IntegerField('Vuosittainen ajoneuvovero', default=210)  # Vehicle tax in €/year

    dcar_price = FloatField('Auton ostohinta', default=32000)
    dcar_depr = FloatField('Vuosittainen arvonalenema', default=15.5)
    dcar_consumption = FloatField('Auton kulutus', default=5.5)
    dcar_dprice = FloatField('Dieselin hinta', default=1.4)
    dcar_weight = FloatField('Auton kokonaispaino (arvio)', default=1800)  # Car driving power tax.
    dcar_co2 = IntegerField('Vuosittainen ajoneuvovero', default=196)  # Vehicle tax in €/year

    drivekm = FloatField('Kuinka paljon ajat vuodessa?', default=30000)
    owntime = IntegerField('Kuinka kauan ajattelit omistaa auton?', default=5)
    submit = SubmitField('Vertaile kustannuksia')


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
    recaptcha = RecaptchaField()
    submit = SubmitField('Lähetä')