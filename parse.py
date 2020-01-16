import re
import csv

class Parser:
    csv = "formatted_data.csv"

    rx_dict = {
        'Course': re.compile(r'^.*EXCO,(?P<course>\d{3}[A-Z]?),.*$'),
        'Code': re.compile(r'^\(unassigned\),(?P<code>\w{6}),.*$'),
        'ID': re.compile(r'\/spreadsheets\/d\/(?P<id>[a-zA-Z0-9-_]+)')
    }

    def _parse_line(self,line):
        for key, rx in self.rx_dict.items():
            match = rx.search(line)
            if match:
                return key, match
        return None, None

    def parse_filecontents(self,file_contents):
        data = {}
        course = 0;
        for line in file_contents:
            key, match = self._parse_line(line)
            if key == 'Course':
                course = match.group('course')
                data[course] = []
            if key == 'Code':
                code = match.group('code')
                data[course].append(code)
        return data

    def createCSV(self, data):
        with open(self.csv, 'w') as f:
            w = csv.writer(f)
            for key in data.keys():
                w.writerow([key] + data[key])

    def parseAuthCodes(self, filename):
        with open(filename) as file:
            file_contents = map(lambda x : ",".join(x.split()), file.read().splitlines()) # process each line
            data = self.parse_filecontents(file_contents)
            print("txt file has been parsed into an array")
            self.createCSV(data)
        print("File has been parsed to " + self.csv)
        return self.csv

    def parseURL(self, URL):
        key, match = self._parse_line(URL)
        if key == 'ID':
            return match.group('id')
        else:
            return ""

    def getKeys(self, csvFilename):
        retVal = []
        with open(csvFilename, 'r') as csv_file:
            for row in csv_file:
                retVal.append(row.split(",")[0])
        return retVal
