from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, \
                            QLineEdit, QTextEdit, QPushButton, QVBoxLayout, \
                            QScrollArea, QGroupBox, QFormLayout, QCalendarWidget
from PyQt5.QtCore import QDate
from TODO.calendar_controller import getDaySchedule
from TODO.todo_model import dateFormat


# pyqt will be designed
class TODOApp(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setFixedHeight(300)
        mainLayout = QGridLayout()

        calendarLayout = QVBoxLayout()
        scheduleLayout = QVBoxLayout()

        monthLayout = QGridLayout()
        syncLayout = QGridLayout()

        dateLayout = QGridLayout()
        todoGroupbox = QGroupBox()
        todoLayout = QFormLayout()
        for i in range(10):
            button = QPushButton("□", self)
            button.setMaximumWidth(50)
            todoLayout.addRow(button, QLineEdit("과제"))
        todoGroupbox.setLayout(todoLayout)
        todoArea = QScrollArea()
        todoArea.setWidget(todoGroupbox)
        searchLayout = QGridLayout()

        self.calendar = self.getCalendarWidget()
        self.getSchedule()
        monthLayout.addWidget(self.calendar)
        syncLayout.addWidget(QLineEdit("새로고침"), 0, 0)

        dateLayout.addWidget(QLineEdit("11월 23일"), 0, 0)
        searchLayout.addWidget(QLineEdit("키워드 검색"), 0, 0)


        # layoutList = [monthLayout, weekdayLayout, dayLayout, synchroLayout,
        #               dateLayout, todoLayout, searchLayout]

        calendarLayout.addLayout(monthLayout)
        calendarLayout.addLayout(syncLayout)

        scheduleLayout.addLayout(dateLayout)
        scheduleLayout.addWidget(todoArea)
        scheduleLayout.addLayout(searchLayout)

        mainLayout.addLayout(calendarLayout, 0, 0)
        mainLayout.addLayout(scheduleLayout, 0, 1)

        self.setLayout(mainLayout)

    def getCalendarWidget(self):
        cal = QCalendarWidget()
        cal.setGridVisible(True)
        cal.selectionChanged.connect(self.getSchedule)

        return cal

    # QDate type date
    def getSchedule(self):
        date = self.calendar.selectedDate().toString(dateFormat)
        print(self.calendar.selectedDate().toString(dateFormat))
        print(getDaySchedule(date))


# 로그인 (crawl 이동)

# calendar = getCalendar(2021, 11)
# for row in calendar:
#     for col in row:
#         print(col[0], end=" ")
#     print()
