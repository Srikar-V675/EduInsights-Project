import json
import time

import trueCaptcha
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# Function to solve captcha using trueCaptcha
def solve_captcha(USN, driver):
    """
    Solves the captcha on a webpage using an image-based captcha solver.

    Args:
        driver: WebDriver object representing the browser driver.

    Returns:
        str: The solved captcha string.

    Description:
        This function finds the captcha image element on the webpage, takes a screenshot
        of the captcha image, and then passes the image to the trueCaptcha solver to
        extract the captcha text. The solved captcha string is returned.
    """
    # Find the captcha image element on the webpage
    div_element = driver.find_element("xpath", '//*[@id="raj"]/div[2]/div[2]/img')

    # Take a screenshot of the captcha image
    div_element.screenshot(
        r"/Users/admin/Documents/Github Repos/EduInsights-Project/EduInsights/Captcha-Solver/captcha.png"
    )

    # Solve the captcha using the trueCaptcha solver
    captcha = trueCaptcha.solve_captcha(
        USN,
        "/Users/admin/Documents/Github Repos/EduInsights-Project/EduInsights/Captcha-Solver/captcha.png",
    )

    return captcha


def scrape_results(USN, driver):
    """
    Scrape the results of a student with the given USN.

    Args:
        USN (str): The University Seat Number (USN) of the student.
        driver: WebDriver object representing the browser driver.

    Returns:
        str: JSON string representing the student's details and marks.

    Description:
        This function navigates to the VTU results website, fills in the USN and captcha
        fields, submits the form, and retrieves the student's results if available. It
        handles cases such as invalid captcha codes and alerts indicating unavailable
        results. The student's details and marks are extracted, formatted into a dictionary,
        converted to a JSON string, and returned.
    """
    print("Currently trying to grab the results of " + USN)
    repeat = True
    while repeat:
        try:
            # Load URL
            url = "https://results.vtu.ac.in/DJcbcs24/index.php"
            driver.get(url)
            time.sleep(1)

            # Solve captcha
            captcha = solve_captcha(USN, driver)

            time.sleep(1)

            # Refresh captcha if length is not 6
            if len(captcha) != 6:
                refresh_button = driver.find_element(
                    "xpath",
                    "/html/body/div[2]/div[1]/div[2]/div/div[2]/form/div/div[2]/div[2]/div[3]/p/a",
                )
                refresh_button.click()
                time.sleep(1)
                captcha = solve_captcha(USN, driver)

            # Fill USN and captcha fields and submit
            usn_text_field = driver.find_element("name", "lns")
            usn_text_field.send_keys(USN)
            captcha_text_field = driver.find_element("name", "captchacode")
            captcha_text_field.send_keys(captcha)

            submit_button = driver.find_element("id", "submit")
            submit_button.click()

            # Check for alerts
            if EC.alert_is_present()(driver):
                alert = driver.switch_to.alert
                if (
                    alert.text
                    == "University Seat Number is not available or Invalid..!"
                ):
                    print(alert.text)
                    alert.accept()
                    student_data = None
                    repeat = False  # Proceed to next USN
                elif alert.text == "Invalid captcha code !!!":
                    print("Invalid captcha code for " + USN)
                    print("Reattempting for " + USN)
                    alert.accept()
                    student_data = scrape_results(USN, driver)
            else:
                # Wait for student details
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/table/tbody/tr[1]/td[2]",
                        )
                    )
                )

                # Extract student details and marks
                usn_element = driver.find_element(
                    "xpath",
                    "/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/table/tbody/tr[1]/td[2]",
                )
                stud_element = driver.find_element(
                    "xpath",
                    "/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/table/tbody/tr[2]/td[2]",
                )
                table_element = driver.find_element(
                    "xpath",
                    "/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div",
                )
                sub_elements = table_element.find_elements("xpath", "div")
                num_sub_elements = len(sub_elements)
                stud_text = stud_element.text
                usn_text = usn_element.text
                print("Student Name: " + stud_text + " | USN: " + usn_text.upper())

                # Extract marks for each subject
                marks_list = []
                for i in range(2, num_sub_elements + 1):
                    marks_data = []
                    for j in range(1, 7):
                        details = driver.find_element(
                            "xpath",
                            "/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div/div["
                            + str(i)
                            + "]/div["
                            + str(j)
                            + "]",
                        )
                        marks_data.append(details.text)
                    marks_details = {
                        "Subject Code": marks_data[0],
                        "Subject Name": marks_data[1],
                        "INT": marks_data[2],
                        "EXT": marks_data[3],
                        "TOT": marks_data[4],
                        "Result": marks_data[5],
                    }

                    marks_list.append(marks_details)

                marks_list.sort(key=lambda x: x["Subject Code"])

                # Construct student data dictionary
                student_data = {
                    "USN": usn_text.upper(),
                    "Name": stud_text.upper(),
                    "Marks": marks_list,
                }

                # Convert the dictionary to a JSON object
                student_data = json.dumps(student_data, indent=4)

                repeat = False

        except WebDriverException as e:
            if "ERR_CONNECTION_TIMED_OUT" in str(e):
                print("Connection timed out. Skipping USN: " + USN)
            else:
                # Handle other WebDriverExceptions if needed
                print("WebDriverException:", e)
            repeat = False  # Stop repeating for this USN

    return student_data


# driver = driver.initialise_driver()
# data = scrape_results('1OX22CS105', driver)
# print(data)
