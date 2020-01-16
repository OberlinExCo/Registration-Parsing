from googleapiclient import discovery
from httplib2 import Http

class GoogleScripts:
    def __init__(self,creds):
        self.script_service = discovery.build('script', 'v1', credentials=creds)
        print("Google Script connection has been authenticated")

    def executeGoogleScript(self,courses,codesId,passwordsId):
        body = {
            "function" : "main",
            "parameters" : [courses, codesId, passwordsId]
        }
        request = self.script_service.scripts().run(scriptId=id,body=body) # must switch out this id
        response = request.execute()
        return response['response']['result']
