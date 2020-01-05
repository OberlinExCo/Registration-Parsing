from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload

class GoogleScripts:
    def __init__(self):
        store = file.Storage('storage.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, store)
        self.script_service = discovery.build('script', 'v1', http=creds.authorize(Http()))
        print("Google Script connection has been authenticated")

    
