import sys

from oauth2client import file, client, tools

from parse import CodeParser
from drive import GoogleDrive
from sheets import GoogleSheets
from script import GoogleScripts

SCOPES = ['https://www.googleapis.com/auth/script.projects',
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

def main():

    # set up argument for just parsing txt file & not uploading & all that

    # authorize Google API stuff
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    # Request name of file for unparsed codes
    print("\nEnter the file name for unparsed codes:")
    codes = input()

    # Parse txt file from Registrar's Office into csv file
    parser = CodeParser()
    parser.parse(codes)
    print("File has been parsed to" + parser.csv)

    # Uploads csv file into google sheets document in drive
    sheets = GoogleSheets(creds)
    sheets.createSheet("auth codes")
    codesId = sheets.push_csv_to_gsheet(parser.csv)

    # request link for passcode document here

    scripts = GoogleScripts(creds)
    # create form for auth requests (write script to do this probably)
    # add google script code
    #   (link to appropriate documents: list of codes, password document)
    #   (set up trigger)

    # organize documents into a folder that makes sense
    drive = GoogleDrive(creds)

main()
