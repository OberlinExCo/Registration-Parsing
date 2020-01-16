from googleapiclient import discovery
from httplib2 import Http

scriptId = "M6jN59wI6iRfX8V7CqwI1OF6JaInSVJzV"

class GoogleScripts:
    def __init__(self,creds):
        self.script_service = discovery.build('script', 'v1', credentials=creds)
        print("\nGoogle Script connection has been authenticated")

    def executeGoogleScript(self,courses,codesId,passwordsId):
        body = {
            "function" : "main",
            "parameters" : [courses, codesId, passwordsId]
        }
        request = self.script_service.scripts().run(scriptId=scriptId,body=body)
        response = request.execute()
        return response['response']['result']
