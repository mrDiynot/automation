import os
import shutil


def delete_all_files_in_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        #Loop through all files and subdirectories in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                # If it is a file, remove it
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                # If it is a directory, remove it and its contents
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print(f"The folder {folder_path} does not exist.")

# Usage example
# folder_path = "videos"
# delete_all_files_in_folder(folder_path)