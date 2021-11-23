from TODO.calendar_controller import getCalendar
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, \
                            QLineEdit, QTextEdit, QPushButton, QVBoxLayout, \
                            QScrollArea, QGroupBox, QFormLayout

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
        weekdayLayout = QGridLayout()
        dayLayout = QGridLayout()
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

        monthLayout.addWidget(QLineEdit("2021년 11월"), 0, 0)
        weekdayLayout.addWidget(QLineEdit("일 월 화 수 목 금 토"), 0, 0)

        calendar = getCalendar(2021, 11)
        for rows in calendar:
            for cols in rows:
                button = QPushButton(str(cols[0]), self)
                button.setMaximumWidth(50)
                row = calendar.index(rows)
                col = rows.index(cols)
                dayLayout.addWidget(button, row, col)

        syncLayout.addWidget(QLineEdit("새로고침"), 0, 0)
        dateLayout.addWidget(QLineEdit("11월 23일"), 0, 0)
        searchLayout.addWidget(QLineEdit("키워드 검색"), 0, 0)


        # layoutList = [monthLayout, weekdayLayout, dayLayout, synchroLayout,
        #               dateLayout, todoLayout, searchLayout]

        calendarLayout.addLayout(monthLayout)
        calendarLayout.addLayout(weekdayLayout)
        calendarLayout.addLayout(dayLayout)
        calendarLayout.addLayout(syncLayout)

        scheduleLayout.addLayout(dateLayout)
        scheduleLayout.addWidget(todoArea)
        scheduleLayout.addLayout(searchLayout)

        mainLayout.addLayout(calendarLayout, 0, 0)
        mainLayout.addLayout(scheduleLayout, 0, 1)

        self.setLayout(mainLayout)

# 로그인 (crawl 이동)

# calendar = getCalendar(2021, 11)
# for row in calendar:
#     for col in row:
#         print(col[0], end=" ")
#     print()
