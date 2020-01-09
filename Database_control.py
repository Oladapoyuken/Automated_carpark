import sqlite3
import time
from datetime import datetime

conn = sqlite3.connect('Cars.db')
c = conn.cursor()


# c.execute("""CREATE TABLE plate_numbers (
#             reg_number text,
#             mode integer,
#             time_in text,
#             time_out text
#             )""")

def clearAll():
    c.execute("DELETE from plate_numbers")
    conn.commit()


def getDateTime():
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M')
    return formatted_date


def deletePlateData(platedata):
    c.execute("DELETE FROM plate_numbers WHERE reg_number = ?", (platedata,))
    conn.commit()


def storePlateData(reg_number, mode, time_in, time_out):
    c.execute("INSERT INTO plate_numbers VALUES (?, ?, ?, ?)", (reg_number, mode, time_in, time_out))
    conn.commit()


def checkPlateData(reg_number):
    c.execute("SELECT * FROM plate_numbers WHERE reg_number = ?", (reg_number,))
    result = c.fetchone()
    conn.commit()
    return result


def forward(reg_number, mode, time_in, time_out):
    with conn:

        c.execute("UPDATE plate_numbers SET mode = ?, time_in = ?, time_out = ? WHERE reg_number = ?",
                  (mode, time_in, time_out, reg_number))
        print('data saved in database')
    conn.commit()


def backward(reg_number, mode, time_out):
    with conn:
        c.execute("UPDATE plate_numbers SET mode = ?, time_out = ? WHERE reg_number = ?",
                  (mode, time_out, reg_number))
    conn.commit()


def showAllRegisteredCars():
    c.execute("SELECT reg_number FROM plate_numbers")
    result = c.fetchall()
    list = []
    for plates in result:
        list.append(plates[0])
    return list



def showAllCarsInPark(car_in):
    c.execute("SELECT reg_number FROM plate_numbers WHERE mode = ?", (car_in,))
    result = c.fetchall()
    list = []
    if result != None:
        for plates in result:
            list.append(plates[0])
    return list


def showAll():
    c.execute("SELECT * FROM plate_numbers")
    result = c.fetchall()
    return result


def getCarDuration(self, reg_number):
    c.execute("SELECT * FROM plate_numbers WHERE reg_number = ?", (reg_number,))
    result = c.fetchone()
    if result != None:
        time_in = datetime.strptime(result[2], '%Y-%m-%d %H:%M')
        time_out = datetime.strptime(result[3], '%Y-%m-%d %H:%M')
        duration = ((time_out - time_in).seconds / 3600) * 60

        # Returns duration in minutes
        return duration


def confirm_plate(plates, data):
    plate_length = 0
    l1 = len(plates)
    l2 = len(data)
    counter = 0

    list_plate = list(plates)
    list_data = list(data)
    for i in range(min(l1, l2)):
        if list_plate[i] != list_data[i]:
            counter += 1
    if counter > 2:
        return False
    else:
        return True


def Entering_process(data):
    grant = True
    result = checkPlateData(data)
    state = True
    if result != None:
        if result[1] == 1:
            print('Vehicle with same plate number already in the car park')
            grant = False
        else:
            forward(data, 1, getDateTime(), '0')
            print('Car registered before, now Timed In')
    else:
        print('could not find original me in database')
        listofplate = showAllRegisteredCars()
        for plates in listofplate:
            if confirm_plate(plates, data) == True:
                state = False
                data = plates
                result = checkPlateData(data)
                if result != None:
                    if result[1] == 1:
                        print('Vehicle with same plate number already in the car park')
                        grant = False
                    else:
                        forward(data, 1, getDateTime(), '0')
                        print('Car registered before, now Timed In')
                    break
                else:
                    storePlateData(data, 1, getDateTime(), '0')
                    print('New car found, now Timed In')
                    break
            else:
                print('Plate not found')
        if state == True:
            print('could not find fake and original me')
            storePlateData(data, 1, getDateTime(), '0')
            print('New car found, now Timed In')
    return grant

def Leaving_process(data):
    grant = True
    result = checkPlateData(data)
    state = True
    if result != None:
        if result[1] == 1:
            backward(data, 0, getDateTime())
        else:
            print('How did you get in')
            grant = False
    else:
        listofplate = showAllCarsInPark(1)
        for plates in listofplate:
            if confirm_plate(plates, data) == True:
                state = False
                data = plates
                result = checkPlateData(data)
                if result != None:
                    if result[1] == 1:
                        backward(data, 0, getDateTime())
                    else:
                        print('How Did you get in')
                        grant = False

        if state == True:
            print('How did you get in, Plate number not found inside')
            grant = False

    return grant



def diffDate(date1, date2):
    return

# db.storePlateData('LSR255AP', 1, getDateTime(), '')
# reg_data = db.checkPlateData('GWA294NV')
# print(reg_data)

# deletePlateData('KJA193AA')

#clearAll()
# Entering_process('LSR255AP')
# Leaving_process('KJA193AA')

# print(showAllCarsInPark(1))


# minute = db.getCarDuration('GWA294NV')
# print(minute)

# storePlateData('KJA193AA', 1, getDateTime(), '')
# reg_data = db.checkPlateData('KJA193AA')
# print(reg_data)

# showAllCars = showAllRegisteredCars()
# for i in range(len(showAllCars)):
#     print(showAllCars[i])

# allCars = db.showAllCarsInPark(1)
# print(allCars)

# print(getDateTime())


# conn.close()
