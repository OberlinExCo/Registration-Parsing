import sys
import time
import webbrowser

from oauth2client import file, client, tools

from parse import Parser
from sheets import GoogleSheets
from script import GoogleScripts

SCOPES = ['https://www.googleapis.com/auth/script.projects',
            'https://www.googleapis.com/auth/script.scriptapp',
            'https://www.googleapis.com/auth/script.send_mail',
            'https://www.googleapis.com/auth/forms',
            'https://www.googleapis.com/auth/spreadsheets']

scriptId = "M6jN59wI6iRfX8V7CqwI1OF6JaInSVJzV"

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
        print("Credentials have been generated")

    # Uploads csv file into google sheets document in drive
    codesId = GoogleSheets(creds).createSheet("Authorization Codes").batchUpdateCSV(outputFilename)

    # ------------------------------------------------------

    # Generate Request Form & Responses Spreadsheet?
    queryContinue("Would you like to generate code request form with this as the primary document?")

    print("In order for this program to run, there must be a password document with the course numbers in the first column\nand the \"passwords\" set by instructors so that only they can request auth codes for their course in the second column.\nThis doesn't need to be complete at the moment, but the document must exist. If you have not created it yet, please do so now.\n")

    # request link for passcode document here
    print("Please paste the URL for the spreadsheet of passwords below:")
    passwordsURL = input()
    passwordsId = Parser().parseURL(passwordsURL)

    # parse list of courses into an array
    courses = Parser().getKeys(outputFilename)
    courses.sort()

    # execute google script
    response = GoogleScripts(creds,scriptId).executeGoogleScript(courses,codesId,passwordsId)
    print(response)

    # Open up browser to set up trigger
    print("\nIn order to complete the setup of this form, you must run a function from the script console to install the trigger.\nWhen the broswer window opens up, select the \'addTrigger\' function from the drop-down menu & click the \'run\' button")

    time.sleep(5)
    webbrowser.open("https://script.google.com/a/oberlin.edu/d/1UVQHcz0uZrXbjx-HN0JZyM5q_EY5owd5zduyj1NubCz1-RcYrpFdVZaF/edit?usp=drive_web")

    print("\nWords of Guidance:\n")
    print("If the password function is not working, make sure that the passwords themselves are cast as \'plain text\' and not a \'number\'\n")
    print("Use this script to parse & upload additional files sent by the Registrar's office, but manually copy over the codes to the primary spreadsheet & copy the course numbers to the google form.")



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
