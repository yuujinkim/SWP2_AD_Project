# 일정 추가
from TODO.calendar_model import scheduleDict
import pickle
import csv


# 일정 추가
def addSchedule(date, data):
    try:
        scheduleDict[date].append([False, data, False])
    except KeyError:
        scheduleDict[date] = [[False, data, False]]
    saveSchedule()
# 일정 삭제

# 일정 가져오기

def removeSchedule(date, data):
    lst = scheduleDict[date]
    for i in range(len(lst)):
        if lst[i][1] == data:
            del lst[i]
            break
    saveSchedule()


def syncSchedule():
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
                scheduleDict[date].append([checked, task, False])
            except KeyError:
                scheduleDict[date] = [[checked, task, False]]
        f.close()
    except FileNotFoundError:
        pass


# 변경 저장하기
def saveSchedule():
    try:
        with open('schedule.pickle', 'wb') as fw:
            pickle.dump(scheduleDict, fw)
    except FileNotFoundError:
        pass