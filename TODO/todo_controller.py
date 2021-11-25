from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, \
                            QWidget,  QPushButton, QLabel, QLineEdit, QCheckBox, \
                            QCalendarWidget, QScrollArea, \
                            QDialog
from PyQt5.QtCore import QDate
from TODO.todo_model import dateFormat
import TODO.crawl_controller
import TODO.calendar_model


# pyqt will be designed
class TODOApp(QWidget):
    loginDialog = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setFixedHeight(300)
        mainLayout = QGridLayout()

        # 달력
        calendar = QCalendarWidget()
        mainLayout.addWidget(calendar, 0, 0)
        calendar.clicked[QDate].connect(self.showDate)

        # 일정
        self.selectDate = QLabel()
        today = calendar.selectedDate()
        self.selectDate.setText(today.toString(dateFormat))

        todoLayout = QVBoxLayout()
        check1 = QCheckBox("과제 1")
        check2 = QCheckBox("과제 2")
        check3 = QCheckBox("과제 3")
        check4 = QCheckBox("과제 4")
        check5 = QCheckBox("과제 5")
        check6 = QCheckBox("과제 6")
        check7 = QCheckBox("과제 7")
        check8 = QCheckBox("과제 8")
        check9 = QCheckBox("과제 9")

        todoLayout.addWidget(self.selectDate)
        todoLayout.addWidget(check1)
        todoLayout.addWidget(check2)
        todoLayout.addWidget(check3)
        todoLayout.addWidget(check4)
        todoLayout.addWidget(check5)
        todoLayout.addWidget(check6)
        todoLayout.addWidget(check7)
        todoLayout.addWidget(check8)
        todoLayout.addWidget(check9)

        schedule = QWidget()
        schedule.setLayout(todoLayout)
        scheduleArea = QScrollArea()
        scheduleArea.setWidget(schedule)
        # scheduleArea.setWidgetResizable(True)
        scheduleLayout = QVBoxLayout()
        scheduleLayout.addWidget(self.selectDate)
        scheduleLayout.addWidget(scheduleArea)
        mainLayout.addLayout(scheduleLayout, 0, 1)

        # 동기화 버튼
        sync = QPushButton("동기화")
        mainLayout.addWidget(sync, 1, 0)

        # 검색
        search = QLineEdit()
        search.setPlaceholderText("키워드 검색")
        mainLayout.addWidget(search, 1, 1)
        self.setLayout(mainLayout)

        # 함수 연결
        sync.clicked.connect(self.synchronize)

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
        self.loginDialog.close()
        TODO2.crawl_controller.crawling(self.id.text(), self.pw.text())

    def showDate(self, date):
        selected = date.toString(dateFormat)
        self.selectDate.setText(selected)
