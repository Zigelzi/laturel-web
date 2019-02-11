from flask import Flask, render_template, request
from forms import ChargerForm, eForm, gForm, dForm, driveForm
from config import Config
from datetime import datetime

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

    econsumption = eform.econsumption.data
    eprice = eform.eprice.data
    edrivingpower = eform.edrivingpower.data
    etax = eform.etax.data
    echarger = eform.echarger.data
    chargerprice = 800

    gconsumption = gform.gconsumption.data
    gprice = gform.gprice.data
    gtax = gform.gtax.data

    dconsumption = dform.dconsumption.data
    dprice = dform.dconsumption.data
    ddrivingpower = dform.ddrivingpower.data
    dtax = dform.dtax.data

    drivekm = kmform.drivekm.data

    eyearly = 0
    gyearly = 0
    dyearly = 0

    # EV price calculation
    if echarger == 'Yes':
        try:
            eyearly = drivekm * eprice * (econsumption / 100) + etax + edrivingpower + chargerprice
        except TypeError:
            pass
    else:
        try:
            eyearly = drivekm * eprice * (econsumption / 100) + etax + edrivingpower
        except TypeError:
            pass

    # Gasoline car price calculation
    try:
        gyearly = drivekm * gprice * (gconsumption / 100) + gtax
    except TypeError:
        pass

    # Diesel car price calculation
    try:
        dyearly = drivekm * dprice * (dconsumption / 100) + ddrivingpower + dtax
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
