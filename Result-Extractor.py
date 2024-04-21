# importing libraries
import os
import io
import sys
import time
import smtplib
import fitz
from email.message import EmailMessage
import pandas as pd
from tqdm import tqdm
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# Authentication functions

# defining scopes for drive and sheets API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]

# authenticate drive API
def authenticate_driveAPI(SCOPES):
    """
    Authenticate with Google Drive API.

    Parameters:
        SCOPES (list): A list of OAuth 2.0 scopes defining the level of access to Google Drive resources.

    Returns:
        Resource: An authenticated Google Drive service object.

    Raises:
        HttpError: An error occurred while attempting to authenticate or build the service.
    """
    credentials = None

    # Check if token file exists
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", scopes=SCOPES)

    # If credentials are not valid or do not exist, perform authentication
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            # Refresh the expired credentials
            credentials.refresh(Request())
        else:
            # Perform OAuth 2.0 authentication
            flow = InstalledAppFlow.from_client_secrets_file("/Users/admin/Documents/Credentials/Google Sheets/OAuth-Credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        
        # Save the refreshed or newly acquired credentials to token file
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    
    try:
        # Build the Google Drive service
        drive_service = build("drive", "v3", credentials=credentials)
        
        return drive_service
    except HttpError as error:
        # Handle any HTTP errors
        print(error)


# Authenticate sheets API
def authenticate_sheetsAPI(SCOPES):
    """
    Authenticate with Google Sheets API.

    Parameters:
        SCOPES (list): A list of OAuth 2.0 scopes defining the level of access to Google Sheets resources.

    Returns:
        Resource: An authenticated Google Sheets service object.

    Raises:
        HttpError: An error occurred while attempting to authenticate or build the service.
    """
    credentials = None

    # Check if token file exists
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", scopes=SCOPES)

    # If credentials are not valid or do not exist, perform authentication
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            # Refresh the expired credentials
            credentials.refresh(Request())
        else:
            # Perform OAuth 2.0 authentication
            flow = InstalledAppFlow.from_client_secrets_file("/Users/admin/Documents/Credentials/Google Sheets/OAuth-Credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        
        # Save the refreshed or newly acquired credentials to token file
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    
    try:
        # Build the Google Sheets service
        sheets_service = build("sheets", "v4", credentials=credentials)
        
        return sheets_service
    except HttpError as error:
        # Handle any HTTP errors
        print(error)


# function calls

# retrieve files list in drive link
def files_list(folder_link):
    """
    Retrieve a list of files within a specific folder in Google Drive.

    Parameters:
        folder_link (str): The link to the Google Drive folder.

    Returns:
        list: A list of dictionaries containing file metadata (id and name) for files within the specified folder,
              or None if no files are found in the folder.

    Raises:
        HttpError: An error occurred while attempting to retrieve the files list.
    """
    drive = authenticate_driveAPI(SCOPES=SCOPES)
    folder_id = folder_link.split("/")[-1:][0]
    print("Fetching list of files...")
    try:
        response = drive.files().list(
                q=f"'{folder_id}' in parents",
                orderBy='name',
                fields="files(id, name)").execute()
        files_list = response.get("files", [])
        if not files_list:
            print("Warning: No Files in the Folder...")
        else:
            print("Files (id,name) fetched succesfully!!")
            return files_list
    except HttpError as e:
        if e.resp.status == 404:
            print("Error 404: Folder not found...")
        else:
            print(f"Error: {e}")


# extracting the pdf content from files list
def extract_pdf_content(file):
    """
    Extract content from a PDF file stored in Google Drive.

    This function retrieves the content from a PDF file and processes it to extract relevant information.

    Parameters:
        file (dict): A dictionary containing metadata of the PDF file, including its ID.

    Returns:
        tuple: A tuple containing details extracted from the PDF (student details) and a DataFrame
               containing marks or other tabular data extracted from the PDF.
        tuple[0] (dict): A dictionary containing student details extracted from the PDF.
        tuple[1] (DataFrame): A pandas DataFrame containing marks or other tabular data extracted from the PDF.

    Raises:
        HttpError: An error occurred while attempting to extract content from the PDF file.
    """
    # Authenticate with Google Drive API
    drive = authenticate_driveAPI(SCOPES=SCOPES)
    
    # Create a BytesIO object to store PDF content
    pdf_content = io.BytesIO()
    
    try:
        # Retrieve the PDF file from Google Drive
        pdf = drive.files().get_media(fileId=file['id'])
        
        # Download the PDF content
        downloader = MediaIoBaseDownload(pdf_content, pdf)
        done = False
        
        while not done:
            status, done = downloader.next_chunk()
            sys.stdout.write(f"Extracting pdf {file['name']}...    Extracted 0%")
            
            # Simulate progress bar
            for i in range(10):
                time.sleep(0.1)
                dash = '-'
                sys.stdout.write(f'{dash}')
                sys.stdout.flush()
            
            if done:
                sys.stdout.write(f"{int(status.progress() * 100)}%\n")
                sys.stdout.flush()
        
        # Reset the pointer to the beginning of the BytesIO object
        pdf_content.seek(0)
        
        # Open the PDF document using PyMuPDF (fitz)
        pdf_doc = fitz.open(stream=pdf_content)
        page = pdf_doc[0]
        
        # Find tables in the PDF page
        tables = page.find_tables()
        
        # Extract details and marks from the tables
        details = tables[0].extract()
        details = [details[0][1][2:],details[1][1][2:]]
        
        marks = tables[1].extract()
        marks_df = pd.DataFrame(marks)
        
        # Clean the DataFrame and format columns
        marks_df = marks_df.applymap(lambda x: x.replace("\n", " ") if isinstance(x, str) else x)
        marks_df.columns = marks_df.iloc[0]
        marks_df.drop(0, inplace=True)
        marks_df.reset_index(drop=True, inplace=True)
        marks_df.drop(['Subject Name', 'Announced / Updated on'], axis=1, inplace=True)
        
        return details, marks_df
    except HttpError as e:
        if e.resp.status == 404:
            print("Error: File not found...")
        elif e.resp.status == 403:
            print("Error: Permission denied. You do not have access to this file...")
        else:
            print(f"Error: {e}")


# extract and process the PDF files
def extract_process_student_result():
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
    files = files_list(folder_link)
    
    # Initialize DataFrames to store student details and marks
    details_df = pd.DataFrame(columns=['USN', 'Name'])
    students_marks = pd.DataFrame()
    
    # Process each file if files are found in the folder
    if files:
        for i in tqdm(range(len(files))):
            # Extract details and marks from the PDF file
            details, marks_df = extract_pdf_content(file=files[i])
            
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
            students_marks.at[i, 'SGPA'] = compute_SGPA(totals, credits)
        
        # Combine student details and marks DataFrames
        students_marks = pd.concat([details_df, students_marks], axis=1)
        
        # Set index to USN and Name
        students_marks = students_marks.set_index(['USN', 'Name'])
        
        print("Extraction Successful!!")
        return students_marks
    else:
        print("Warning: Folder empty or folder not found...")


# calculate the SGPA
def compute_SGPA(totals, credits):
    """
    Compute the Semester Grade Point Average (SGPA) based on the total marks and credits of subjects.

    Parameters:
        totals (list): A list of total marks obtained in each subject.
        credits (list): A list of credits associated with each subject.

    Returns:
        float: The calculated SGPA.

    """
    sgpa = 0  # Initialize SGPA
    sum_credits = 0  # Initialize total credits
    
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
def compute_grades(students_marks):
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


# create a new spreadsheet from title
def create_new_spreadsheet(service):
    """
    Create a new Google Sheets spreadsheet.

    This function prompts the user to enter the title for the new spreadsheet,
    creates the spreadsheet with the specified title, and returns its ID.

    Parameters:
        service: An authenticated Google Sheets service object.

    Returns:
        str: The ID of the newly created spreadsheet.

    """
    try:
        # Prompt the user to enter the title of the new spreadsheet
        sheetName = input("Please enter the title of the new spreadsheet: ")
        
        # Define the properties of the new spreadsheet
        spreadsheet = {
            'properties': {'title': sheetName}
        }
        
        # Create the new spreadsheet
        spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        
        # Print confirmation message
        print(f"Successfully created spreadsheet - {sheetName}")
        
        # Return the ID of the newly created spreadsheet
        return spreadsheet['spreadsheetId']
    
    except HttpError as e:
        # Handle HTTP errors
        print(f"Error: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected Error: {e}")


# change access permission of spreadsheet
def change_access_permission(spreadsheetId):
    """
    Change access permissions for a Google Sheets spreadsheet.

    This function changes the access permissions for the specified spreadsheet
    to allow anyone with the link to edit it.

    Parameters:
        spreadsheetId (str): The ID of the Google Sheets spreadsheet.

    """
    # Authenticate with Google Drive API
    service = authenticate_driveAPI(SCOPES=SCOPES)
    
    try:
        # Define permissions for the spreadsheet
        permissions = {
            'type': 'anyone',  # Allow anyone with the link
            'role': 'writer'   # Grant write access
        }
        
        # Update permissions for the spreadsheet
        service.permissions().create(fileId=spreadsheetId, body=permissions).execute()
        
        # Print confirmation message
        print("Spreadsheet permissions updated: anyone with link can edit...")
    
    except HttpError as e:
        # Handle HTTP errors
        print(f"Error: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected Error: {e}")


# write the dataframes to the spreadsheet
def write_to_sheet(service, dataframes, start_rows, spreadsheetId):
    """
    Write data from DataFrame(s) to a Google Sheets spreadsheet.

    This function takes a list of DataFrames, their starting rows, and the spreadsheet ID.
    It writes the data from each DataFrame to the spreadsheet, starting from the specified rows.

    Parameters:
        service: An authenticated Google Sheets service object.
        dataframes (list): A list of pandas DataFrames containing the data to be written.
        start_rows (list): A list of starting rows for each DataFrame in the spreadsheet.
        spreadsheetId (str): The ID of the Google Sheets spreadsheet.

    """
    try:
        print("Writing dataframes to spreadsheet...")
        
        # Loop through each DataFrame
        for i in tqdm(range(len(dataframes))):
            data = dataframes[i].values.tolist()  # Convert DataFrame to list of lists
            
            # Rename columns if it's the second DataFrame
            if i == 1:
                dataframes[i].columns = [''.join(map(str, col)) for col in dataframes[i].columns]
            
            cols = []
            subs = []
            
            # Extract headers for the first DataFrame
            if i == 0:
                print(dataframes[i])
                columnss = dataframes[i].columns.to_list()
                for j in range(len(columnss)):
                    # Separate main and sub columns for the first DataFrame
                    if j < 2:
                        cols.append(columnss[j])
                    elif j > (len(columnss) - 4):
                        cols.append(columnss[j][0])
                    else:
                        cols.append(columnss[j][1])
                        subs.append(columnss[j][0])
                
                # Write sub-headers for the first DataFrame
                body = {"values": [subs]}
                service.spreadsheets().values().update(spreadsheetId=spreadsheetId,
                                                       range=f"C1",
                                                       valueInputOption="RAW",
                                                       body=body).execute()
            
            # Extract headers for subsequent DataFrames
            if i != 0:
                headers = [dataframes[i].columns.tolist()]
            else:
                headers = [cols]
            
            # Write headers to the spreadsheet
            body = {"values": headers}
            service.spreadsheets().values().update(spreadsheetId=spreadsheetId,
                                                   range=f"A{start_rows[i]}",
                                                   valueInputOption="RAW",
                                                   body=body).execute()
            
            # Write data to the spreadsheet
            body = {"values": data}
            service.spreadsheets().values().update(spreadsheetId=spreadsheetId,
                                                   range=f"A{start_rows[i] + 1}",
                                                   valueInputOption="RAW",
                                                   body=body).execute()
        
        print("Writing Completed!!")
    
    except HttpError as e:
        # Handle HTTP errors
        print(f"Error: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected Error: {e}")


# send email
def send_email(receiver_email, spreadsheetLink):
    """
    Send an email with the VTU results spreadsheet link.

    This function sends an email to the specified recipient with a link to the VTU results spreadsheet.

    Parameters:
        receiver_email (str): The email address of the recipient.
        spreadsheetLink (str): The link to the VTU results spreadsheet.

    """
    print("Preparing to send mail...")
    
    sender_email = "srikarvuchiha@gmail.com"
    password = "glhy xvwc uaxs rstn"  # Note: It's recommended to use environment variables or a secure method to store passwords.
    
    # Create the email message
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "VTU Extracted Results Link"
    message.set_content(f"""Dear Recipient,
        
    I am pleased to share with you the VTU results spreadsheet link. Please find it below:
    Access the spreadsheet: {spreadsheetLink}
        
    If you have any questions or concerns, feel free to reach out.
    
    Best Regards,
    Srikar V""")
    
    print("Connecting to server...")
    
    # Connect to the SMTP server and send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)

    print("Email sent successfully!!")


# main function that calls all the other functions to execute the program
def generate_student_result():
    """
    Generate and distribute student result data.

    This function orchestrates the entire process of generating student result data,
    creating a Google Sheets spreadsheet, populating it with data, and optionally sending
    an email with the spreadsheet link to a recipient.

    """
    
    # Extract and process student result data
    students_marks = extract_process_student_result()
    
    # Extract top 10 students based on Percentage and SGPA
    top10 = students_marks.sort_values(by=[('Percentage', ''), ('SGPA', '')], ascending=False)[:10][[('Total', ''), ('Percentage', ''), ('SGPA', '')]]
    
    # Compute grades for all students
    grades = compute_grades(students_marks=students_marks)
    
    # Reset index for dataframes
    students_marks.reset_index(inplace=True)
    top10.reset_index(inplace=True)
    grades.reset_index(inplace=True)
    
    # Authenticate with Google Sheets API
    sheets = authenticate_sheetsAPI(SCOPES=SCOPES)
    
    # Create a new spreadsheet
    spreadsheetId = create_new_spreadsheet(service=sheets)
    
    # Change access permission for the spreadsheet
    change_access_permission(spreadsheetId=spreadsheetId)
    
    # Define starting rows for each dataframe in the spreadsheet
    start_rows = [2, len(students_marks) + 5, len(students_marks) + len(top10) + 10]
    
    # Prepare dataframes to be written to the spreadsheet
    dataframes = [students_marks, top10, grades]
    
    # Write dataframes to the spreadsheet
    write_to_sheet(sheets, dataframes, start_rows, spreadsheetId)
    
    # Generate the link to the spreadsheet
    spreadsheet_link = f"https://docs.google.com/spreadsheets/d/{spreadsheetId}"
    
    # Print the link to the spreadsheet
    print(f"You can access the spreadsheet here: {spreadsheet_link}")
    
    # Prompt user if they want to receive the link through mail
    print("Do you want to receive the link through email?")
    mail = int(input("Yes: 1 or No: 0: "))
    
    # If user chooses to receive the link through email
    if mail == 1:
        receiver_email = input("Please enter your email id: ")
        send_email(receiver_email, spreadsheet_link)
        print("Thank you! The link has been sent to your email.")
    else:
        print("Thank you!")
    
    #except Exception as e:
    #    print(f"An error occurred: {e}")


if __name__ == "__main__":
    generate_student_result()
