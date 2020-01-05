from googleapiclient import discovery
from httplib2 import Http
from apiclient.http import MediaFileUpload

class GoogleDrive:
    SCOPES = 'https://www.googleapis.com/auth/drive'

    def __init__(self, creds):
        self.drive_service = discovery.build('drive', 'v3', credentials=creds)
        print("Google Drive connection has been authenticated")

    def uploadCSV(self,filename):
        file_metadata = {'name': filename }
        media = MediaFileUpload(filename,
                                mimetype='text/csv')
        file = self.drive_service.files().create(body=file_metadata,
                                                    media_body=media,
                                                    fields='id').execute()
        self.id = file.get('id')
