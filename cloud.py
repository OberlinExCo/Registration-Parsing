from googleapiclient import discovery
from httplib2 import Http

class GoogleScripts:
    def __init__(self,creds):
        self.script_service = discovery.build('cloud', 'v2', credentials=creds)
        print("Google Cloud Resource Manager connection has been authenticated")
