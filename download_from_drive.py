import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.cloud import storage
from googleapiclient.http import MediaIoBaseDownload
import io

class DownloadFromDrive:
    def __init__(self, service_account_file, folder_id, bucket_name):
        self.service_account_file = service_account_file
        self.folder_id = folder_id
        self.bucket_name = bucket_name
        self.drive_service = self.authenticate_drive()
        self.storage_client = self.authenticate_gcs()

    def authenticate_drive(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.service_account_file,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        return build('drive', 'v3', credentials=credentials)

    def authenticate_gcs(self):
        return storage.Client.from_service_account_json(self.service_account_file)

    def download_and_upload_to_gcs(self, file_id, file_name):
        request = self.drive_service.files().get_media(fileId=file_id)
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        
        with io.BytesIO() as file_obj:
            downloader = MediaIoBaseDownload(file_obj, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.")
            file_obj.seek(0)
            blob.upload_from_file(file_obj)
            print(f"File {file_name} uploaded to {self.bucket_name}.")

    def main(self, new_files):
        for file in new_files:
            file_id = file['id']
            file_name = file['name']
            self.download_and_upload_to_gcs(file_id, file_name)
        print('All files uploaded to GCS.')

if __name__ == '__main__':
    new_files = [...]  # Pass the new_files list from poll_recordings.py
    downloader = DownloadFromDrive('service_account.json', 'FOLDER_ID', 'BUCKET_NAME')
    downloader.main(new_files)
