import sys

from parse import CodeParser
from drive import GoogleDrive
from sheets import GoogleSheets

def main():
    # Parse txt file from Registrar's Office into csv file
    parser = CodeParser()
    parser.parse(sys.argv[1])
    print("File has been parsed to" + parser.csv)

    # Uploads csv file into google sheets document in drive
    sheets = GoogleSheets()
    sheets.createSheet("auth codes")
    sheets.push_csv_to_gsheet(parser.csv)

    # create form & data spreadsheet & add code(?) & trigger(?)
    # organize drive to make sense

main()
