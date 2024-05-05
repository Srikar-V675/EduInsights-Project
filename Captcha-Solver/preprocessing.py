import json
import pandas as pd
import compute
import scraper
from driver import initialise_driver

def processResults(thread_id, start_usn, end_usn, prefix_usn):
    """
    Process the results for a range of USNs.

    Args:
        thread_id (int): The ID of the current thread.
        start_usn (int): The starting USN of the range.
        end_usn (int): The ending USN of the range.
        prefix_usn (str): The prefix for USNs.

    Returns:
        pd.DataFrame: DataFrame containing student details and marks.

    Description:
        This function processes the results for a range of USNs. It iterates over each USN
        in the range, scrapes the results using the `scrape_results` function, and stores
        the details and marks in DataFrames. The function calculates total marks, percentage,
        and SGPA for each student and combines the details and marks DataFrames. Finally, it
        sets the index to USN and Name and returns the combined DataFrame.
    """
    # Initialize WebDriver and DataFrames
    driver = initialise_driver()
    details_df = pd.DataFrame(columns=['USN', 'Name'])
    students_marks = pd.DataFrame()

    i = 0
    for usn in range(start_usn, end_usn + 1):
        if usn > 0 and usn < 10:
            usn = '00' + str(usn)
        elif usn > 9 and usn < 100:
            usn = '0' + str(usn)
        USN = prefix_usn + usn

        # Scrape student details and marks
        student_details = scraper.scrape_results(USN, driver)
        student_details = json.loads(student_details)

        details = [student_details['USN'], student_details['Name']]
        sub_marks = student_details['Marks']

        # Ignore if only one or no subjects are present
        if len(sub_marks) == 1 or len(sub_marks) == 0:
            print(f"Ignoring {details[0]} because He/She must have dropped out")
            continue

        details_df.loc[i] = details

        # Initialize DataFrame to store marks if processing the first USN
        if i == 0:
            subcodes = [mark['Subject Code'] for mark in sub_marks]
            marks = ['INT', 'EXT', 'TOT', 'RESULT']
            cols = pd.MultiIndex.from_product([subcodes, marks])
            students_marks = pd.DataFrame(columns=cols)
            students_marks['Total'] = 0
            students_marks['Percentage'] = 0
            students_marks['SGPA'] = 0

        # Flatten and append marks to student_marks DataFrame
        values = []
        for mark in sub_marks:
            values.append(mark['INT'])
            values.append(mark['EXT'])
            values.append(mark['TOT'])
            values.append(mark['Result'])
        values.append('0')
        values.append('0')
        values.append('0')
        students_marks.loc[i] = values

        # Calculate total marks, percentage, and SGPA for each student
        total = 0
        totals = []
        for code in subcodes:
            totals.append(int(students_marks.loc[i][code]['TOT']))
            total += int(students_marks.loc[i][code]['TOT'])
        students_marks.at[i, 'Total'] = total
        students_marks.at[i, 'Percentage'] = total / len(subcodes)

        # Calculate SGPA using function compute_SGPA
        students_marks.at[i, 'SGPA'] = compute.SGPA(totals)

        i += 1

    # Combine student details and marks DataFrames
    students_marks = pd.concat([details_df, students_marks], axis=1)

    # Set index to USN and Name
    students_marks = students_marks.set_index(['USN', 'Name'])

    # Quit WebDriver
    driver.quit()

    return students_marks
