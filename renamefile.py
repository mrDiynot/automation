import os
def rename_mp4_files(folder_path):
    """
    Renames all MP4 files in the specified folder to a sequential format (video1.mp4, video2.mp4, etc.).
    Args:
        folder_path (str): The path to the folder containing the MP4 files.
    """

    mp4_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]


    for index, file in enumerate(mp4_files, start=1):

        new_name = f"video{index}.mp4"

        old_file_path = os.path.join(folder_path, file)
        new_file_path = os.path.join(folder_path, new_name)

        os.rename(old_file_path, new_file_path)
        print(f"Renamed '{old_file_path}' to '{new_file_path}'")

folder_path = 'videos' 
rename_mp4_files(folder_path)