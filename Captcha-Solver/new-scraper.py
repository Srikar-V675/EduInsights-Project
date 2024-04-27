import cv2
import numpy as np
import pytesseract
import time
import threading
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from captcha_solver import captcha_og

start_usn = int(input('Enter the start USN number: '))
end_usn = int(input('Enter the end USN number: '))
count = 0
error_count = 0
start_time = time.time()
names = []

# Function to solve captcha
def solve_captcha(driver):
    div_element = driver.find_element('xpath', '//*[@id="raj"]/div[2]/div[2]/img')
    div_element.screenshot(r'Captcha-Solver/Captcha/unsolved.png')
    
    # Load image and set the bounds
    img = cv2.imread(r'Captcha-Solver/Captcha/unsolved.png')
    lower = (102, 102, 102)  # Lower bound for each channel
    upper = (125, 125, 125)  # Upper bound for each channel

    # Create the mask and use it to change the colors
    mask = cv2.inRange(img, lower, upper)
    img[mask != 0] = [0, 0, 0]

    # Save it
    cv2.imwrite(r'Captcha-Solver/Captcha/semisolved.png', img)

    img = Image.open(r'Captcha-Solver/Captcha/semisolved.png')  # Get image
    pixels = img.load()  # Create the pixel map

    for i in range(img.size[0]):  # For every pixel:
        for j in range(img.size[1]):
            if pixels[i, j] != (0, 0, 0):  # If not black:
                pixels[i, j] = (255, 255, 255)  # Change to white

    img.save(r'Captcha-Solver/Captcha/solved.png')

    # Read image
    img = cv2.imread(r'Captcha-Solver/Captcha/solved.png')

    # Configurations
    config = ('-l eng --oem 1 --psm 3')

    # Pytesseract
    text = pytesseract.image_to_string(img, config=config)

    # Print text
    tes_captcha = text.split('\n')[0]
    captcha = captcha_og()
    if len(captcha) < 6:
        return tes_captcha

    return captcha

print(f"Total USNs to be scraped: {end_usn - start_usn}")
prefix_usn = '1OX21CS'
def process_usn_range(start_usn, end_usn, count, error_count):
    for i in range(start_usn, end_usn + 1):
        USN = prefix_usn + str(i)
        print("Currently trying to grab the results of " + USN)
        repeat = True
        while repeat:
            # Configure webdriver options
            try:
                service = Service('/Users/admin/Documents/Github Repos/EduInsights-Project/Driver/chromedriver-mac-x64/chromedriver')
                options = webdriver.ChromeOptions()
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--headless')
                options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'

                # Launch browser
                driver = webdriver.Chrome(service=service, options=options)

                # Load url
                url = 'https://results.vtu.ac.in/JJEcbcs23/index.php'
                driver.get(url)
                time.sleep(1)

                captcha = solve_captcha(driver)

                time.sleep(2)

                if len(captcha) != 6:
                    refresh_button = driver.find_element('xpath', '/html/body/div[2]/div[1]/div[2]/div/div[2]/form/div/div[2]/div[2]/div[3]/p/a')
                    refresh_button.click()
                    time.sleep(1)
                    captcha = solve_captcha(driver)

                usn_text_field = driver.find_element('name', 'lns')
                usn_text_field.send_keys(USN)  # CHANGE THIS LATER ON FOR DEBUGGING
                captcha_text_field = driver.find_element('name', 'captchacode')
                captcha_text_field.send_keys(captcha)

                submit_button = driver.find_element('id', 'submit')
                submit_button.click()

                # Check if alert is present
                if EC.alert_is_present()(driver):
                    alert = driver.switch_to.alert
                    if alert.text == "University Seat Number is not available or Invalid..!":
                        alert.accept()
                        driver.quit()
                        repeat = False  # Proceed to next USN
                    elif alert.text == "Invalid captcha code !!!":
                        print("Invalid captcha code for " + USN)
                        count = count + 1
                        alert.accept()  # Dismiss the alert
                        driver.quit()  # Quit the driver without executing further lines for the current USN
                        repeat = False  # Proceed to next USN
                else:
                    # Wait for student name element
                    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/table/tbody/tr[1]/td[2]')))

                    stud_element = driver.find_element('xpath', '/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/table/tbody/tr[1]/td[2]')
                    print("Student Name: " + stud_element.text + " | USN: " + USN)
                    names.append(stud_element.text)
                    driver.quit()
                    repeat = False

            except WebDriverException as e:
                if "ERR_CONNECTION_TIMED_OUT" in str(e):
                    print("Connection timed out. Skipping USN: " + USN)
                    error_count = error_count + 1
                else:
                    # Handle other WebDriverExceptions if needed
                    print("WebDriverException:", e)
                repeat = False  # Stop repeating for this USN
    return count, error_count


count, error_count = process_usn_range(start_usn, end_usn, count, error_count)

# num_threads = 5
# 
# usn_range_size = (end_usn - start_usn) // num_threads
# thread_ranges = [(start_usn + i * usn_range_size, start_usn + (i + 1) * usn_range_size) for i in range(num_threads)]
# 
# # Create and start threads
# threads = []
# for usn_range in thread_ranges:
#     thread = threading.Thread(target=process_usn_range, args=usn_range)
#     threads.append(thread)
#     thread.start()
# 
# # wait for all threads to finish
# for thread in threads:
# 	thread.join()

print("Done!")
print("Total time taken: " + str(time.time() - start_time) + " seconds")    
print("Total number of USNs: " + str(end_usn - start_usn))
print("Total number of captcha errors: " + str(count))
print('Total number of connection timeouts: ' + str(error_count))
accuracy = ((end_usn - start_usn) - count - error_count) / (end_usn - start_usn) * 100
print("Accuracy: " + str(accuracy) + "%")
print(names)