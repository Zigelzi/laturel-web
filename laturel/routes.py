from flask import render_template, jsonify, make_response, request
from datetime import datetime
from laturel import app
from laturel.forms import CostForm, ChargerForm, CarSelectorForm
from laturel.helpers import depr_oper, round_hundreds
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

    edeprcalc = 0
    gdeprcalc = 0
    ddeprcalc = 0

    eyearly = 0
    gyearly = 0
    dyearly = 0

    etotal = 0
    gtotal = 0
    dtotal = 0

    edepr_yearly = 0
    edepr_owntime = 0
    ecost_list = 0
    eoper = 0
    eafter = 0
    gdepr_yearly = 0
    gdepr_owntime = 0
    gcost_list = 0
    goper = 0
    gafter = 0
    ddepr_yearly = 0
    ddepr_owntime = 0
    dcost_list = 0
    doper = 0
    dafter = 0

    # EV data from EV form
    ecarprice = form.ecar_price.data
    edepr = form.ecar_depr.data
    esubsidy = form.ecar_subsidy.data
    econsumption = form.ecar_consumption.data
    eprice = form.ecar_eprice.data
    eweight = form.ecar_weight.data
    edrivingpower = round_hundreds(eweight)  # Round to starting hundreds and multiply by 0.055 (€)
    etax = form.ecar_tax.data
    echarger = form.ecar_charger.data
    chargerprice = 800

    # Gasoline car data from gasoline form
    gcarprice = form.gcar_price.data
    gdepr = form.gcar_depr.data
    gconsumption = form.gcar_consumption.data
    gprice = form.gcar_gprice.data
    gtax = form.gcar_tax.data

    # Diesel car data from diesel form
    dcarprice = form.dcar_price.data
    ddepr = form.dcar_depr.data
    dconsumption = form.dcar_consumption.data
    dprice = form.dcar_dprice.data
    dweight = form.dcar_weight.data
    ddrivingpower = round_hundreds(dweight)  # Round to starting hundreds and multiply by 0.055 (€)
    dtax = form.dcar_tax.data

    drivekm = form.drivekm.data
    owntime = form.owntime.data

    error = None

    try:
        # Calculating the driving power tax based on car weight.
        edrivingpower = edrivingpower * 0.015 * 365 # EV 0.015€/starting 100 kg
        ddrivingpower = ddrivingpower * 0.055 * 365 # Diesel 0.055€/starting 100 kg

        # EV price calculation
        eyearly = int(
            drivekm * eprice * (econsumption / 100) + etax + edrivingpower)  # int for rounding to full numbers
        if esubsidy != 0:
            ecarprice = ecarprice - esubsidy

        #  Use function to take deprecation values, yearly deprecation and yearly
        #  operating costs and assign them to variables.
        edepr_total, edepr_yearly, ecost_list = depr_oper(ecarprice, edepr, owntime, eyearly)

        # Take the index of the lists and calculate total
        edepr_owntime = int(edepr_total[owntime - 1])
        etotal = int(ecost_list[owntime - 1] + edepr_total[owntime - 1])
        eoper = ecost_list[owntime - 1]
        eafter = int(ecarprice - edepr_total[owntime - 1])

        # Gasoline car price calculation
        gyearly = int(drivekm * gprice * (gconsumption / 100) + gtax)
        gdepr_total, gdepr_yearly, gcost_list = depr_oper(gcarprice, gdepr, owntime, gyearly)
        gdepr_owntime = int(gdepr_total[owntime - 1])
        gtotal = int(gcost_list[owntime - 1] + gdepr_total[owntime - 1])
        goper = gcost_list[owntime - 1]
        gafter = int(gcarprice - gdepr_total[owntime - 1])

        # Diesel car price calculation
        dyearly = int(drivekm * dprice * (dconsumption / 100) + ddrivingpower + dtax)
        ddepr_total, ddepr_yearly, dcost_list = depr_oper(dcarprice, ddepr, owntime, dyearly)
        ddepr_owntime = int(ddepr_total[owntime - 1])
        dtotal = int(dcost_list[owntime - 1] + ddepr_total[owntime - 1])
        doper = dcost_list[owntime - 1]
        dafter = int(dcarprice - ddepr_total[owntime - 1])

        if echarger == 'No':
            etotal = etotal + chargerprice

    except TypeError:
        error = 'Error'
        pass

    return render_template('cars.html',
                           form=form,
                           car_form=car_form,
                           eyearly=eyearly,
                           etotal=etotal,
                           edepr_owntime=edepr_owntime,
                           eoper=eoper,
                           eafter=eafter,
                           gyearly=gyearly,
                           gtotal=gtotal,
                           gdepr_owntime=gdepr_owntime,
                           goper=goper,
                           gafter=gafter,
                           dyearly=dyearly,
                           dtotal=dtotal,
                           ddepr_owntime=ddepr_owntime,
                           doper=doper,
                           dafter=dafter,
                           owntime=owntime,
                           error=error,
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