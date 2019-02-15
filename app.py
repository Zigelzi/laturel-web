from flask import Flask, render_template, request
from forms import ChargerForm, eForm, gForm, dForm, driveForm
from config import Config
from datetime import datetime
from helpers import round_hundreds, deprecation, depr_oper

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

    error = None

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
        ddrivingpower = ddrivingpower * 0.055 * 365 # Diesel 0.055€/starting 100 kg
    except TypeError:
        pass

    # EV price calculation
    eyearly = int(drivekm * eprice * (econsumption / 100) + etax + edrivingpower)  # int for rounding to full numbers

    #  Use function to take deprecation values, yearly deprecation and yearly
    #  operating costs and assign them to variables.
    edepr_total, edepr_yearly, ecost_list = depr_oper(ecarprice, edepr, owntime, eyearly)

    # Take the index of the lists and calculate total costs
    etotal = int(ecost_list[owntime-1] + edepr_total[owntime-1] - esubsidy)
    eoper = ecost_list[owntime-1]
    eafter = int(ecarprice - edepr_total[owntime-1])


    if echarger == 'No':
        try:
            etotal = etotal + chargerprice
        except TypeError:
            etotal = None
            pass

    # Gasoline car price calculation
    gyearly = int(drivekm * gprice * (gconsumption / 100) + gtax)
    gdepr_total, gdepr_yearly, gcost_list = depr_oper(gcarprice, gdepr, owntime, gyearly)
    gtotal = int(gcost_list[owntime-1] + gdepr_total[owntime-1])
    goper = gcost_list[owntime-1]
    gafter = int(gcarprice - gdepr_total[owntime - 1])

    # Diesel car price calculation
    dyearly = int(drivekm * dprice * (dconsumption / 100) + ddrivingpower + dtax)
    ddepr_total, ddepr_yearly, dcost_list = depr_oper(dcarprice, ddepr, owntime, dyearly)
    dtotal = int(dcost_list[owntime-1] + ddepr_total[owntime-1])
    doper = dcost_list[owntime-1]
    dafter = int(dcarprice - ddepr_total[owntime - 1])

    ziplist= zip(edepr_yearly,gdepr_yearly,ddepr_yearly)


    return render_template('cars.html',
                           eform=eform,
                           gform=gform,
                           dform=dform,
                           kmform=kmform,
                           eyearly=eyearly,
                           etotal=etotal,
                           edepr_yearly=edepr_yearly,
                           ecost_list=ecost_list,
                           eoper=eoper,
                           eafter=eafter,
                           gyearly=gyearly,
                           gtotal=gtotal,
                           gdepr_yearly=gdepr_yearly,
                           gcost_list=gcost_list,
                           goper=goper,
                           gafter=gafter,
                           dyearly=dyearly,
                           dtotal=dtotal,
                           ddepr_yearly=ddepr_yearly,
                           dcost_list=dcost_list,
                           doper=doper,
                           dafter=dafter,
                           owntime=owntime,
                           ziplist=ziplist
                           )

@app.route('/about')
def about():
    return render_template('about.html')
