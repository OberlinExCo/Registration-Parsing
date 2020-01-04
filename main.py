import sys

from parse import CodeParser
from drive import GoogleDrive
from sheets import GoogleSheets

def main():
    parser = CodeParser()
    parser.parse(sys.argv[1])
    print("File has been parsed to" + parser.csv)

    sheets = GoogleSheets()
    sheets.createSheet("auth codes")
    sheets.push_csv_to_gsheet(parser.csv)

    #drive = GoogleDrive()
    #drive.uploadCSV(parser.csv)
    #print("File has been uploaded with id: " + drive.id)

    # parse .txt file => .csv file
    # upload .csv file to drive & convert to google sheets document
    # create form & data spreadsheet & add code(?) & trigger(?)

main()
