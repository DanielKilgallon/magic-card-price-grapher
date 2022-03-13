import os
import re
import csv

card_data = {}
headers = ['oracle_id','card name']

file_path = 'daily-files/'
files = os.listdir(file_path)
file_number = 0
print("aggregating data files")
for file_name in files:
    file_name_arr = re.split('_|\.', file_name)
    headers.append(file_name_arr[1])
    with open(file_path + file_name, encoding="utf8", errors='ignore', mode = 'r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            card_name = line[1].replace(",", '').replace('"', '').replace("\'", '').replace("-", '')
            if line[0] in card_data:
                card_data[line[0]][1] = card_name
                card_data[line[0]].append(line[2])
            else:
                buffer = []
                buffer.append(line[0])
                buffer.append(card_name)
                for i in range(0, file_number):
                    buffer.append('0')
                buffer.append(line[2])
                card_data[line[0]] = buffer
    file_number = file_number + 1


print("creating output.csv file")
with open('output.csv', mode = 'w', newline = '', encoding = 'utf-8') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(headers)
    for key in card_data:
        # filter out cards with 0 prices only
        price_data = card_data[key][2:]
        if price_data.count('0') == file_number:
            continue
        csv_writer.writerow(card_data[key])
print("done!")