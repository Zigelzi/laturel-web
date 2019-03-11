from flask import render_template, jsonify, make_response, request
from datetime import datetime
from laturel import app
from laturel.forms import CostForm, ChargerForm, CarSelectorForm
from laturel.models import model_dict


@app.route('/')
def index():
    return render_template('index.html', active='index')


@app.route('/chargers', methods=['POST', 'GET'])
def chargers():
    form = ChargerForm()
    driveKm = int(form.driveKmRadio.data)
    stopTime = form.stopTime.data
    startTime = form.startTime.data
    if stopTime and startTime is not None:
        stopTime = datetime.strptime(stopTime, '%H:%M')
        startTime = datetime.strptime(startTime, '%H:%M')
        chargingTime = stopTime - startTime

    return render_template('chargers.html',
                           form=form,
                           driveKm=driveKm,
                           stopTime=stopTime,
                           startTime=startTime,
                           chargingTime=chargingTime,
                           active='chargers')


@app.route('/evbasics')
def evbasics():
    return render_template('evbasics.html', active='evbasics')


@app.route('/cars', methods=['GET', 'POST'])
def cars():
    form = CostForm()
    car_form = CarSelectorForm()

    return render_template('cars.html',
                           form=form,
                           car_form=car_form,
                           active='cars'
                           )


@app.route('/about')
def about():
    return render_template('about.html', active='about')


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

    #  Create JSON response from dict and respond it to application
    res = make_response(jsonify(model), 200)
    return res