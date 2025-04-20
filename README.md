# YouTube Video Upload Automation Script

## Goal
This script automates the process of uploading videos to YouTube from a specified directory. It authenticates the user via OAuth2, allows uploading of video files in `.mp4`, `.mov`, `.avi`, `.mkv` formats, and sets metadata such as title and description.

## Setup Instructions

### Step 1: Set up the Google Cloud Project

1. **Create a new Google Cloud Project**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Click on the **project drop-down** in the top navigation and select **New Project**.
   - Name your project (e.g., `YouTube Video Upload Script`), and click **Create**.

2. **Enable the YouTube Data API**:
   - In the **Google Cloud Console**, navigate to **APIs & Services > Library**.
   - Search for **YouTube Data API v3**.
   - Select it and click **Enable**.

### Step 2: Set up OAuth 2.0 Credentials

1. **Create OAuth 2.0 Credentials**:
   - In the **Google Cloud Console**, go to **APIs & Services > Credentials**.
   - Click **Create Credentials** and choose **OAuth 2.0 Client IDs**.
   - Select **Web application** for the application type.
   - Under **Authorized redirect URIs**, add `http://localhost:8080/`.
   - Save the credentials, and **download the JSON file**. This is your `credentials.json`.

2. **Save the credentials file**:
   - Rename the downloaded JSON file to `credentials.json` and place it in the root of the project directory.
  
3. **Add test user**:
   - Add test user from the **Audience** Section
  
4. **Add allowed scopes**:
   - Add 'https://www.googleapis.com/auth/youtube.upload' to allowed scope from **Data Access**
