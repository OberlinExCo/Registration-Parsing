import sys

from oauth2client import file, client, tools

from parse import Parser
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
    inputFilename = input()

    outputFilename = Parser().parseAuthCodes(inputFilename)

    # ------------------------------------------------------

    # Upload CSV file?
    queryContinue("Would you like to upload this CSV file to Google Drive?")

    # authorize Google API stuff
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store) # creds variable is here!!

    # Uploads csv file into google sheets document in drive
    codesId = GoogleSheets(creds).createSheet("Authorization Codes").batchUpdateCSV(outputFilename)

    # ------------------------------------------------------

    # Generate Request Form & Responses Spreadsheet?
    queryContinue("Would you like to generate code request form with this as the primary document?")

    # request link for passcode document here
    print("Please paste the URL for the spreadsheet of passwords:")
    passwordsURL = input()
    passwordsId = Parser().parseURL(passwordsURL)

    # parse list of courses into an array
    courses = Parser().getKeys(outputFilename)

    # execute google script
    GoogleScripts(creds).executeGoogleScript(courses,codesId,passwordsId)

    # runMain("M6jN59wI6iRfX8V7CqwI1OF6JaInSVJzV")

    # open up browser to set up trigger



# used to quit the program if "no", continue if "yes"
def queryContinue(prompt):
    validInput = False
    while not validInput:
        print("\n" + prompt + " (y/n)")
        response = input()

        if response in ['y','Y','yes','Yes']:
            validInput = True
        if response in ['n','N','no','No']:
            sys.exit()
    print("\n")

main()
