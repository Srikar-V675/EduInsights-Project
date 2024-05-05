import io
import sys
import time

import authenticate
import fitz
import pandas as pd
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = authenticate.SCOPES


# extracting the pdf content from files list
def extractContent(file):
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
    drive = authenticate.driveAPI(SCOPES=SCOPES)

    # Create a BytesIO object to store PDF content
    pdf_content = io.BytesIO()

    try:
        # Retrieve the PDF file from Google Drive
        pdf = drive.files().get_media(fileId=file["id"])

        # Download the PDF content
        downloader = MediaIoBaseDownload(pdf_content, pdf)
        done = False

        while not done:
            status, done = downloader.next_chunk()
            sys.stdout.write(
                f"Extracting pdf {file['name']}...    Extracted 0%"
            )

            # Simulate progress bar
            for _ in range(10):
                time.sleep(0.1)
                dash = "-"
                sys.stdout.write(f"{dash}")
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
        details = [details[0][1][2:], details[1][1][2:]]

        marks = tables[1].extract()
        marks_df = pd.DataFrame(marks)

        # Clean the DataFrame and format columns
        marks_df = marks_df.map(
            lambda x: (x.replace("\n", " ") if isinstance(x, str) else x)
        )
        marks_df.columns = marks_df.iloc[0]
        marks_df.drop(0, inplace=True)
        marks_df.reset_index(drop=True, inplace=True)
        marks_df.drop(
            ["Subject Name", "Announced / Updated on"],
            axis=1,
            inplace=True,
        )

        return details, marks_df
    except HttpError as e:
        if e.resp.status == 404:
            print("Error: File not found...")
        elif e.resp.status == 403:
            print(
                "Error: Permission denied. You do not have access to this file..."
            )
        else:
            print(f"Error: {e}")
