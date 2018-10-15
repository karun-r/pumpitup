import csv
import os
import sys
import json 
sys.path.insert(0, os.getcwd())


def parse_json(file_path):
    with open(file_path,newline='') as input_file:
        json_data = json.load(input_file)
    test_data = json_data["data"]
    csv_data = open('data/external/testdata.csv', 'w')
    csvwriter = csv.writer(csv_data)
    header_index = 0
    for dt in test_data:
        if header_index == 0:
            header = dt.keys()
            csvwriter.writerow(header)
            header_index += 1
        csvwriter.writerow(dt.values())
    csv_data.close()


if __name__ == '__main__':
    parse_json("data/external/data.json")