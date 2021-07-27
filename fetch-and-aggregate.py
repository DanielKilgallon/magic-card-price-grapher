import os
import re
import csv

# os.system('cmd /c "aws s3 sync s3://card-prices-data-lake ./price-data-files/"')
 
card_data = {}
headers = ['oracle_id','card name']

file_path = 'price-data-files/'
files = os.listdir(file_path)
file_number = 0
for file_name in files:
    file_name_arr = re.split('_|\.', file_name)
    headers.append(file_name_arr[1])
    with open(file_path + file_name, mode ='r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            card_name = line[1].replace(',', '').replace('"', '')
            if line[0] in card_data:
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

with open('output.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(headers)
    for key in card_data:
        spamwriter.writerow(card_data[key])