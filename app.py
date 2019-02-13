from flask import Flask, render_template, request
from forms import ChargerForm, eForm, gForm, dForm, driveForm
from config import Config
from datetime import datetime
from helpers import round_hundreds, deprecation

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
    esubsidy = eform.esubsidy.data
    econsumption = eform.econsumption.data
    eprice = eform.eprice.data
    eweight = eform.eweight.data
    edrivingpower = round_hundreds(eweight)  # Round to starting hundreds and multiply by 0.055 (€)
    etax = eform.etax.data
    echarger = eform.echarger.data
    chargerprice = 800

    # Gasoline car data from gasoline form
    gcarprice = gform.gcarprice.data
    gdepr = gform.gdepr.data
    gconsumption = gform.gconsumption.data
    gprice = gform.gprice.data
    gtax = gform.gtax.data

    # Diesel car data from diesel form
    dcarprice = dform.dcarprice.data
    ddepr = dform.ddepr.data
    dconsumption = dform.dconsumption.data
    dprice = dform.dprice.data
    dweight = dform.dweight.data
    ddrivingpower = round_hundreds(dweight)  # Round to starting hundreds and multiply by 0.055 (€)
    dtax = dform.dtax.data

    drivekm = kmform.drivekm.data
    owntime = kmform.owntime.data

    edeprcalc = 0
    gdeprcalc = 0
    ddeprcalc = 0

    eyearly = 0
    gyearly = 0
    dyearly = 0

    etotal = 0
    gtotal = 0
    dtotal = 0

    # Calculating the driving power tax based on car weight.
    try:
        edrivingpower = edrivingpower * 0.015 * 365 # EV 0.015€/starting 100 kg
        ddrivingpower = ddrivingpower * 0.055 * 365# Diesel 0.055€/starting 100 kg
    except TypeError:
        pass

    # EV price calculation
    edeprcalc = deprecation(ecarprice, edepr, owntime)
    eyearly = drivekm * eprice * (econsumption / 100) + etax + edrivingpower
    eyearly = int(eyearly)  # int for rounding to full numbers
    etotal = int(eyearly * owntime + edeprcalc - esubsidy)  # int for rounding to full numbers


    if echarger == 'No':
        try:
            etotal = etotal + chargerprice
        except TypeError:
            etotal = None
            pass

    # Gasoline car price calculation
    gdeprcalc = deprecation(gcarprice, gdepr, owntime)
    gyearly = drivekm * gprice * (gconsumption / 100) + gtax
    gyearly = int(gyearly)  # int for rounding to full numbers
    gtotal = int(gyearly * owntime + gdeprcalc)  # int for rounding to full numbers

    # Diesel car price calculation
    ddeprcalc = deprecation(dcarprice, ddepr, owntime)
    dyearly = drivekm * dprice * (dconsumption / 100) + ddrivingpower + dtax
    dyearly = int(dyearly)  # int for rounding to full numbers
    dtotal = int(dyearly * owntime + ddeprcalc)  # int for rounding to full numbers

    return render_template('cars.html',
                           eform=eform,
                           gform=gform,
                           dform=dform,
                           kmform=kmform,
                           eyearly=eyearly,
                           etotal=etotal,
                           gyearly=gyearly,
                           gtotal=gtotal,
                           dyearly=dyearly,
                           dtotal=dtotal,
                           owntime=owntime)

@app.route('/about')
def about():
    return render_template('about.html')
