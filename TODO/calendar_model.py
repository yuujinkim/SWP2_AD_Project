import pickle
import csv

scheduleDict = {}

try:
    with open('schedule.pickle', 'rb') as fr:
        scheduleDict = pickle.load(fr, encoding='utf-8-sig')
except FileNotFoundError:
    pass
except EOFError:
    pass

try:
    f = open('data.csv', 'r', encoding='utf-8-sig')
    data = csv.reader(f)
    # line = 과목명, 제목, 마감일, 제출/시청 여부
    for line in data:
        date = line[2].split()[0]
        task = line[0] + line[1]
        checked = True if line[3] == 'yes' else False

        try:
            if any(task in lst[1] for lst in scheduleDict[date]):
                continue
            scheduleDict[date].append([checked, task])
        except KeyError:
            scheduleDict[date] = [[checked, task]]
    f.close()
except FileNotFoundError:
    pass

try:
    with open('schedule.pickle', 'wb') as fw:
        pickle.dump(scheduleDict, fw)
except FileNotFoundError:
    pass