from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.cloud import firestore

class PollRecordings:
    def __init__(self, service_account_file, folder_id):
        self.service_account_file = service_account_file
        self.folder_id = folder_id
        self.drive_service = self.authenticate_drive()
        self.firestore_client = self.authenticate_firestore()

    def authenticate_drive(self):
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials = service_account.Credentials.from_service_account_file(self.service_account_file, scopes=scopes)
        return build('drive', 'v3', credentials=credentials)

    def authenticate_firestore(self):
        return firestore.Client.from_service_account_json(self.service_account_file)

    def poll_recordings(self):
        new_files = []
        results = self.drive_service.files().list(
            q=f"'{self.folder_id}' in parents",
            spaces='drive',
            fields="nextPageToken, files(id, name)"
        ).execute()
        items = results.get('files', [])
        for item in items:
            print(f'Found file: {item["name"]} ({item["id"]})')
            # Check if file exists in Firestore
            doc_ref = self.firestore_client.collection('firestore_collection').document(item["id"])
            if not doc_ref.get().exists:
                new_files.append(item)
                # Store the recording details in Firestore
                doc_ref.set({
                    'name': item['name'],
                    'id': item['id'],
                    'timestamp': firestore.SERVER_TIMESTAMP
                })
        return new_files

    def main(self):
        return self.poll_recordings()

if __name__ == "__main__":
    service_account_file = 'service_account.json'
    folder_id = 'FOLDER_ID'
    poller = PollRecordings(service_account_file, folder_id)
    poller.main()
