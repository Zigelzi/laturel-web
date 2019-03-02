from db import db
from tabulate import tabulate

class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maker = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    battery = db.Column(db.Float)
    driverange = db.Column(db.Integer)
    consumption = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Cars(maker='{self.maker}', model='{self.model}', price='{self.price}', battery='{self.battery}'," \
            f"range='{self.driverange}', consumption='{self.consumption}', weight='{self.weight}')>"


#  Adding cars to database with one command.
def add_car():
    car_list = []

    print('Adding new cars to database')
    print('-----------------------------')
    while True:
        car_dict = {}

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
        print(f'Values added for {car_dict["maker"]} {car_dict["model"]}.')
        answer_add = input(' Add another? (y/n)').lower()
        if answer_add == 'n':
            break

    print('Cars to be added to database:\n')
    result_table = tabulate(car_list, headers='keys', tablefmt='orgtbl')
    print(result_table)
    print()

    answer_commit = input('Commit these changes to database? (y/n')

    if answer_commit == 'y':
        for cars in car_list:
            car = Cars(maker=cars['maker'],
                       model=cars['model'],
                       price=cars['price'],
                       battery=cars['battery'],
                       driverange=cars['driverange'],
                       consumption=cars['consumption'],
                       weight=cars['weight'])
            db.session.add(car)
        db.session.commit()
        print('\nChanges committed to database!')
    else:
        print('No changes committed to database.')
        return
