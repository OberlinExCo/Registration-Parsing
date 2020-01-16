from googleapiclient import discovery
from httplib2 import Http

class GoogleScripts:
    def __init__(self,creds,scriptId):
        self.script_service = discovery.build('script', 'v1', credentials=creds)
        self.scriptId = scriptId
        print("\nGoogle Script connection has been authenticated")

    def executeGoogleScript(self,courses,codesId,passwordsId):
        body = {
            "function" : "main",
            "parameters" : [courses, codesId, passwordsId]
        }
        request = self.script_service.scripts().run(scriptId=self.scriptId,body=body)
        response = request.execute()
        return response
