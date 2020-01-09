import Database_control

showAllCars = Database_control.showAll()
print('PLATE NUMBERS\tLOCATION\t\tTIME IN\t\tTIME OUT')
for carInfos in showAllCars:
    print('{}\t\t{}\t\t{}\t\t{}'.format(carInfos[0], carInfos[1], carInfos[2], carInfos[3]))