from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

import sys

class GuiMasterTest(QMainWindow):
    def __init__(self):
        super(GuiMasterTest,self).__init__()
        uic.loadUi("MainApp.ui",self)
        self.setWindowTitle("GuiMaster Test")
        
        self.pushButton_SystemLogin.clicked.connect(self.systemLogin)

    def systemLogin(self):
        print("System Login Button Clicked")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GuiMasterTest()
    window.show()
    sys.exit(app.exec_())