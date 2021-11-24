from PyQt5.QtCore import QDate
from TODO.calendar_model import dataDict

# 일정 추가

# 일정 삭제

# 일정 가져오기
def getDaySchedule(date):
    for key, lst in dataDict.items():
        if key == date:
            return lst
