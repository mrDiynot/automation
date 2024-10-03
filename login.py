import os
import instaloader

# Replace this with the file path you want to delete
file_path = "my_session"

try:
    # Check if file exists
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        print(f"{file_path} has been deleted successfully.")
    else:
        print(f"The file {file_path} does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")

L = instaloader.Instaloader()
username = 'sahminvests'  
password = 'dumju1-cyjvyb-gybJin'
session_file = 'my_session' 
if os.path.exists(session_file):
    L.load_session_from_file(username, session_file)


if not L.context.is_logged_in:

    try:

        L.login(username, password)

        L.save_session_to_file(session_file)
        print("Login successful and session saved.")

    except instaloader.exceptions.BadCredentialsException:
        print("Login error: Wrong username or password.")

    except instaloader.exceptions.ConnectionException as e:
        print(f"Connection error: {e}")

    except Exception as e:
        print(f"An error occurred during login: {e}")

else:
    print("Already logged in.")