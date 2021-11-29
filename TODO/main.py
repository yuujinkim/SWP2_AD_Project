import sys
from PyQt5.QtWidgets import QApplication
from TODO.application import TODOApp

# main
app = QApplication(sys.argv)
todo = TODOApp()
todo.setWindowTitle("일정")
todo.show()
sys.exit(app.exec_())
