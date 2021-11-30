from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, \
                            QWidget,  QPushButton, QLabel, QLineEdit, \
                            QCalendarWidget, QListWidget, \
                            QDialog, QListWidgetItem, QMessageBox
from PyQt5.QtCore import QDate, Qt
import TODO.crawler
from TODO.schedule import Schedule
import datetime


def showException(text):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(text)
    msgBox.setWindowTitle("오류")
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.activateWindow()
    msgBox.exec_()


class TODOApp(QWidget):
    loginDialog = None
    schedule = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.schedule = Schedule()
        self.dateFormat = 'yyyy-MM-dd'
        self.initUI()

    def initUI(self):
        self.setFixedHeight(300)
        mainLayout = QGridLayout()

        # 동기화 버튼
        sync = QPushButton("동기화")
        mainLayout.addWidget(sync, 0, 0)

        # 검색
        funcLayout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("키워드 입력")
        addButton = QPushButton('+')
        delButton = QPushButton('-')
        funcLayout.addWidget(self.input)
        funcLayout.addWidget(addButton)
        funcLayout.addWidget(delButton)
        mainLayout.addLayout(funcLayout, 0, 1)
        self.setLayout(mainLayout)

        # 달력
        self.calendar = QCalendarWidget()
        mainLayout.addWidget(self.calendar, 1, 0)
        self.calendar.clicked[QDate].connect(self.showDate)
        self.calendar.clicked[QDate].connect(self.showSchedule)

        # 일정
        self.selectDate = QLabel()
        today = self.calendar.selectedDate()
        self.selectDate.setText(today.toString(self.dateFormat))
        self.todoList = QListWidget()
        schedule = QVBoxLayout()
        schedule.addWidget(self.selectDate)
        schedule.addWidget(self.todoList)
        mainLayout.addLayout(schedule, 1, 1)
        self.showSchedule(self.calendar.selectedDate())

        # 함수 연결
        sync.clicked.connect(self.synchronize)
        self.input.returnPressed.connect(self.searchItem)
        addButton.clicked.connect(self.addItem)
        delButton.clicked.connect(self.removeItem)

    def synchronize(self):
        self.loginDialog = QDialog()
        self.loginDialog.setWindowTitle("로그인")

        login_layout = QGridLayout()
        self.id = QLineEdit()
        self.id.setPlaceholderText("아이디")
        self.pw = QLineEdit()
        self.pw.setPlaceholderText("비밀번호")
        self.pw.setEchoMode(QLineEdit.Password)
        loginButton = QPushButton("로그인")
        loginButton.setMaximumHeight(60)
        login_layout.addWidget(self.id, 0, 0)
        login_layout.addWidget(self.pw, 1, 0)
        login_layout.addWidget(loginButton, 0, 1, 2, 1)
        self.loginDialog.setLayout(login_layout)
        self.loginDialog.show()

        loginButton.clicked.connect(self.login)

    def login(self):
        try:
            self.loginDialog.close()
            TODO.crawler.crawling(self.id.text(), self.pw.text())
            self.schedule.syncSchedule()
        except:
            showException("로그인 오류")

    def showDate(self, date):
        self.saveCheck(self.selectDate.text())
        selected = date.toString(self.dateFormat)
        self.selectDate.setText(selected)

    def showSchedule(self, date):
        selected = date.toString(self.dateFormat)
        self.todoList.clear()
        if selected in self.schedule.scheduleDict:
            for data in self.schedule.scheduleDict[selected]:
                text = data[1]
                item = QListWidgetItem(text)
                if data[0]:
                    item.setCheckState(Qt.Checked)
                else:
                    item.setCheckState(Qt.Unchecked)
                self.todoList.addItem(item)
        self.todoList.itemDoubleClicked.connect(self.modifyItem)

    def searchItem(self):
        word = self.input.text()
        self.todoList.clear()
        self.selectDate.setText("")

        for date in sorted(self.schedule.scheduleDict.keys()):
            lst = [i[1] for i in self.schedule.scheduleDict[date]]
            if any(word in i for i in lst):
                self.todoList.addItem(date)
                for data in self.schedule.scheduleDict[date]:
                    if word in data[1]:
                        text = data[1]
                        item = QListWidgetItem(text)
                        if data[0]:
                            item.setCheckState(Qt.Checked)
                        else:
                            item.setCheckState(Qt.Unchecked)
                        self.todoList.addItem(item)
                    else:
                        pass
        self.todoList.itemDoubleClicked.connect(self.modifyItem)

    def addItem(self):
        data = self.input.text()
        if data:
            item = QListWidgetItem(data)
            item.setCheckState(Qt.Unchecked)
            self.todoList.addItem(item)
            self.todoList.setDragDropMode(self.todoList.InternalMove)
            self.input.setText("")

            date = self.calendar.selectedDate().toString(self.dateFormat)
            self.schedule.addSchedule(date, data)

    def removeItem(self):
        index = self.todoList.currentRow()
        data = self.todoList.item(index).text()
        date = self.calendar.selectedDate().toString(self.dateFormat)
        self.schedule.removeSchedule(date, data)
        self.todoList.takeItem(index)

    def modifyItem(self):
        index = self.todoList.currentRow()
        data = self.todoList.item(index).text()

        self.editDialog = QDialog()
        self.editDialog.setWindowTitle("수정")

        editLayout = QGridLayout()
        self.editWindow = QLineEdit()
        self.editWindow.setText(data)

        editButton = QPushButton("수정")
        editButton.setMaximumHeight(60)
        editLayout.addWidget(self.editWindow, 0, 0)
        editLayout.addWidget(editButton, 1, 0)
        self.editDialog.setLayout(editLayout)
        self.editDialog.show()

        editButton.clicked.connect(self.modify)

    def modify(self):
        self.editDialog.close()
        index = self.todoList.currentRow()
        data = self.todoList.item(index).text()

        if self.selectDate.text() != "":
            date = str(self.selectDate.text())
        else:
            temp = index-1
            date = ""
            while 1:
                try:
                    text = self.todoList.item(temp).text()
                    datetime.datetime.strptime(text, "%Y-%m-%d")
                    date = str(text)
                    break
                except ValueError:
                    pass
                temp -= 1

        newData = self.editWindow.text()
        if newData == "":
            showException("데이터는 공백을 제외한 값을 넣어야 합니다.")
            self.modifyItem()

        for lst in self.schedule.scheduleDict[date]:
            if lst[1] == data:
                lst[1] = newData

        self.schedule.saveSchedule()
        self.todoList.item(index).setText(newData)

    def saveCheck(self, date):
        if self.selectDate.text() != "":
            date = str(self.selectDate.text())
        else:
            return

        try:
            lst = self.schedule.scheduleDict[date]
        except KeyError:
            return

        itemList = [[self.todoList.item(i).checkState(), str(self.todoList.item(i).text())] for i in range(self.todoList.count())]

        for i in range(len(itemList)):
            if itemList[i][0] == 2:
                lst[i][0] = True
            else:
                lst[i][0] = False
        self.schedule.scheduleDict[date] = lst
        self.schedule.saveSchedule()

    def saveSearchCheck(self):
        date = ""
        lst = []
        for i in range(self.todoList.count()):
            text = self.todoList.item(i).text()
            try:
                datetime.datetime.strptime(text, "%Y-%m-%d")
                for j in lst:
                    for k in Schedule.scheduleDict[date]:
                        if j[1] == k[1]:
                            if j[0] == 2:
                                k[0] = True
                            else:
                                k[0] = False
                            break
                lst = []
                date = text
            except:
                lst.append([self.todoList.item(i).checkState(), text])

    def closeEvent(self, event):
        self.saveCheck(self.calendar.selectedDate().toString(self.dateFormat))
