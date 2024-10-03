from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from get_file_path import get_mp4_file_paths


def upload_file_to_drive(file_path):
    """
    Uploads a file to Google Drive and makes it publicly accessible.

    Args:
        file_path (str): The path to the file to upload.

    Returns:
        str: The shareable link to the uploaded file.
    """
    # Step 1: Authenticate using Service Account
    gauth = GoogleAuth()
    
    # Load the service account credentials
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'automation-437411-d6b82e440cdc.json',  # Replace with your service account key file
        ['https://www.googleapis.com/auth/drive']
    )

    drive = GoogleDrive(gauth)

    # Step 2: Upload File to Google Drive
    file_name = file_path.split('\\')[-1]  # Get just the file name
    file = drive.CreateFile({'title': file_name})
    file.SetContentFile(file_path)
    file.Upload()  # Upload the file


    file.InsertPermission({
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader'
    })

    # Step 4: Get the shareable link
    shareable_link = file['alternateLink']
    return shareable_link

# Example usage
folder_path = 'videos'  # Specify your folder path here
mp4_files = get_mp4_file_paths(folder_path)  # This returns a list of file paths
print(mp4_files)
# Upload each file and print the shareable link
# for file_path in mp4_files:
#     link = upload_file_to_drive(file_path)
#     print(f"Your file '{file_path}' has been uploaded. Shareable link: {link}")