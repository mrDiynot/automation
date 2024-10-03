import os

def get_mp4_file_paths(folder_path):
    """
    Retrieves the full file paths of all MP4 files in the specified folder.

    Args:
        folder_path (str): The path to the folder containing MP4 files.

    Returns:
        list: A list of full paths to the MP4 files.
    """
    mp4_file_paths = []
    
    # Check if the provided folder path exists
    if os.path.exists(folder_path):
        # Iterate through all files in the specified folder
        for file_name in os.listdir(folder_path):
            # Check if the file ends with .mp4
            if file_name.endswith('.mp4'):
                # Construct the full file path
                full_path = os.path.join(folder_path, file_name)
                mp4_file_paths.append(full_path)
    else:
        print(f"The folder '{folder_path}' does not exist.")

    return mp4_file_paths

# Example usage
folder_path = 'videos'  # Specify your folder path here
 
mp4_files = get_mp4_file_paths(folder_path)

# Print the retrieved MP4 file paths
for mp4_file in mp4_files:
    print(mp4_file)
                                                                                                                                 