import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
from google.cloud import storage
import io
from googleapiclient.http import MediaIoBaseUpload  # Add this import

class UploadToYouTube:
    def __init__(self, client_secrets_file, token_pickle_file, bucket_name, playlist_id=None):
        self.client_secrets_file = client_secrets_file
        self.token_pickle_file = token_pickle_file
        self.bucket_name = bucket_name
        self.playlist_id = playlist_id
        self.youtube = self.get_authenticated_service()
        self.storage_client = self.authenticate_gcs()

    def get_authenticated_service(self):
        credentials = None

        if os.path.exists(self.token_pickle_file):
            with open(self.token_pickle_file, 'rb') as token:
                credentials = pickle.load(token)
        
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file, ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.upload"]
                )
                credentials = flow.run_local_server(port=8080, prompt='consent')

            with open(self.token_pickle_file, 'wb') as token:
                pickle.dump(credentials, token)
        
        return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    def authenticate_gcs(self):
        return storage.Client.from_service_account_json('service_account.json')

    def upload_video(self, file_name, title, description):
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(file_name)

        with io.BytesIO() as file_obj:
            blob.download_to_file(file_obj)
            file_obj.seek(0)
            media_body = MediaIoBaseUpload(file_obj, mimetype='video/mp4')

            request_body = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "categoryId": "22"
                },
                "status": {
                    "privacyStatus": "public"
                }
            }

            try:
                response = self.youtube.videos().insert(
                    part="snippet,status",
                    body=request_body,
                    media_body=media_body
                ).execute()

                video_id = response['id']
                print("Video uploaded successfully!")
                print("Video ID:", video_id)

                if self.playlist_id:
                    self.add_video_to_playlist(video_id)

                return video_id
            except googleapiclient.errors.HttpError as e:
                print("An error occurred while uploading the video:", e)
                return None

    def add_video_to_playlist(self, video_id):
        request = self.youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": self.playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        request.execute()
        print("Video added to playlist successfully!")

    def main(self):
        blobs = self.storage_client.list_blobs(self.bucket_name)
        for blob in blobs:
            file_name = blob.name
            title = os.path.splitext(file_name)[0]
            description = title
            self.upload_video(file_name, title, description)
        
        # Clear the bucket after uploading
        self.clear_bucket()

        print("All videos uploaded to YouTube from GCS.")

    def clear_bucket(self):
        bucket = self.storage_client.bucket(self.bucket_name)
        blobs = bucket.list_blobs()
        for blob in blobs:
            blob.delete()

if __name__ == "__main__":
    uploader = UploadToYouTube('client_secrets.json', 'TOKEN_PICKLE_FILE', 'BUCKET_NAME', playlist_id='YOUTUBE_PLAYLIST_ID')
    uploader.main()
