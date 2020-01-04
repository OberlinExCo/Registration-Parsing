import sys

from parse import CodeParser
from drive import GoogleDrive

def main():
    parser = CodeParser()
    print(parser.csv)
    #parser.parse(sys.argv[1])

    drive = GoogleDrive()

    # parse .txt file => .csv file
    # upload .csv file to drive & convert to google sheets document
    # create form & data spreadsheet & add code(?) & trigger(?)

main()
