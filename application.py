from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    active = True
    return render_template('index.html')

@app.route('/index')
def index2():
    return render_template('index.html')

@app.route('/chargers', methods=['POST', 'GET'])
def chargers():
    if request.method == 'GET':
        drivekm = '-'
        endtime = '-'
        starttime = '-'
        return render_template('chargers.html', drivekm=drivekm, endtime=endtime, starttime=starttime)
    else:
        drivekm = request.form.get('drivekm')
        endtime = request.form.get('endtime')
        starttime = request.form.get('starttime')
        return render_template('chargers.html', drivekm=drivekm, endtime=endtime, starttime=starttime)

@app.route('/evbasics')
def evbasics():
    return render_template('evbasics.html')

@app.route('/cars')
def cars():
    return render_template('cars.html')

@app.route('/about')
def about():
    return render_template('about.html')
