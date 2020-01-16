from googleapiclient import discovery
from httplib2 import Http

class GoogleSheets:
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

    def __init__(self, creds):
        self.sheets_service = discovery.build('sheets', 'v4', credentials=creds)
        print("\nGoogle Sheets connection has been authenticated")

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
        print("Spreadsheet has been created with id " + self.id + "\n")
        return self

    def batchUpdateCSV(self,csv_path):
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
        return response.get("sheetId") # idk if this works, too lazy to test rn
