import re
import csv
import sys


def process_line(x):
    return ",".join(x.split()) #removes all spaces and replaces with single comma

rx_dict = {
    'Course': re.compile(r'^.*EXCO,(?P<course>\d{3}[A-Z]?),.*$'),
    'Code': re.compile(r'^\(unassigned\),(?P<code>\w{6}),.*$'),
}

def _parse_line(line):
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None

def parse_filecontents(file_contents):
    data = {}
    course = 0;
    for line in file_contents:
        key, match = _parse_line(line)
        if key == 'Course':
            course = match.group('course')
            data[course] = []
        if key == 'Code':
            code = match.group('code')
            data[course].append(code)
    return data

def print_dict(data):
    for key in data:
        print("EXCO ", key, "\n", data[key], "\n")

def main():
    with open(str(sys.argv[1])) as file:
        file_contents = list(map(process_line, file.read().splitlines())) # process each line
        data = parse_filecontents(file_contents)
        with open('formatted_data.csv', 'w') as f:
            w = csv.writer(f)
            for key in data.keys():
                w.writerow([key] + data[key])

main()
