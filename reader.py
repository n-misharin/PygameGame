import csv


data = open('data.txt', encoding="utf8").read()
for row in data.split('\n')[1:]:
    if len(row) > 1:
        print(row.split('\t'))