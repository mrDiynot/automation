import os
import time

import instaloader

L = instaloader.Instaloader()

# Define your Instagram username
username = 'sahminvests'  # Replace with your Instagram username
session_file = 'my_session'  # Name of the session file
def download_instagram_video(post_url):
    #

    # Load the session from the file
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
    if not L.context.is_logged_in:
        print("Not logged in. Please log in first to create a session file.")
        return  # Exit if not logged in

    try:
        # Extract the shortcode from the URL
        post_shortcode = post_url.split('/')[-2]
        
        # Introduce a small delay to avoid rate limiting (optional, but helpful)
        time.sleep(3)
        
        # Fetch the post metadata
        post = instaloader.Post.from_shortcode(L.context, post_shortcode)

        # Check if the post is a video
        if post.is_video:
            # Download the post (this will save it in the current working directory)
            L.download_post(post, target='videos')
         

        else:
            print("The post is not a video.")
    except instaloader.exceptions.ConnectionException as e:
        print(f"ConnectionException: {e}. You might be rate-limited, please wait a few minutes and try again.")
    except instaloader.exceptions.QueryReturnedNotFoundException as e:
        print(f"Post not found: {e}")
    except instaloader.exceptions.LoginRequiredException:
        print("Login required. Please check your login credentials.")
    except Exception as e:
        print(f"An error occurred: {e}")

# # Example usage
# post_url = 'https://www.instagram.com/p/CsrpvkVPcsN/'  # Replace with the actual post URL
# download_instagram_video(post_url)
