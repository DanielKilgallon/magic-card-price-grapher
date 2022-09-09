import os
import re
import csv

price_data = {}
headers = ['name']

file_path = './card-prices-data-lake/warframe-daily-prices/'
files = os.listdir(file_path)
file_number = 0

print("aggregating data files")
for file_name in files:
    file_name_arr = re.split('_|\.', file_name)
    headers.append(file_name_arr[1])
    headers.append(file_name_arr[1] + " volume")
    with open(file_path + file_name, encoding="utf8", errors='ignore', mode = 'r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            item_name = line[0].replace(",", '').replace('"', '').replace("\'", '').replace("-", '')
            item_volume = line[1].replace(",", '').replace('"', '').replace("\'", '').replace("-", '')
            item_median = line[4].replace(",", '').replace('"', '').replace("\'", '').replace("-", '')
            
            if item_name in price_data:
                price_data[line[0]][0] = item_name
                price_data[item_name].append(item_volume)
                price_data[item_name].append(item_median)
            else:
                buffer = []
                buffer.append(item_name)
                for i in range(0, file_number):
                    buffer.append('0')
                    buffer.append('0')
                buffer.append(item_volume)
                buffer.append(item_median)
                price_data[line[0]] = buffer
            
    file_number = file_number + 1


print("creating output.csv file")
with open('wf-output.csv', mode = 'w', newline = '', encoding = 'utf-8') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(headers)
    for key in price_data:
        csv_writer.writerow(price_data[key])
print("done!")