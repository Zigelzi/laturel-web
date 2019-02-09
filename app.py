from flask import Flask, render_template, request
from forms import ChargerForm
from config import Config
import datetime

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
    deptTime = form.date1.data - form.date2.data # Taking the
    return render_template('chargers.html', form=form, deptTime=deptTime)


@app.route('/evbasics')
def evbasics():
    return render_template('evbasics.html')

@app.route('/cars')
def cars():
    return render_template('cars.html')

@app.route('/about')
def about():
    return render_template('about.html')
