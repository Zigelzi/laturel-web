from flask import Flask, render_template, request, flash
from forms import ChargerForm, Form
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
    form = Form()

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
    ziplist = []

    # EV data from EV form
    eform_ecarprice = form.ecarprice
    ecarprice = eform_ecarprice.data
    edepr = form.edepr.data
    esubsidy = form.esubsidy.data
    econsumption = form.econsumption.data
    eprice = form.eprice.data
    eweight = form.eweight.data
    edrivingpower = round_hundreds(eweight)  # Round to starting hundreds and multiply by 0.055 (€)
    etax = form.etax.data
    echarger = form.echarger.data
    chargerprice = 800

    # Gasoline car data from gasoline form
    gcarprice = form.gcarprice.data
    gdepr = form.gdepr.data
    gconsumption = form.gconsumption.data
    gprice = form.gprice.data
    gtax = form.gtax.data

    # Diesel car data from diesel form
    dcarprice = form.dcarprice.data
    ddepr = form.ddepr.data
    dconsumption = form.dconsumption.data
    dprice = form.dprice.data
    dweight = form.dweight.data
    ddrivingpower = round_hundreds(dweight)  # Round to starting hundreds and multiply by 0.055 (€)
    dtax = form.dtax.data

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

        ziplist = zip(edepr_yearly, gdepr_yearly, ddepr_yearly)

        if echarger == 'No':
            etotal = etotal + chargerprice

    except TypeError:
        error = 'TypeError'
        pass

    return render_template('cars.html',
                           form=form,
                           eyearly=eyearly,
                           etotal=etotal,
                           edepr_owntime=edepr_owntime,
                           edepr_yearly=edepr_yearly,
                           ecost_list=ecost_list,
                           eoper=eoper,
                           eafter=eafter,
                           gyearly=gyearly,
                           gtotal=gtotal,
                           gdepr_owntime=gdepr_owntime,
                           gdepr_yearly=gdepr_yearly,
                           gcost_list=gcost_list,
                           goper=goper,
                           gafter=gafter,
                           dyearly=dyearly,
                           dtotal=dtotal,
                           ddepr_owntime=ddepr_owntime,
                           ddepr_yearly=ddepr_yearly,
                           dcost_list=dcost_list,
                           doper=doper,
                           dafter=dafter,
                           owntime=owntime,
                           ziplist=ziplist,
                           error=error
                           )


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=False)