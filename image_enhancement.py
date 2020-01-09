from PIL import Image
from PIL import ImageEnhance
import cv2
import numpy as np

def image_preprocess(image):
    # image = Image.open('rasbian.jpg')
    # image.show()

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
    # image_sha.show

    return image_sha

def image_cv(im):
    # im = cv2.imread('test_images\\rasbian1.jpg')
    im = im/255.0
    im_power = cv2.pow(im, 0.6)
    # cv2.imshow('ORIGINAL', im)
    # cv2.imshow('PROCESSED', im_power)
    return im_power
    # cv2.waitKey(0)

#image_cv()