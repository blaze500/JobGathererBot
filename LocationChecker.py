import csv

def isCity(city):
    if city[0].isalpha() is False or city[0] == ' ':
        return False
    reader = csv.reader(open('US_City_And_States/' + city[0].upper() + '_Cities_PlusTheirStates.csv', 'rt'), delimiter=',')
    for row in reader:
        if city.lower() == row[0].lower():
            return True
    return False

def isState(state):
    if state[0].isalpha() is False or state[0] == ' ':
        return False
    reader = csv.reader(open('US_City_And_States/US_States.csv', 'rt'), delimiter=',')
    for row in reader:
        if state.lower() == row[0].lower():
            return True
    return False

def isLocation(location):
    if location[0].isalpha() is False or location[0] == ' ':
        return False
    reader = csv.reader(open('US_City_And_States/' + location[0].upper() + '_Cities_PlusTheirStates.csv', 'rt'), delimiter=',')
    for row in reader:
        cityAndStateLocation = row[0] +',' + row[1]
        if location.lower() == cityAndStateLocation.lower():
            return True
    return False
