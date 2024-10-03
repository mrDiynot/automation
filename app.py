import os
import subprocess
import time

import instaloader

L = instaloader.Instaloader()
count = 0
# Define your Instagram username
username = 'sahminvests'  # Replace with your Instagram username
session_file = 'my_session'  # Name of the session file

def download_instagram_video(post_url):
    global count
    if count == 0:
        L.load_session_from_file(username, session_file)
        count += 1    
    if not os.path.exists(session_file):

        if os.path.exists(session_file):
            try:
                L.load_session_from_file(username, session_file)
                print(f"Session loaded successfully for {username}")
            except Exception as e:
                print(f"Error loading session: {e}")
                return  # Exit if session loading fails
        else:
            print(f"Session file '{session_file}' not found. Please log in first.")
            return  # Exit if session file does not exist

    # Check if we are logged in
    # if not L.context.is_logged_in:
    #     print("Not logged in. Please log in first to create a session file.")
        return  # Exit if not logged in

    # Load the session from the file
    

    post_shortcode = post_url.split('/')[-2]  # Extract shortcode from URL
    
    while True:
        try:
            # Introduce a small delay to avoid rate limiting (optional, but helpful)
            time.sleep(3)

            # Fetch the post metadata
            post = instaloader.Post.from_shortcode(L.context, post_shortcode)

            # Check if the post is a video
            if post.is_video:
                # Download the post (this will save it in the 'videos' folder)
                L.download_post(post, target='videos')
                print("Video downloaded successfully.")
                break  # Exit loop after successful download
            else:
                print("The post is not a video.")
                break  # Exit if the post is not a video
        except instaloader.exceptions.ConnectionException as e:
            print(f"ConnectionException: {e}. Running login script and retrying in a few seconds...")
            subprocess.run(["python", "login.py"])  
            time.sleep(60) 
        except instaloader.exceptions.QueryReturnedNotFoundException as e:
            print(f"Post not found: {e}. Running login script and retrying in a few seconds...")
            subprocess.run(["python", "login.py"])  
            time.sleep(60) 
        except instaloader.exceptions.LoginRequiredException:
            print("Login required. Running login script.")
            subprocess.run(["python", "login.py"]) 
            time.sleep(60) 
        except Exception as e:
            print(f"An error occurred: {e}. Running login script and retrying in a few seconds...")
            subprocess.run(["python", "login.py"])  
            time.sleep(60) 
# Example usage
# post_url = 'https://www.instagram.com/p/CsrpvkVPcsN/'  # Replace with the actual post URL
# download_instagram_video(post_url)
