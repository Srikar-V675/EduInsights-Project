import cv2
import numpy as np
import pytesseract
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from captcha_solver import captcha_og

USN = input('Enter your USN: ')

#function to solve captcha
def solve_captcha(driver):
    div_element = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div/div[2]/form/div/div[2]/div[2]/div[2]/img')
    div_element.screenshot(r'Data\Captcha\unsolved.png')

    # load imge and set the bounds
    img = cv2.imread(r'Data\Captcha\unsolved.png')
    lower =(102, 102, 102) # lower bound for each channel
    upper = (125,125, 125) # upper bound for each channel

    # create the mask and use it to change the colors
    mask = cv2.inRange(img, lower, upper)
    img[mask != 0] = [0,0,0]

    # Save it
    cv2.imwrite(r'Data\Captcha\semisolved.png',img)

    img = Image.open(r'Data\Captcha\semisolved.png') # get image
    pixels = img.load() # create the pixel map

    for i in range(img.size[0]): # for every pixel:
        for j in range(img.size[1]):
            if pixels[i,j] != (0,0,0): # if not black:
                pixels[i,j] = (255, 255, 255) # change to white
    #img.show()
    img.save(r'Data\Captcha\solved.png')


    # read image
    img = cv2.imread(r'Data\Captcha\solved.png')

    # configurations
    config = ('-l eng --oem 1 --psm 3')

    # pytessercat
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text = pytesseract.image_to_string(img, config=config)

    # print text
    tes_captcha = text.split('\n')[0]
    captcha=captcha_og()
    if len(captcha) < 6 :
        return tes_captcha

    return captcha

