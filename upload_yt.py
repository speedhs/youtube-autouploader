import os
import pickle
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Get paths from environment variables
TOKEN_PATH = os.getenv('TOKEN_PATH', 'token.pickle')
CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH', 'credentials.json')
DIRECTORY_PATH = os.getenv('DIRECTORY_PATH', 'kspqyvideos')

# Authenticate and construct the YouTube service
def authenticate_youtube():
    creds = None

    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                logger.error(f'Credentials file {CREDENTIALS_PATH} not found.')
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=8080)
        
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('youtube', 'v3', credentials=creds)

# Upload a single video
def upload_video(youtube, file_path, title, description, category_id='22', privacy_status='public'):
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                logger.info(f"Upload progress: {int(status.progress() * 100)}%")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return
    logger.info(f"Upload complete. Video ID: {response.get('id')}")

# Iterate over files in a directory and upload
def upload_videos_from_directory(directory_path):
    youtube = authenticate_youtube()
    if not youtube:
        logger.error("YouTube authentication failed.")
        return

    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            file_path = os.path.join(directory_path, filename)
            title = os.path.splitext(filename)[0]
            description = f"Uploaded from {directory_path}"
            logger.info(f"Uploading: {title}")
            upload_video(youtube, file_path, title, description)

# Example usage
if __name__ == '__main__':
    if os.path.exists(DIRECTORY_PATH):
        upload_videos_from_directory(DIRECTORY_PATH)
    else:
        logger.error(f"Directory {DIRECTORY_PATH} does not exist.")
