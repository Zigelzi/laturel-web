from flask import Flask, render_template, request
from forms import ChargerForm
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

@app.route('/cars')
def cars():
    return render_template('cars.html')

@app.route('/about')
def about():
    return render_template('about.html')
