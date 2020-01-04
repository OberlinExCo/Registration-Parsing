from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload

class GoogleSheets:
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

    def __init__(self):
        store = file.Storage('storage.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, store)
        self.sheets_service = discovery.build('sheets', 'v4', http=creds.authorize(Http()))
        print("Google Sheets connection has been authenticated")

    def createSheet(self, title):
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = self.sheets_service.spreadsheets().create(body=spreadsheet,
                                            fields='spreadsheetId').execute()
        self.id = spreadsheet.get('spreadsheetId')
        self.gid = spreadsheet.get('sheetId')
        print("Spreadsheet has been created with id " + self.id)

    def push_csv_to_gsheet(self,csv_path):
        with open(csv_path, 'r') as csv_file:
            csvContents = csv_file.read()
        body = {
            'requests': [{
                'pasteData': {
                    "coordinate": {
                        "sheetId": self.gid,
                        "rowIndex": "0",  # adapt this if you need different positioning
                        "columnIndex": "0", # adapt this if you need different positioning
                    },
                    "data": csvContents,
                    "type": 'PASTE_NORMAL',
                    "delimiter": ',',
                }
            }]
        }
        request = self.sheets_service.spreadsheets().batchUpdate(spreadsheetId=self.id, body=body)
        response = request.execute()



x = GoogleSheets()
x.createSheet("codes")
x.push_csv_to_gsheet("formatted_data.csv")
