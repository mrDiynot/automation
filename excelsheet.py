import logging
import os
import shutil
import time
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

from app import download_instagram_video
from delete import delete_all_files_in_folder
from get_file_path import get_mp4_file_paths
from google_link_share import upload_file_to_drive
from renamefile import rename_mp4_files
from transcript import process_video_files

folder_path = "videos"
delete_all_files_in_folder(folder_path)


time.sleep(2)


# Log file name
log_file = 'execution_log.txt'

# Set up logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to log script execution
def log_execution():
    # Log the current execution time
    logging.info("----------%Script Executed%----------")

    # Read the current log file
    with open(log_file, 'r') as f:
        lines = f.readlines()

    # Reverse the log file contents
    with open(log_file, 'w') as f:
        f.writelines(reversed(lines))

# Add the log_execution call wherever needed in your script to log and reverse the log file
log_execution()




# Define the scope (Google Sheets API and Google Drive API)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Load credentials from the JSON file
credentials = Credentials.from_service_account_file(
    'automation-437411-d6b82e440cdc.json', 
    scopes=SCOPES
)

# Authorize the API connection
gc = gspread.authorize(credentials)

try:
    # Try opening the Google Sheet by title
    spreadsheet = gc.open('Automation')
    
    # Select the first worksheet
    worksheet = spreadsheet.sheet1
    
    # Fetch all data from the sheet
    data = worksheet.get_all_values()
    
    # Extract the URLs from the first column (ignoring the header row)
    urls = [row[0] for row in data[1:]]  
    print("Extracted URLs:", urls)

    
    
    for index, url in enumerate(urls):
        url = url + '/'
        download_instagram_video(url)
        folder_path = 'videos' 
 

        file_path=get_mp4_file_paths(folder_path)
        print(".............................working...............................")


        link=upload_file_to_drive(file_path[0])
        
        print(link)
        
        worksheet.update_cell(index+2, 11, link)  # Column 10 for OC
      
        
        results = process_video_files(folder_path)



        ocr_text = results[0].get('ocr', 'No OCR text')

        transcript_text =results[0].get('transcript', 'No transcript text')
        worksheet.update_cell(index+2, 9,ocr_text)
        worksheet.update_cell(index+2, 10, transcript_text )

        folder_path = "videos"
        delete_all_files_in_folder(folder_path)
        # for entry in results:
        #     ocr_text = entry.get('ocr', 'No OCR text')
        #     transcript_text = entry.get('transcript', 'No transcript text')
        #     worksheet.update_cell(index+2, 9,ocr_text)
        #     worksheet.update_cell(index+2, 10, transcript_text )
    
      
        # for index, result in enumerate(results):
        #     row_index = index + 2  # Start from row 2 to avoid overwriting the header
        #   
        
        
    print("Results written to Google Sheet.")

except gspread.SpreadsheetNotFound:
    print("The Google Sheet could not be found. Please check the title or ensure the sheet is shared with the service account.")
except Exception as e:
    print(f"An error occurred: {e}")
