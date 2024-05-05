import os
import smtplib
from email.message import EmailMessage

import authenticate
import compute
import driveSheetsOps
import preprocessing

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
    password = os.getenv(
        "SMTP_GMAIL_CREDENTIALS"
    )  # Note: It's recommended to use environment variables or a secure method to store passwords.

    # Create the email message
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "VTU Extracted Results Link"
    message.set_content(
        f"""Dear Recipient,

    I am pleased to share with you the VTU results spreadsheet link. Please find it below:
    Access the spreadsheet: {spreadsheetLink}

    If you have any questions or concerns, feel free to reach out.

    Best Regards,
    Srikar V"""
    )

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
    students_marks = preprocessing.processResult()

    # Extract top 10 students based on Percentage and SGPA
    top10 = students_marks.sort_values(
        by=[("Percentage", ""), ("SGPA", "")], ascending=False
    )[:10][[("Total", ""), ("Percentage", ""), ("SGPA", "")]]

    # Compute grades for all students
    grades = compute.grades(students_marks=students_marks)

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
    start_rows = [
        2,
        len(students_marks) + 5,
        len(students_marks) + len(top10) + 10,
    ]

    # Prepare dataframes to be written to the spreadsheet
    dataframes = [students_marks, top10, grades]

    # Write dataframes to the spreadsheet
    driveSheetsOps.write_to_sheet(
        sheets, dataframes, start_rows, spreadsheetId
    )

    # Generate the link to the spreadsheet
    spreadsheet_link = (
        f"https://docs.google.com/spreadsheets/d/{spreadsheetId}"
    )

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

    # except Exception as e:
    #    print(f"An error occurred: {e}")


if __name__ == "__main__":
    generate_student_result()
