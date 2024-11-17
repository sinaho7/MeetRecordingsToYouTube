# MeetRecordingsToYouTube
Application for uploading Google meeting recordings to YouTube

## Project Overview

This project automates the process of polling Google Drive for new Google Meet recordings and uploading these recordings to YouTube. This system is designed to be deployed on Google Cloud to ensure scalability and reliability.

## System Components and Interactions

### Components

1. **Google Drive Polling Service**
    - Polls a specified Google Drive folder for new Google Meet recordings.
    - Uses Google Drive API to list and download files.

2. **Google Cloud Storage Service**
    - Uploads downloaded recordings from Google Drive to a GCS bucket.
    - Stores the recordings temporarily for further processing.

3. **YouTube Upload Service**
    - Uploads recordings from the GCS bucket to YouTube.
    - Uses YouTube Data API for uploading videos and managing playlists.

4. **Firestore Database**
    - Keeps track of the files that have been processed to avoid duplicates.
    - Uses Firestore to store metadata of processed recordings.

![APIs](https://github.com/sinaho7/MeetingRecordingsToYouTube/assets/164720452/95373064-12a7-45ba-ab26-4e6d6a36b866)

### Interactions

1. **Polling for New Recordings**
    - The system polls the specified Google Drive folder for new recordings that are not yet in the Firestore database.
    - New recordings are identified and downloaded to a temporary location.

2. **Uploading to Google Cloud Storage**
    - Recordings are uploaded to the GCS bucket.

3. **Uploading to YouTube**
    - The system fetches recordings from the GCS bucket.
    - Each recording is uploaded to YouTube with appropriate metadata (title, description).
    - After successful upload, the recordings are removed from the GCS bucket.
  
![Data Flow Diagram](https://github.com/sinaho7/MeetingRecordingsToYouTube/assets/164720452/e9ce2695-318a-40ec-87e5-387184f32dd8)


## Setup and Running the Application

### Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/meet-recordings-to-youtube.git
   cd meet-recordings-to-youtube
   
2. **Create and Activate a Virtual Environment**
   ```sh
   python -m venv myenv
   source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
  
3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
4. **Set Up Google Cloud Credentials**
    - Place the service_account.json file in the project directory.
    - Place the client_secrets.json file in the project directory for YouTube API authentication.

### Running the Application

   
1. **Run the Main.py**
   ```sh
   python main.py

### Backend Tools

1. **Python**
    - Chosen for its simplicity and extensive support for Google APIs.
    - Facilitates quick development and integration with various Google services.

2. **Google Drive API**
    - Used to access and download files from Google Drive.
    - Essential for polling and retrieving new Google Meet recordings.

3. **Google Cloud Storage**
    - Provides scalable and secure storage for temporary holding of recordings.
    - Ensures recordings are readily available for upload to YouTube.

4. **YouTube Data API**
    - Enables programmatic upload of videos to YouTube.
    - Allows for managing video metadata and playlist integration..

5. **Firestore**
    - Chosen for its real-time capabilities and ease of use with the rest of the Google Cloud ecosystem.
    - Ensures efficient tracking and management of processed recordings.
  
### Deploy Cloud Function

#### Deploy Using gcloud CLI:


1. Use the following command to deploy the function:

    ```sh
    gcloud functions deploy run_main_function \
    --runtime python39 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point main \
    --env-vars-file .env.yaml \
    --project YOUR_PROJECT_ID
## Step 4: Set Up Cloud Scheduler

#### Create a Cloud Scheduler Job:

1. Go to the Cloud Scheduler Console.

2. Click on "Create Job".

3. Configure the job:
   - Name: run-main-function
   - Frequency: */30 * * * * (every 30 minutes)
   - Timezone: Choose your preferred timezone
   - Target: HTTP
   - URL: https://REGION-PROJECT_ID.cloudfunctions.net/run_main_function
   - HTTP Method: POST
   - Body: {}

By following these steps, your project will be set up to run on Google Cloud as a service that executes main.py every 30 minutes, automating the process of downloading files from Google Drive, temporarily uploading them to Google Cloud Storage, and then uploading them to YouTube.

### Conclusion
This project leverages the power and flexibility of Google Cloud Platform services to automate the processing and uploading of Google Meet recordings to YouTube. The integration of these services ensures a robust, scalable, and efficient system suitable for deployment in production environments. By following the setup instructions, you can easily deploy and run this application in your own Google Cloud environment.


