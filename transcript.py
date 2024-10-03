import os
import time

import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory

# Configure API key for Google Gemini
genai.configure(api_key="AIzaSyBkrM63b_gXRZ1pQ6CXmvc6Js0FkFyL6zI")

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active."""
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()

def process_video_files(folder_path):
    """Processes all MP4 files in the specified folder for OCR and transcription."""
    results = []

    # Get a list of all MP4 files in the folder
    mp4_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]

    # Create the model configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )

    # Process each MP4 file
    for file_name in mp4_files:
        file_path = os.path.join(folder_path, file_name)
        uploaded_file = upload_to_gemini(file_path)
        
        # Wait for the uploaded file to be ready
        wait_for_files_active([uploaded_file])

        # Start chat session
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        uploaded_file,
                    ],
                },
            ]
        )

        # Request OCR and transcript
        ocr_response = chat_session.send_message(
            """Please analyze the video for its subtitle text only. Ignore other visual assets and focus solely on extracting the words displayed in the subtitles. I need the extracted text to be highlighted for easy identification. Please ensure that the timing information is not included, just the pure text content of the subtitles in a single line."""
        )
        transcript_response = chat_session.send_message(
            """Please provide trasncript of the video."""
        )

        # Store the results
        results.append({
            "file": file_name,
            "ocr": ocr_response.text,
            "transcript": transcript_response.text,
        })

        print(f"Processed '{file_name}'")

    return results

# # Example usage
# folder_path = 'videos'  # Specify the folder containing MP4 files
# results = process_video_files(folder_path)

# # Print results
# for result in results:
#     print(f"File: {result['file']}")
#     print("OCR Text:", result['ocr'])
#     print("Transcript:", result['transcript'])
#     print("-------------------------------------------------------------------------------------------------------------")
