import os
import re
import csv

os.system('cmd /c "aws s3 sync s3://card-prices-data-lake ./price-data-files/"')
 
card_data = {}
headers = ['id','card name']

first_file = False

file_path = 'price-data-files/'
files = os.listdir(file_path)
for file_name in files:
    file_name_arr = re.split('_|\.', file_name)
    headers.append(file_name_arr[1])
    with open(file_path + file_name, mode ='r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            card_name = line[1]
            if first_file is False:
                card_data[line[0]] = [line[0], card_name, line[2]]
            else:
                card_data[line[0]].append(line[2])
        first_file = True

with open('output.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(headers)
    for key in card_data:
        spamwriter.writerow(card_data[key])