from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

import sys

import RegistrationSystemClass

class MainGuiTest(QMainWindow):
    def __init__(self):
        super(MainGuiTest,self).__init__()
        uic.loadUi("GUI_MainApp.ui",self)
        self.setWindowTitle("GuiMaster Test")
        
        self.pushButton_Login1.clicked.connect(self.buttonPressed)

    def buttonPressed(self):
        '''
        method authentication
        1 2
        method(1,2)
        '''
    
        print("Login Button Clicked")
        print("asdgjklhgf")
        #Opens a new window or performs login actions
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainGuiTest()
    window.show()
    sys.exit(app.exec_())