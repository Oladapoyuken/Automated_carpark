import cv2
import full
import Database_control
import Main
from PIL import ImageEnhance
from PIL import Image
import  image_enhancement

def startProgram(image):
    error = False
    plateNumber = []
    data = ''
    checker = True
    try:
        text = full.execute_ALPR(image)
        if text != False:
            print('Method one: {}'.format(text))
            plateNumber.append(text)
            checker = True
        else:
            try:
                text = Main.main(image)
                if text != None:
                    print('Method two: {}'.format(text))
                    plateNumber.append(text)
                    checker = False
            except:
                print('Error occured, Image not okay')
        # if checker == True:
        #     text = Main.main(image)
        #     if text != None:
        #         print('Method two: {}'.format(text))
        #         plateNumber.append(text)

    except:
        try:
            text = Main.main(image)
            if text != None:
                print('Method two: {}'.format(text))
                plateNumber.append(text)
            else:
                print('Error occured, Image not okay')
        except:
            print('Error occured, Image not okay')


    # print(plateNumber)
    if len(plateNumber) == 2:
        if len(plateNumber[0]) >= len(plateNumber[1]) or len(plateNumber[1]) - len(plateNumber[0]) < 2:
            data = plateNumber[0]
        else:
            print('Im two')
            data = plateNumber[1]
    elif len(plateNumber) == 1:
        data = plateNumber[0]
    else:
        data = '0'

    return data

def image_preprocess(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(img)
    enh_bri = ImageEnhance.Brightness(image)
    image_br = enh_bri.enhance(1.5)
    # image_br.show()

    enh_col = ImageEnhance.Color(image_br)
    image_col = enh_col.enhance(1.5)
    # image_col.show()

    enh_con = ImageEnhance.Contrast(image_col)
    image_con = enh_bri.enhance(1.5)
    # image_con.show()

    enh_sha = ImageEnhance.Sharpness(image_con)
    image_sha = enh_sha.enhance(1.5)
    image_sha.show()

    return image_sha




db = Database_control


imagepath = 'C:\\Users\\Yuken4real\\PycharmProjects\\Automated_carpark\\test_images\\rasbian1.jpg'

image = cv2.imread(imagepath)
#image = image_enhancement.image_cv(image)
# image = image_preprocess(image)
state = False
data = startProgram(image)
# print('\nPlate Number: {}'.format(data))

if state == True:

    if data != '0':

        if db.Entering_process(data) == True:
            print('GRANTED, vehicle may go in')
        else:
            print ('REVOKED!')

    else:
        print('Database is not responding')

else:
    if data != '0':

        if db.Leaving_process(data) == True:
            print('GRANTED, vehicle may go out')
        else:
            print('REVOKED')

    else:
        print('Database is not responding')

print('\n')
showAllCars = db.showAll()
print('PLATE NUMBERS\tLOCATION\t\tTIME IN\t\tTIME OUT')
for carInfos in showAllCars:
    print('{}\t\t{}\t\t{}\t\t{}'.format(carInfos[0], carInfos[1], carInfos[2], carInfos[3]))

# image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
cv2.imshow('IMAGE', image)
cv2.waitKey(0)
