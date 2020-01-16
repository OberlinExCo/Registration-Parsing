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
        request = self.script_service.scripts().run(scriptId=id,body=body)
        response = request.execute()
        return response['response']['result']

    def createProject(self,title,parentId):
        body = {
            'title' : title,
            'parentId' : parentId
        }
        request = self.script_service.projects().create(body=body)
        response = request.execute()
        return response['scriptId']

    def updateProject(self,id,script):
        body = {
            "scriptId" : id,
            "files" : [
                {
                    "name" : "appsscript",
                    "type" : "JSON",
                    "source" : "{\"timeZone\":\"America/New_York\",\"exceptionLogging\":\"CLOUD\"}"
                },
                {
                    "name" : "main",
                    "type" : "SERVER_JS",
                    "source" : script
                }
            ]
        }
        request = self.script_service.projects().updateContent(scriptId=id,body=body)
        response = request.execute()
        return response["scriptId"]

    def deployProject(self,id):
        body = {
            "versionNumber" : 1,
            "scriptId" : id,
            "description" : "for internal operations"
        }
        request = self.script_service.projects().deployments().create(scriptId=id,body=body)
        response = request.execute()
        return response

    def runMain(self,id):
         body = {
             "function" : "main"
         }
         request = self.script_service.scripts().run(scriptId=id,body=body)
         response = request.execute()
         return response['response']['result']

    def generateForm(self):
        with open("scripts/generateForm.gs") as script:
            id = self.createProject('Form Creation','')
            GenerateForm = script.read()
            self.updateProject(id,GenerateForm)
            print("Project has been created & updated with script: " + id)

            # in order to do anything below, you must add the script project to
            # the quickstart project cloud-based project rather than default
            # is there an api to do this too? Cloud Resource Manager API?
            # somehow have to deploy as an API executable using API? get the API ID?

            deploy = self.deployProject(id)
            print("Project has been deployed")
            print(deploy)

            result = self.runMain(id)
            print(result)

        # run script & create form & stuff
        # add script & set up trigger
