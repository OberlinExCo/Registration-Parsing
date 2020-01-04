from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload

class GoogleDrive:
    SCOPES = 'https://www.googleapis.com/auth/drive'

    def __init__(self):
        self.id = ''

        store = file.Storage('storage.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, store)
        self.drive_service = discovery.build('drive', 'v3', http=creds.authorize(Http()))
        print("Google Drive connection has been authenticated")

    def uploadCSV(self,filename):
        file_metadata = {'name': filename }
        media = MediaFileUpload(filename,
                                mimetype='text/csv')
        file = self.drive_service.files().create(body=file_metadata,
                                                    media_body=media,
                                                    fields='id').execute()
        self.id = file.get('id')
