import pandas as pd
import numpy as np
from tqdm import tqdm
import json

# calculate the SGPA
def SGPA(totals):
    """
    Compute the Semester Grade Point Average (SGPA) based on the total marks of subjects and their respective credits.

    Args:
        totals (list): A list of total marks obtained in each subject.

    Returns:
        float: The calculated SGPA.

    Description:
        This function calculates the Semester Grade Point Average (SGPA) based on the total marks obtained in each subject
        and their respective credits. It reads the credits associated with each subject from a JSON file. The JSON file
        is expected to contain an array of integers representing the credits for each subject in the same order as the
        subjects appear in the totals list. The function iterates over the total marks and corresponding credits to
        calculate the grade points for each subject. It then calculates the weighted sum of grade points and divides
        it by the total credits to obtain the SGPA.

        Note:
        - The JSON file should contain an array of integers representing the credits for each subject.
        - The number of credits in the JSON file should match the number of subjects in the totals list.
        - The function applies the following conversion from total marks to grade points:
          - 90 and above: 10 grade points
          - 80-89: 9 grade points
          - 70-79: 8 grade points
          - 60-69: 7 grade points
          - 50-59: 6 grade points
          - 40-49: 5 grade points
          - Below 40: No grade points (considered as failing grades)
    """
    sgpa = 0  # Initialize SGPA
    sum_credits = 0  # Initialize total credits
    
    # Read credits from JSON file
    filename = "credits.json"
    with open(filename, "r") as json_file:
        credits = json.load(json_file)
    
    # Iterate over total marks and credits simultaneously
    for total, credit in zip(totals, credits):
        sum_credits += credit  # Accumulate total credits
        
        # Determine grade points based on total marks
        if total >= 90:
            sgpa += (10 * credit)
        elif total >= 80:
            sgpa += (9 * credit)
        elif total >= 70:
            sgpa += (8 * credit)
        elif total >= 60:
            sgpa += (7 * credit)
        elif total >= 50:
            sgpa += (6 * credit)
        elif total >= 40:
            sgpa += (5 * credit)
        else:
            sgpa += 0  # No grade points for failing grades
    
    # Calculate SGPA by dividing total grade points by total credits
    sgpa = sgpa / sum_credits
    
    return sgpa


# calculating grades for each subject
def grades(students_marks):
    """
    Compute grades based on the marks obtained by students.

    Parameters:
        students_marks (DataFrame): A pandas DataFrame containing marks obtained by students.

    Returns:
        DataFrame: A pandas DataFrame containing the computed grades for each subject.

    """
    # Define the index for the DataFrame to store grade counts
    index = ['FCD', 'FC', 'SC', 'Fail', 'Absent', 'Total']
    
    # Initialize DataFrame to store grade counts
    pfa = pd.DataFrame()
    
    # List to store columns to drop from students_marks DataFrame
    cols = []
    
    # Loop over the columns of students_marks DataFrame to compute grades
    for i in tqdm(range(3, len(students_marks.columns) - 2, 4)):
        result = students_marks.columns[i]  # Get the column representing the result (e.g., Internal Marks)
        total = students_marks.columns[i - 1]  # Get the column representing the total marks
        
        # Initialize counters for different grades
        fcd = 0
        fc = 0
        sc = 0
        f = 0
        a = 0
        
        # Iterate over result and total marks to compute grades
        for res, tot in zip(students_marks[result], students_marks[total]):
            if res == 'P':  # If student passed
                if int(tot) >= 75:
                    fcd += 1  # First Class with Distinction
                elif int(tot) >= 60:
                    fc += 1  # First Class
                else:
                    sc += 1  # Second Class
            elif res == 'F':  # If student failed
                f += 1
            elif res == 'A':  # If student was absent
                a += 1
        
        # Count the total number of students for each grade
        count = len(students_marks[result])
        
        # If it's the first iteration, create the DataFrame pfa
        if i == 3:
            pfa = pd.DataFrame([[fcd], [fc], [sc], [f], [a], [count]], columns=[result[0]], index=index)
        else:
            # Otherwise, concatenate the counts to pfa DataFrame
            pfa = pd.concat([pfa, pd.DataFrame([fcd, fc, sc, f, a, count], index=index, columns=[result[0]])], axis=1)
        
        # Add the result column to the list of columns to drop
        cols.append(result)
    
    # Drop the result columns from the students_marks DataFrame
    students_marks.drop(cols, axis=1, inplace=True)
    
    # Add Total and Percentage columns to the pfa DataFrame
    pfa['Total'] = 0
    pfa['Percentage'] = 0.0
    
    # Compute total counts and percentage for each grade
    for index in pfa.index.tolist():
        nums = pfa.loc[index].tolist()[:-1]
        pfa.at[index, 'Total'] = sum(nums)
    
    for index in pfa.index.tolist():
        if index == 'Total':
            pfa.at[index, 'Percentage'] = 100.0
        else:
            total = pfa['Total'].loc[index]
            pfa.at[index, 'Percentage'] = (total / pfa['Total'].loc['Total']) * 100
    
    return pfa