from TODO.calendar_model import leapMonth, normalMonth
import datetime


# 달력 추가
def isLeapYear(year):
    if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
        return True
    return False


def getCalendar(year, month):
    calendar = []
    monthList = leapMonth if isLeapYear(year) else normalMonth

    tempList = []
    for day in range(1, monthList[month-1]+1):
        weekday = datetime.date(year, month, day).weekday()
        tempList.append([day, weekday])

        if weekday == 5:
            calendar.append(tempList)
            tempList = []

    if tempList:
        calendar.append(tempList)

    while len(calendar[0]) != 7:
        calendar[0].insert(0, [0, 0])
    return calendar

# 일정 추가

# 일정 삭제
