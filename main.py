import sys

from parse import CodeParser
from drive import GoogleDrive
from sheets import GoogleSheets
from script import GoogleScripts

def main():
    # Parse txt file from Registrar's Office into csv file
    parser = CodeParser()
    parser.parse(sys.argv[1])
    print("File has been parsed to" + parser.csv)

    # Uploads csv file into google sheets document in drive
    sheets = GoogleSheets()
    sheets.createSheet("auth codes")
    sheets.push_csv_to_gsheet(parser.csv)

    # request link for passcode document here

    scripts = GoogleScripts()
    # create form for auth requests (write script to do this probably)
    # add google script code
    #   (link to appropriate documents: list of codes, password document)
    #   (set up trigger)

    # organize documents into a folder that makes sense

main()
