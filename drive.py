from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

class GoogleDrive:
    SCOPES = 'https://www.googleapis.com/auth/drive'

    def __init__(self):
        store = file.Storage('storage.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, store)
        self.drive_service = discovery.build('drive', 'v3', http=creds.authorize(Http()))

    def uploadCSV(self,filename):
        file_metadata = {'name': filename }
        media = MediaFileUpload('files/photo.jpg',
                                mimetype='image/jpeg')
        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        return file.get('id')
