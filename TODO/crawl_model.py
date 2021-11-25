import csv

crawlingDict = {}
f = open('data.csv', 'r', encoding='utf-8-sig')
data = csv.reader(f)
for line in data:
    date = line[2].split()[0]
    task = line[0].strip() + line[1]
    crawlingDict[date] = [[task, line[3]]]
f.close()
