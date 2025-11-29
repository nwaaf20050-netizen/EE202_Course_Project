from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys

#================= Main Application Window =====================#
class MainApp(QMainWindow):

    def __init__(self):

        super(MainApp, self).__init__()
        
        # Load the UI file with error handling
        try:
            uic.loadUi("GUI_MainApp.ui", self)
        except FileNotFoundError:
            print("Error: GUI_MainApp.ui not found. Please ensure the file exists.")
            sys.exit(1)

        # Create child windows once (single instances) and set this as their parent
        self.studentPage = StudentPage(parent=self)  # Parent: MainApp

        self.setWindowTitle("Main Page")

        # Connect the login button to its function
        self.pushButton_Login.clicked.connect(self.loginButtonPressed)
        # Connect the close button to quit the app
        self.pushButton_Close.clicked.connect(self.closeApp)


    def loginButtonPressed(self):
        username = self.lineEdit_Username.text()
        password = self.lineEdit_Password.text()

        print(f"Username: {username}, Password: {password}")

        # Hide login and show student page (reuse instances)
        self.hide()
        self.studentPage.show()


    def closeApp(self):
        # Properly quit the application
        QApplication.quit()


    def closeEvent(self, event):
        # Override to quit the app when the main window closes (e.g., via X button)
        QApplication.quit()
        event.accept()




#================= Student Page Window =====================#
class StudentPage(QMainWindow):

    def __init__(self, parent=None):

        super(StudentPage, self).__init__(parent)  # Set parent for proper parenting
        
        # Load the UI file with error handling
        try:
            uic.loadUi("GUI_StudentPage.ui", self)
        except FileNotFoundError:
            print("Error: GUI_StudentPage.ui not found. Please ensure the file exists.")
            sys.exit(1)
        
        self.setWindowTitle("Student Page")

        # Create child window (single instance) and set this as its parent
        self.studentProfile = StudentProfile(parent=self)  # Parent: StudentPage

        # Connect buttons to their functions
        self.commandLinkButton_StudentProfile.clicked.connect(self.openStudentProfile)
        self.commandLinkButton_CompletedCourses.clicked.connect(self.openCompletedCourses)
        self.commandLinkButton_CourseRegistration.clicked.connect(self.openCourseRegistration)
        self.commandLinkButton_Logout.clicked.connect(self.logout)



    def openStudentProfile(self):
        # Hide this window and show profile (reuse instance)
        self.hide()
        self.studentProfile.displayInformation()  #Since self.studentProfile exists
        self.studentProfile.show()


    def openCompletedCourses(self):
        pass  # Implement completed courses functionality here


    def openCourseRegistration(self):
        pass  # Implement course registration functionality here


    def logout(self):
        # Hide this window and show main app (reuse instance via parent)
        self.hide()
        self.parent().show()  # Access parent (MainApp) and show it




#================= Student Profile Window =====================#
class StudentProfile(QMainWindow):

    def __init__(self, parent=None):

        super(StudentProfile, self).__init__(parent)  # Set parent for proper parenting

        # Load the UI file with error handling
        try:
            uic.loadUi("GUI_StudentProfile.ui", self)
        except FileNotFoundError:
            print("Error: GUI_StudentProfile.ui not found. Please ensure the file exists.")
            sys.exit(1)

        self.setWindowTitle("Student Profile")

        # Connect button (fixed to match UI: 'pushButton' instead of 'pushButton_Back')
        self.pushButton_Back.clicked.connect(self.goBack)

    def displayInformation(self):

        name = "Ahmed Afifi"  # Example name, replace with actual data retrieval logic
        self.lineEdit_Name.setText(name)
        
        id_num = 2222222  # Example ID, replace with actual data retrieval logic
        self.lineEdit_IDNumber.setText(str(id_num))

        email = "aaaa@stu.kau.edu.sa"  # Example email, replace with actual data retrieval logic
        self.lineEdit_Email.setText(email)

        program = "Computer Engineering"  # Example program, replace with actual data retrieval logic
        self.lineEdit_Program.setText(program)

        currentLevel = 3  # Example level, replace with actual data retrieval logic
        self.lineEdit_CurrentLevel.setText(str(currentLevel))


    def goBack(self):
        # Hide this window and show student page (reuse instance via parent)
        self.hide()
        self.parent().show()  # Access parent (StudentPage) and show it







#================= Initialize the app =====================#
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())