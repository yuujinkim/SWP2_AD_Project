from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, \
                            QWidget,  QPushButton, QLabel, QLineEdit, \
                            QCalendarWidget, QListWidget, \
                            QDialog, QListWidgetItem, QMessageBox
from PyQt5.QtCore import QDate, Qt
from TODO.todo_model import dateFormat
import TODO.crawl_controller
import TODO.calendar_model
from TODO.calendar_controller import addSchedule, removeSchedule, syncSchedule, saveSchedule


def showException(text):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(text)
    msgBox.setWindowTitle("오류")
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.activateWindow()
    msgBox.exec_()


# pyqt will be designed
class TODOApp(QWidget):
    loginDialog = None

    def __init__(self, parent=None):
        super().__init__(parent)
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
        mainLayout.addWidget(calendar, 1, 0)
        self.calendar.clicked[QDate].connect(self.showDate)
        self.calendar.clicked[QDate].connect(self.showSchedule)

        # 일정
        self.selectDate = QLabel()
        today = self.calendar.selectedDate()
        self.selectDate.setText(today.toString(dateFormat))
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
            TODO.crawl_controller.crawling(self.id.text(), self.pw.text())
            syncSchedule()
        except:
            showException("로그인 오류")

    def showDate(self, date):
        selected = date.toString(dateFormat)
        self.selectDate.setText(selected)

    def showSchedule(self, date):
        selected = date.toString(dateFormat)
        self.todoList.clear()
        if selected in TODO.calendar_model.scheduleDict:
            for data in TODO.calendar_model.scheduleDict[selected]:
                text = data[1]
                item = QListWidgetItem(text)
                if data[0]:
                    item.setCheckState(Qt.Checked)
                else:
                    item.setCheckState(Qt.Unchecked)
                self.todoList.addItem(item)
            self.todoList.setDragDropMode(self.todoList.InternalMove)
        self.todoList.itemDoubleClicked.connect(self.modifyItem)

    def searchItem(self):
        word = self.input.text()
        self.todoList.clear()
        self.selectDate.setText("")

        for date in sorted(TODO.calendar_model.scheduleDict.keys()):
            lst = [i[1] for i in TODO.calendar_model.scheduleDict[date]]
            if any(word in i for i in lst):
                self.todoList.addItem(date)
                for data in TODO.calendar_model.scheduleDict[date]:
                    print(data)
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
        self.todoList.setDragDropMode(self.todoList.InternalMove)
        self.todoList.itemDoubleClicked.connect(self.modifyItem)

    def addItem(self):
        data = self.input.text()
        if data:
            item = QListWidgetItem(data)
            item.setCheckState(Qt.Unchecked)
            self.todoList.addItem(item)
            self.todoList.setDragDropMode(self.todoList.InternalMove)
            self.input.setText("")

            date = self.calendar.selectedDate().toString(dateFormat)
            addSchedule(date, data)

    def removeItem(self):
        index = self.todoList.currentRow()
        data = self.todoList.item(index).text()
        date = self.calendar.selectedDate().toString(dateFormat)
        removeSchedule(date, data)
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
        date = self.calendar.selectedDate().toString(dateFormat)

        newData = self.editWindow.text()
        for lst in TODO.calendar_model.scheduleDict[date]:
            if lst[1] == data:
                lst[1] = newData

        saveSchedule()
        self.todoList.item(index).setText(newData)