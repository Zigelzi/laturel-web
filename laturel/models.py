from tabulate import tabulate
from laturel import db

class Cars(db.Model):

    #  Initializing database columns.
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    maker = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    body_type = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    battery = db.Column(db.Float)
    driverange = db.Column(db.Integer)
    consumption = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    fullmodel = db.Column(db.String(60), nullable=False)
    co2 = db.Column(db.Float, nullable=False)

    #  Printout formatting
    def __repr__(self):
        return f"<Cars(type='{self.type}'," \
            f" maker='{self.maker}'," \
            f" model='{self.model}'," \
            f" body_type='{self.body_type}'," \
            f" price='{self.price}'," \
            f" battery='{self.battery}'," \
            f" driverange='{self.driverange}'," \
            f" consumption='{self.consumption}'," \
            f" weight='{self.weight}'," \
            f"fullmodel={self.fullmodel}," \
            f"co2={self.co2})>"


class Co2Tax(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    co2 = db.Column(db.Integer, nullable=False)
    tax = db.Column(db.Float, nullable=False)

    #  Printout formatting
    def __repr__(self):
        return f"<Co2Tax( co2='{self.co2}'," \
            f"tax='{self.tax}' )>"


#  Adding cars to database with one command.
def add_cars():
    car_list = []
    dash_line = (40 * '-') + '\n'

    #  Function to validate that correct body type and engine type is entered
    def check_type(checked_type):
        allowed_types = ['ev', 'gasoline', 'diesel']
        allowed_body_types = ['sedan', 'suv', 'wagon', 'hatchback']
        car_type = ''
        if checked_type == 'type':
            while True:
                car_type = input('Engine type (EV/Gasoline/Diesel): ').lower()
                if car_type not in allowed_types:
                    print('Enter correct engine type (EV/Gasoline/Diesel): ')
                    continue
                break
        if checked_type == 'body_type':
            while True:
                car_type = input('Body type (sedan/suv/wagon/hatchback): ').lower()
                if car_type not in allowed_body_types:
                    print('Enter correct body type (sedan/suv/wagon): ')
                    continue
                break
        return car_type



    print('Adding new cars to database')
    print(dash_line)
    while True:
        car_dict = {}
        #  Query user for values for the row to be commited.
        car_dict['type'] = check_type('type')
        car_dict['maker'] = input('Maker: ').lower()
        car_dict['model'] = input('Model: ').lower()
        car_dict['body_type'] = check_type('body_type')
        car_dict['price'] = input('Price: (€) ').lower()
        #  Battery is optional value, set to None if left blank.
        car_dict['battery'] = input('Battery size (kWh, optional): ').lower()
        if car_dict['battery'] == '':
            car_dict['battery'] = None
        #  Drive range is optional value, set to None if left blank.
        car_dict['driverange'] = input('Drive range (km, optional): ').lower()
        if car_dict['driverange'] == '':
            car_dict['driverange'] = None
        car_dict['consumption'] = input('Consumption (kWh or l/100km): ').lower()
        car_dict['weight'] = input('Weight (kg): ').lower()
        car_list.append(car_dict)
        print(f'Values added for {car_dict["maker"].upper()} {car_dict["model"].upper()}.')
        print(dash_line)
        answer_add = input(' Add another? (y/n)').lower()
        if answer_add == 'n':
            break

    #  Print out the inputted cars and confirm the commit
    print('Cars to be added to database:\n')
    result_table = tabulate(car_list, headers='keys', tablefmt='orgtbl')
    print(result_table)

    answer_commit = input('Commit these changes to database? (y/n)')
    if answer_commit == 'y':
        #  Loop through the list of inputted cars and take values from individual dictionaries to input
        for cars in car_list:
            car = Cars(type=cars['type'],
                       maker=cars['maker'],
                       model=cars['model'],
                       body_type=cars['body_type'],
                       price=cars['price'],
                       battery=cars['battery'],
                       driverange=cars['driverange'],
                       consumption=cars['consumption'],
                       weight=cars['weight'])
            db.session.add(car)
        db.session.commit()
        db.session.close_all()
        print('\nChanges committed succesfully to database!')
    else:
        print('No changes committed to database.')
        return


#  Query all cars in database and create list list for Select field
def get_cars():
    ecars = Cars.query.filter_by(type='ev').all()
    gcars = Cars.query.filter_by(type='gasoline').all()
    dcars = Cars.query.filter_by(type='diesel').all()
    ecars_select = []
    gcars_select = []
    dcars_select = []
    for car in ecars:
        ecars_select.append((car.model, f'{car.maker.capitalize()} {car.model.capitalize()}'))
    for car in gcars:
        gcars_select.append((car.model, f'{car.maker.capitalize()} {car.model.capitalize()}'))
    for car in dcars:
        dcars_select.append((car.model, f'{car.maker.capitalize()} {car.model.capitalize()}'))
    return ecars_select, gcars_select, dcars_select


#  Function to query all models from database and make list of dictionaries from them
def get_car_dict():
    cars = Cars.query.all()
    car_list = []
    for car in cars:
        try:
            car_dict = car.__dict__
            car_dict.pop('_sa_instance_state')
            car_list.append(car_dict)
        except TypeError:
            pass
    for i in car_list:
        for key in i:
            i[key] = str(i[key])
    return car_list


#  Query model from Select Box in /cars and return it's data
def model_dict(type, model):
    car = Cars.query.filter_by(type=type, model=model).first()
    car_dict = car.__dict__
    car_dict.pop('_sa_instance_state')
    return car_dict

def co2_dict(co2):
    tax_value = Co2Tax.query.filter_by(co2=co2).first()
    tax_value_dict = car.__dict__
    tax_value_dict.pop('_sa_instance_state')
    return tax_value_dict

