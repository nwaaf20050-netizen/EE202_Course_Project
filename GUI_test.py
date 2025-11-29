from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

import sys


class MainGuiTest(QMainWindow):
    def __init__(self):

        super(MainGuiTest,self).__init__()

        # Load the UI file
        uic.loadUi("GUI_MainApp.ui",self)

        self.setWindowTitle("Main Page")

        # Connect the login button to its function
        self.pushButton_Login.clicked.connect(self.loginButtonPressed)
        

    def loginButtonPressed(self):

        # Get username and password from input fields
        username = self.lineEdit_Username.text()
        password = self.lineEdit_Password.text()

        #Later you can add code to verify username and password

        print(f"Username: {username}, Password: {password}")
        
        







#Initialize the app

app = QtWidgets.QApplication(sys.argv)
main_window = MainGuiTest()
main_window.show()
sys.exit(app.exec_())