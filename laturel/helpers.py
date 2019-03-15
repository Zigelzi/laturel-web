'''
Python file for helper functions
'''

import csv

def get_csv():

    file = input('Enter the absolute file path')
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        list = []
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            list.append(dict(row))
    return list