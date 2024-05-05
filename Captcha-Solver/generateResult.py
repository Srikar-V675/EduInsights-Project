import threading
import time
import compute
import preprocessing
import smtplib
from email.message import EmailMessage
import driveSheetsOps
import authenticate
import pandas as pd

# initialise lock to ensure thread safety for results
lock = threading.Lock()
SCOPES = authenticate.SCOPES

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

def process_usn_range(thread_id, start_usn, end_usn, prefix_usn):
    """
    Process the USN range within a thread.

    Args:
        thread_id (int): The ID of the thread.
        start_usn (int): The starting USN number.
        end_usn (int): The ending USN number.
        prefix_usn (str): The prefix for the USNs.

    Returns:
        DataFrame: A DataFrame containing the processed results for the specified USN range.
    """
    # Process the USN range
    return preprocessing.processResults(thread_id, start_usn, end_usn, prefix_usn)

def process_thread(thread_id, start_usn, end_usn, prefix_usn, results):
    """
    Process a specific range of USNs within a thread.

    Args:
        thread_id (int): The ID of the thread.
        start_usn (int): The starting USN number.
        end_usn (int): The ending USN number.
        prefix_usn (str): The prefix for the USNs.
        results (list): A list to store the results from each thread.
    """
    # Process a specific range of USNs in a thread
    # Acquire the lock to ensure thread-safe access to the shared 'results' list
    # This prevents multiple threads from appending results simultaneously, avoiding data corruption
    result = process_usn_range(thread_id, start_usn, end_usn, prefix_usn)
    with lock:
        results.append(result)


def generate_student_result():
    """
    Generate student results by processing multiple threads.

    This function divides the specified range of USNs into chunks and assigns each chunk to a separate thread for processing.
    The results from each thread are then combined to generate overall student results. The function also writes the results
    to a Google Sheets spreadsheet and optionally sends the link to the spreadsheet via email.
    """
    start_usn = input('Enter the start USN number: ')
    end_usn = input('Enter the end USN number: ')
    prefix_usn = input('Enter the USN prefix: ')
    start_time = time.time()
    num_threads = 2

    # Divide the USN range into chunks for each thread
    usn_range_size = (int(end_usn) - int(start_usn)) // num_threads
    remainder = (int(end_usn) - int(start_usn)) % num_threads
    thread_ranges = [(int(start_usn) + i * usn_range_size, int(start_usn) + (i + 1) * usn_range_size) for i in range(num_threads)]
    thread_ranges[-1] = (thread_ranges[-1][0], thread_ranges[-1][1] + remainder)

    # Create a list to store the results from each thread
    results = []

    # Create and start threads
    threads = []
    for i, (start, end) in enumerate(thread_ranges):
        thread = threading.Thread(target=process_thread, args=(i, start, end, prefix_usn, results))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Combine results from all threads
    students_marks = pd.concat(results)
    print("Students Marks:")
    print(students_marks)

    # Extract top 10 students based on Percentage and SGPA
    top10 = students_marks.sort_values(by=[('Percentage', ''), ('SGPA', '')], ascending=False)[:10][[('Total', ''), ('Percentage', ''), ('SGPA', '')]]
    print("Top 10 Students:")
    print(top10)

    # Compute grades for all students
    grades = compute.grades(students_marks=students_marks)
    print("Grades:")
    print(grades)

    # Reset index for dataframes
    students_marks.reset_index(inplace=True)
    top10.reset_index(inplace=True)
    grades.reset_index(inplace=True)

    # Authenticate with Google Sheets API
    sheets = authenticate.sheetsAPI(SCOPES=SCOPES)

    # Create a new spreadsheet
    spreadsheetId = driveSheetsOps.create_new_spreadsheet(service=sheets)

    # Change access permission for the spreadsheet
    driveSheetsOps.change_access_permission(spreadsheetId=spreadsheetId)

    # Define starting rows for each dataframe in the spreadsheet
    start_rows = [2, len(students_marks) + 5, len(students_marks) + len(top10) + 10]

    # Prepare dataframes to be written to the spreadsheet
    dataframes = [students_marks, top10, grades]

    # Write dataframes to the spreadsheet
    driveSheetsOps.write_to_sheet(sheets, dataframes, start_rows, spreadsheetId)

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

    print(f"Time taken: {time.time() - start_time} seconds")


generate_student_result()
