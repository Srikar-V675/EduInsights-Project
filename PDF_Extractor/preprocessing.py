import pandas as pd
from tqdm import tqdm
import pdf
import compute
import driveSheetsOps

# extract and process the PDF files
def processResult():
    """
    Extract and process student results from PDF files stored in a Google Drive folder.

    This function prompts the user to enter the link to a Google Drive folder containing PDF files of student results.
    It then extracts data from each PDF file, processes it, and returns a DataFrame containing student details and their results.

    Returns:
        DataFrame: A pandas DataFrame containing student details (USN and Name) and their respective marks and other result data.
                    The DataFrame is indexed by USN and Name.

    Raises:
        ValueError: An error occurred while processing the data.
    """
    # Prompt the user to enter the Google Drive folder link
    folder_link = input("Please enter the drive link: ")
    
    # Retrieve the list of files from the specified folder
    files = driveSheetsOps.files_list(folder_link)
    
    # Initialize DataFrames to store student details and marks
    details_df = pd.DataFrame(columns=['USN', 'Name'])
    students_marks = pd.DataFrame()
    
    # Process each file if files are found in the folder
    if files:
        for i in tqdm(range(len(files))):
            # Extract details and marks from the PDF file
            details, marks_df = pdf.extractContent(file=files[i])
            
            # Ignore students with no or one subject (likely dropped out)
            if len(marks_df) == 1 or len(marks_df) == 0:
                print(f"Ignoring {details[0]} because He/She has dropped out") 
                continue
            
            # Append student details to details DataFrame
            details_df.loc[i] = details
            
            # Initialize DataFrame to store marks if processing the first file
            if i == 0:
                subcodes = marks_df['Subject Code'].tolist()
                marks = ['INT', 'EXT', 'TOT', 'RESULT']
                cols = pd.MultiIndex.from_product([subcodes, marks])
                students_marks = pd.DataFrame(columns=cols)
                students_marks['Total'] = 0
                students_marks['Percentage'] = 0
                students_marks['SGPA'] = 0
                
                credits = []
                print("Please enter the credits:")
                for code in subcodes:
                    c = int(input(f"{code}:"))
                    credits.append(c)
            
            # Flatten and append marks to students_marks DataFrame
            values = []
            for mark in marks_df[['Internal Marks', 'External Marks', 'Total', 'Result']].values:
                for val in mark:
                    values.append(val)
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
            students_marks.at[i, 'SGPA'] = compute.SGPA(totals, credits)
        
        # Combine student details and marks DataFrames
        students_marks = pd.concat([details_df, students_marks], axis=1)
        
        # Set index to USN and Name
        students_marks = students_marks.set_index(['USN', 'Name'])
        
        print("Extraction Successful!!")
        return students_marks
    else:
        print("Warning: Folder empty or folder not found...")