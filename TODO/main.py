import sys
from PyQt5.QtWidgets import QApplication
from TODO.todo_controller import TODOApp
import selenium
# main
app = QApplication(sys.argv)
todo = TODOApp()
todo.show()
sys.exit(app.exec_())
