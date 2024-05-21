import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# defining credentials file path from environment variable
credentials_file_path = os.getenv("GOOGLE_API_CREDENTIALS")

# defining scopes for drive and sheets API
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


# authenticate drive API
def driveAPI(SCOPES):
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
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file_path, SCOPES
            )
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
def sheetsAPI(SCOPES):
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
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file_path, SCOPES
            )
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
