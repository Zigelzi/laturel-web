from flask import Flask, render_template, request
from forms import ChargerForm, eForm, gForm, dForm, driveForm
from config import Config
from datetime import datetime
from helpers import round_hundreds

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    active = True
    return render_template('index.html')

@app.route('/index')
def index2():
    return render_template('index.html')

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
                           chargingTime=chargingTime)


@app.route('/evbasics')
def evbasics():
    return render_template('evbasics.html')

@app.route('/cars', methods=['GET', 'POST'])
def cars():
    eform = eForm()
    gform = gForm()
    dform = dForm()
    kmform = driveForm()

    # EV data from EV form
    ecarprice = eform.ecarprice.data
    edepr = eform.edepr.data
    econsumption = eform.econsumption.data
    eprice = eform.eprice.data
    eweight = eform.eweight.data
    edrivingpower = round_hundreds(eweight)  # Round to starting hundreds and multiply by 0.055 (€)
    etax = eform.etax.data
    echarger = eform.echarger.data
    chargerprice = 800

    # Gasoline car data from gasoline form
    gconsumption = gform.gconsumption.data
    gprice = gform.gprice.data
    gtax = gform.gtax.data

    # Diesel car data from diesel form
    dconsumption = dform.dconsumption.data
    dprice = dform.dprice.data
    dweight = dform.dweight.data
    ddrivingpower = round_hundreds(dweight)  # Round to starting hundreds and multiply by 0.055 (€)
    dtax = dform.dtax.data

    drivekm = kmform.drivekm.data

    eyearly = 0
    gyearly = 0
    dyearly = 0

    # Calculating the driving power tax based on car weight.
    try:
        edrivingpower = edrivingpower * 0.015  # EV 0.015€/starting 100 kg
        ddrivingpower = ddrivingpower * 0.055  # Diesel 0.055€/starting 100 kg
    except TypeError:
        pass

    # EV price calculation
    try:
        eyearly = drivekm * eprice * (econsumption / 100) + etax + edrivingpower
        eyearly = int(eyearly)
    except TypeError:
        pass

    if echarger == 'No':
        try:
            eyearly = eyearly + chargerprice
        except TypeError:
            eyearly = None
            pass

    # Gasoline car price calculation
    try:
        gyearly = drivekm * gprice * (gconsumption / 100) + gtax
        gyearly = int(gyearly)
    except TypeError:
        pass

    # Diesel car price calculation
    try:
        dyearly = drivekm * dprice * (dconsumption / 100) + ddrivingpower + dtax
        dyearly = int(dyearly)
    except TypeError:
        pass

    return render_template('cars.html',
                           eform=eform,
                           gform=gform,
                           dform=dform,
                           kmform=kmform,
                           eyearly=eyearly,
                           gyearly=gyearly,
                           dyearly=dyearly)

@app.route('/about')
def about():
    return render_template('about.html')
