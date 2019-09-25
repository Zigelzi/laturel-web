from flask import render_template, jsonify, make_response, request
from flask_mail import Message
from datetime import datetime

from laturel import app, mail
from laturel.forms import CostForm, CarSelectorForm, ContactForm
from laturel.models import model_dict, co2_dict


@app.route('/')
def index():
    return render_template('index.html', active='index')

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


@app.route('/web', methods=['GET', 'POST'])
def web_index():
    form = ContactForm()
    if request.method == 'POST':
        # Parse the form element submitted by user and send the email.
        msg = Message(subject='[Web] Uusi yhteydenottopyyntö',
                      recipients=['miika.a.savela@gmail.com'])
        msg.body = 'This is a test body for plain text message'
        msg.html = f"""<h1>Uusi yhteydenottopyyntö</h1>
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
        mail.send(msg)
    return render_template('web/web_index.html', form=form)