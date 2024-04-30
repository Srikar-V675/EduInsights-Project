from tqdm import tqdm
import authenticate
from googleapiclient.errors import HttpError

SCOPES = authenticate.SCOPES

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
    drive = authenticate.driveAPI(SCOPES=SCOPES)
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
    service = authenticate.driveAPI(SCOPES=SCOPES)
    
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