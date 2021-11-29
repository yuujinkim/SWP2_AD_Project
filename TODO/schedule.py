# 일정 추가
import pickle
import csv


class Schedule:
    scheduleDict = {}

    def __init__(self):
        try:
            with open('schedule.pickle', 'rb') as fr:
                self.scheduleDict = pickle.load(fr, encoding='utf-8-sig')
        except FileNotFoundError:
            pass
        except EOFError:
            pass
        self.syncSchedule()
        self.saveSchedule()

    def addSchedule(self, date, data):
        try:
            self.scheduleDict[date].append([False, data])
        except KeyError:
            self.scheduleDict[date] = [[False, data]]
        self.saveSchedule()

    def removeSchedule(self, date, data):
        lst = self.scheduleDict[date]
        for i in range(len(lst)):
            if lst[i][1] == data:
                del lst[i]
                break
        self.saveSchedule()

    def syncSchedule(self):
        try:
            f = open('data.csv', 'r', encoding='utf-8-sig')
            data = csv.reader(f)
            # line = 과목명, 제목, 마감일, 제출/시청 여부
            for line in data:
                date = line[2].split()[0]
                task = line[0] + line[1]
                checked = True if line[3] == 'yes' else False

                try:
                    if any(task in lst[1] for lst in self.scheduleDict[date]):
                        continue
                    self.scheduleDict[date].append([checked, task])
                except KeyError:
                    self.scheduleDict[date] = [[checked, task]]
            f.close()
        except FileNotFoundError:
            pass

    # 변경 저장하기
    def saveSchedule(self):
        try:
            with open('schedule.pickle', 'wb') as fw:
                pickle.dump(self.scheduleDict, fw)
        except FileNotFoundError:
            pass
