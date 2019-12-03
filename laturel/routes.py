from flask import render_template, jsonify, make_response, request
from flask_mail import Message
from datetime import datetime
import sys

from laturel import app, mail
from laturel.forms import CostForm, CarSelectorForm, ContactForm
from laturel.models import model_dict, co2_dict

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    if request.method == 'POST':
        recepient = 'miika.a.savela@gmail.com' # Recepient where the contact form is sent to.
        reply_recepient = form.email.data # Where the confirmation email is sent
        # Parse the form element submitted by user and send the email.
        contact_msg = Message(subject='[Web] Uusi yhteydenottopyyntö',
                              recipients=[recepient],
                              sender=app.config['MAIL_DEFAULT_SENDER'])
        contact_msg.body = f"""Uusi yhteydenottopyyntö
                              Nimi: {form.name.data}
                              Sähköposti: {form.email.data}
                              Puhelinnumero: {form.phone.data}
                              Toivottu yhteydenottotapa: {form.preferred_contact.data}
                              Lisätietoja: {form.description.data}
                           """
        contact_msg.html = f"""<h1>Uusi yhteydenottopyyntö</h1>
                               <p><strong>Nimi</strong></p>
                               <p>{form.name.data}</p>
                               <p><strong>Sähköposti</strong></p>
                               <p>{form.email.data}</p>
                               <p><strong>Puhelinnumero</strong></p>
                               <p>{form.phone.data}</p>
                               <p><strong>Toivottu yhteydenottotapa</strong></p>
                               <p>{form.preferred_contact.data}</p>
                               <p><strong>Lisätietoja</strong></p>
                               <p>{form.description.data}</p>"""

        reply_msg = Message(subject='[Laturel] Yhteydenottopyyntö',
                            recipients=[reply_recepient])
        reply_msg.body = f"""Kiitos yhteydenotostasi!
                             
                             Olemme vastaanottaneet yhteydenottopyyntösi ja vastaamme sinulle viikon sisällä.

                             Syötit seuraavat tiedot:
                             Nimi
                             {form.name.data}
                             Sähköposti
                             {form.email.data}
                             Puhelinnumero
                             {form.phone.data}
                             Toivottu yhteydenottotapa
                             {form.preferred_contact.data}
                             Lisätietoja 
                             {form.description.data}

                             Ystävällisin terveisin
                             Laturel tiimi
                          """
        reply_msg.html = f"""<h1>Kiitos yhteydenotostasi!</h1>
                             <p>Olemme vastaanottaneet yhteydenottopyyntösi ja vastaamme sinulle viikon sisällä.</p>
                             <p>Syötit seuraavat tiedot:</p>
                             <p><strong>Nimi</strong></p>
                             <p>{ form.name.data }</p>
                             <p><strong>Sähköposti</strong></p>
                             <p>{ form.email.data }</p>
                             <p><strong>Puhelinnumero</strong></p>
                             <p>{ form.phone.data }</p>
                             <p><strong>Toivottu yhteydenottotapa</strong></p>
                             <p>{ form.preferred_contact.data }</p>
                             <p><strong>Lisätietoja</strong></p>
                             <p>{ form.description.data }</p>
                          """
        mail.send(contact_msg)
        mail.send(reply_msg)
    return render_template('web_index.html', form=form)



@app.route('/cars', methods=['GET', 'POST'])
def cars():
    form = CostForm()
    car_form = CarSelectorForm()

    return render_template('cars.html',
                           form=form,
                           car_form=car_form,
                           active='cars'
                           )

@app.route('/db/data', methods=['GET', 'POST'])
def data():
    #  Take the JSON request and convert it to dict
    req = request.get_json()

    #  Set the id values to compare and switch to correct type for DB input in model_dict
    ev = 'ecar_model'
    gasoline = 'gcar_model'
    diesel = 'dcar_model'

    #  Replace the id value for type value to be able to do DB query correctly
    if req['type'] == ev:
        req['type'] = 'ev'
    if req['type'] == gasoline:
        req['type'] = 'gasoline'
    if req['type'] == diesel:
        req['type'] = 'diesel'

    #  Query DB for car values and make dict of values
    model = model_dict(req['type'], req['model'])
    co2 = co2_dict(model['co2'])

    #  Create JSON response from dict and respond it to application
    res = make_response(jsonify(car_info=model, co2=co2), 200)
    return res


@app.route('/e/contact_card')
def web_contact_card():
    return render_template('example_contactcard.html')