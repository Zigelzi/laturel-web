from tabulate import tabulate
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class Cars(db.Model):

    #  Initializing database columns.
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    maker = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    battery = db.Column(db.Float)
    driverange = db.Column(db.Integer)
    consumption = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    #  Printout formatting
    def __repr__(self):
        return f"<Cars(type='{self.type}'," \
            f" maker='{self.maker}'," \
            f" model='{self.model}'," \
            f" price='{self.price}'," \
            f" battery='{self.battery}'," \
            f" driverange='{self.driverange}'," \
            f" consumption='{self.consumption}'," \
            f" weight='{self.weight}')>"


#  Adding cars to database with one command.
def add_cars():
    car_list = []
    dash_line = (40 * '-') + '\n'

    print('Adding new cars to database')
    print(dash_line)
    while True:
        car_dict = {}
        allowed_types = ['ev', 'gasoline', 'diesel']

        #  Query user for values for the row to be commited.
        car_dict['type'] = input('Engine type (EV/Gasoline/Diesel): ').lower()
        if car_dict['type'] not in allowed_types:
            print('Enter correct engine type (EV/Gasoline/Diesel): ')
            continue
        car_dict['maker'] = input('Maker: ').lower()
        car_dict['model'] = input('Model: ').lower()
        car_dict['price'] = input('Price: (€) ').lower()
        #  Battery is optional value, set to None if left blank.
        car_dict['battery'] = input('Battery size (kWh, optional): ').lower()
        if car_dict['battery'] == '':
            car_dict['battery'] = None
        #  Drive range is optional value, set to None if left blank.
        car_dict['driverange'] = input('Drive range (km, optional): ').lower()
        if car_dict['driverange'] == '':
            car_dict['driverange'] = None
        car_dict['consumption'] = input('Consumption (kWh/100km): ').lower()
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
                       price=cars['price'],
                       battery=cars['battery'],
                       driverange=cars['driverange'],
                       consumption=cars['consumption'],
                       weight=cars['weight'])
            db.session.add(car)
        db.session.commit()
        print('\nChanges committed succesfully to database!')
    else:
        print('No changes committed to database.')
        return
