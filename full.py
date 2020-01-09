import os
from preprocess import PreProcess
from deepMachine import DeepMachineLearning
from ocr import OCROnObjects
from textclassification import TextClassification
import time

# from dbAspect import DBConnection

imagepath = ''
listRow = 0
listResult = ''


# instantiate the db connection
# db_aspect = DBConnection()

def license_plate_extract(plate_like_objects, pre_process):
    number_of_candidates = len(plate_like_objects)

    if number_of_candidates == 0:
        print('Method ONE failed: could not locate plate')
        # wx.MessageBox("License plate could not be located",
        #     "Plate Localization" ,wx.OK|wx.ICON_ERROR)
        return []

    if number_of_candidates == 1:
        license_plate = pre_process.inverted_threshold(plate_like_objects[0])
    else:
        license_plate = pre_process.validate_plate(plate_like_objects)

    return license_plate


def execute_ALPR(imagepath):
    """
    runs the full license plate recognition process.
    function is called when user clicks on the execut button on the gui
    """

    # time the function execution
    start_time = time.time()

    root_folder = os.path.dirname(os.path.realpath(__file__))

    # print(root_folder)
    models_folder = os.path.join(root_folder, 'ml_models')
    # pre_process = PreProcess(imagepath)
    pre_process = PreProcess(imagepath)
    # print(imagepath)

    plate_like_objects = pre_process.get_plate_like_objects()
    # plotting.plot_cca(pre_process.full_car_image,
    #     pre_process.plate_objects_cordinates)

    license_plate = license_plate_extract(plate_like_objects, pre_process)
    # if license_plate == False:
    #     print('Method ONE failed: could not find any character')
    #     return False
    if len(license_plate) == 0:
        print('Method ONE failed: could not find any character')
        return False

    ocr_instance = OCROnObjects(license_plate)

    if ocr_instance.candidates == {}:
        print('Method ONE failed: could not segment')
        # wx.MessageBox("No character was segmented",
        #               "Character Segmentation", wx.OK | wx.ICON_ERROR)
        return False

    # plotting.plot_cca(license_plate, ocr_instance.candidates['coordinates'])

    deep_learn = DeepMachineLearning()
    text_result = deep_learn.learn(ocr_instance.candidates['fullscale'],
                                   os.path.join(models_folder, 'SVC_model', 'SVC_model.pkl'),
                                   (20, 20))

    text_phase = TextClassification()
    scattered_plate_text = text_phase.get_text(text_result)
    plate_text = text_phase.text_reconstruction(scattered_plate_text,
                                                ocr_instance.candidates['columnsVal'])

    # print('ALPR process took ' + str(time.time() - start_time) + ' seconds')
    # print('License plate read from image = {}'.format(plate_text))
    return plate_text
