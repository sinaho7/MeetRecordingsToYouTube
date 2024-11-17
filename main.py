from poll_recordings import PollRecordings
from download_from_drive import DownloadFromDrive
from upload_to_youtube import UploadToYouTube

if __name__ == "__main__":
    service_account_file = 'service_account.json'
    folder_id = 'FOLDER_ID'
    bucket_name = 'BUCKET_NAME'

    # Poll for new recordings
    poller = PollRecordings(service_account_file, folder_id)
    new_files = poller.main()

    if new_files:
        # Download new files and upload to GCS
        downloader = DownloadFromDrive(service_account_file, folder_id, bucket_name)
        downloader.main(new_files)

        # Upload to YouTube from GCS
        uploader = UploadToYouTube('client_secrets.json', 'TOKEN_PICKLE_FILE', bucket_name, playlist_id='YOUTUBE_PLAYLIST_ID')
        uploader.main()
