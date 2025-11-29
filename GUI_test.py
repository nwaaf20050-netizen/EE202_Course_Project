from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

import sys


#================= Main Application Window =====================#
class MainApp(QMainWindow):
    def __init__(self):

        super(MainApp,self).__init__()

        # Load the UI file
        uic.loadUi("GUI_MainApp.ui",self)

        self.setWindowTitle("Main Page")

        # Connect the login button to its function
        self.pushButton_Login.clicked.connect(self.loginButtonPressed)
        self.pushButton_Close.clicked.connect(self.close)
        

    def loginButtonPressed(self):

        # Get username and password from input fields
        username = self.lineEdit_Username.text()
        password = self.lineEdit_Password.text()

        #Later you can add code to verify username and password

        print(f"Username: {username}, Password: {password}")
        
        #Open Window after login
        self.studentPage = StudentPage()
        self.studentPage.show()

        #hide the main window
        self.hide()

        #Close the login window
        # self.close() #Don't use close() method here it will cause an error

        
    def close(self):
        self.close()

#================= Student Page Window =====================#
        
class StudentPage(QMainWindow):
    def __init__(self):

        super(StudentPage,self).__init__()

        # Load the UI file
        uic.loadUi("GUI_StudentPage.ui",self)

        self.setWindowTitle("Student Page")

        # Connect buttons to their functions
        self.commandLinkButton_StudentProfile.clicked.connect(self.openStudentProfile)
        self.commandLinkButton_CourseRegistration.clicked.connect(self.openCourseRegistration)
        self.commandLinkButton_Logout.clicked.connect(self.logout)


    def openStudentProfile(self):
        pass  # Implement student profile functionality here

    def openCourseRegistration(self):
        pass  # Implement course registration functionality here

    def logout(self):
        self.mainApp = MainApp()
        self.mainApp.show()
        self.close()

        







#Initialize the app

app = QtWidgets.QApplication(sys.argv)
main_window = MainApp()
main_window.show()
sys.exit(app.exec_())