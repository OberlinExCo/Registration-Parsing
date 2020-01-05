from googleapiclient import discovery
from httplib2 import Http

class GoogleScripts:
    SCOPES = 'https://www.googleapis.com/auth/script.projects'

    def __init__(self,creds):
        self.script_service = discovery.build('script', 'v1', credentials=creds)
        print("Google Script connection has been authenticated")

    def createProject(self,title,parentId):
        body = {
            'title' : title,
            'parentId' : parentId
        }
        request = self.script_service.projects().create(body=body)
        response = request.execute()
        return response['scriptId']
