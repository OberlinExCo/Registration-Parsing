import sys

from oauth2client import file, client, tools

from parse import CodeParser
from drive import GoogleDrive
from sheets import GoogleSheets
from script import GoogleScripts

SCOPES = ['https://www.googleapis.com/auth/cloud-platform',
'https://www.googleapis.com/auth/script.projects',
'https://www.googleapis.com/auth/script.deployments',
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive']

def main():

    # Parse txt file from Registrar's Office into csv file
    print("\nEnter the file name for unparsed codes:")
    filename = input()

    outputFilename = Parser().parseAuthCodes(filename)


    # authorize Google API stuff
    queryContinue("Would you like to upload this CSV file to Google Drive? (y/n)")

    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)


    # Uploads csv file into google sheets document in drive
    sheets = GoogleSheets(creds)
    sheets.createSheet("auth codes")
    codesId = sheets.push_csv_to_gsheet(outputFilename) # print out relevant information


    # Query user about further steps
    queryContinue("Would you like to generate code request form with this as the primary document? (y/n)")

    scripts = GoogleScripts(creds)
    print(scripts.runMain("M6jN59wI6iRfX8V7CqwI1OF6JaInSVJzV"))
    # create form for auth requests (write script to do this probably)
    # add google script code
    #   (link to appropriate documents: list of codes, password document)
    #   (set up trigger)

    # return # temporary



    # request link for passcode document here

    scripts = GoogleScripts(creds)
    # create form for auth requests (write script to do this probably)
    # add google script code
    #   (link to appropriate documents: list of codes, password document)
    #   (set up trigger)

    # organize documents into a folder that makes sense
    drive = GoogleDrive(creds)

def queryContinue(prompt):
    validInput = False
    while not validInput:
        print("\n" + prompt)
        response = input()

        if response in ['y','Y','yes','Yes']:
            validInput = True
        if response in ['n','N','no','No']:
            sys.exit()

main()
