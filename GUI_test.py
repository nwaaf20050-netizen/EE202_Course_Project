from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow


import loginvalidation

import sys
import time

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


    def clearLoginText(self):
        self.lineEdit_Username.setPlaceholderText("")
        self.lineEdit_Password.setPlaceholderText("")

    

    def loginButtonPressed(self):

        username = self.lineEdit_Username.text()
        password = self.lineEdit_Password.text()

        print(f"Username: {username}, Password: {password}")
        
        # login = loginvalidation.LoginSystem.login(username, password)
        global instance_data , instance_status , instance_object
        global instance_ID_number , instance_name , instance_email
        global instance_program ,instance_level
 
        
        try:
            instance_data = loginvalidation.system.login(username, password)
            instance_status = instance_data[0]
            instance_object = instance_data[1]

            print(instance_data)
            print(instance_status)


            if instance_status == 'student':


                instance_ID_number = instance_object.student_id
                instance_name = instance_object.name
                instance_email = instance_object.email
                instance_program = instance_object.program
                instance_level =  instance_object.level

                self.hide()
                self.studentPage.show()

            
            elif instance_status == 'admin':
                instance_ID_number = instance_object.admin_id
                instance_name = instance_object.name
                instance_email = instance_object.email

            elif instance_data != 'student' or instance_data != 'admin':
                print('invalid returned')
                self.lineEdit_Username.clear()
                self.lineEdit_Password.clear()

                self.lineEdit_Username.setPlaceholderText("Invalid login, try again.")
                self.lineEdit_Password.setPlaceholderText("Invalid login, try again.")
                print(f"Login failed: {e}")

            
            
        except Exception as e:
            self.lineEdit_Username.clear()
            self.lineEdit_Password.clear()

            self.lineEdit_Username.setPlaceholderText("Invalid login, try again.")
            self.lineEdit_Password.setPlaceholderText("Invalid login, try again.")
            print(f"Login failed: {e}")
            
            return


                

        # instance_name = loginvalidation.system.login(username, password)[1]
        # instance_email = loginvalidation.system.login(username, password)[2]
        # instance_program = loginvalidation.system.login(username, password)[3]
        # instance_level = loginvalidation.system.login(username, password)[4]

        
        # print(instance_ID_number, "\n", instance_name, "\n", instance_email, "\n", instance_program, "\n", instance_level)
        # print(login)


        

        # Hide login and show student page (reuse instances)

    def clearGlobalVariables(self):
        instance_data, instance_status, instance_object = None, None, None
        instance_ID_number, instance_name, instance_email, instance_program, instance_level = None, None, None, None, None


    def closeApp(self):
        # Properly quit the application
        self.clearLoginText
        self.clearGlobalVariables
        QApplication.quit()


    def closeEvent(self, event):
        # Override to quit the app when the main window closes (e.g., via X button)
        self.clearLoginText
        self.clearGlobalVariables
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


        # name = "Ahmed Afifi"  # Example name, replace with actual data retrieval logic
        # self.lineEdit_Name.setText(name)
        
        # id_num = 2222222  # Example ID, replace with actual data retrieval logic
        # self.lineEdit_IDNumber.setText(str(id_num))

        # email = "aaaa@stu.kau.edu.sa"  # Example email, replace with actual data retrieval logic
        # self.lineEdit_Email.setText(email)

        # program = "Computer Engineering"  # Example program, replace with actual data retrieval logic
        # self.lineEdit_Program.setText(program)

        # currentLevel = 3  # Example level, replace with actual data retrieval logic
        # self.lineEdit_CurrentLevel.setText(str(currentLevel))
        


        # Example name, replace with actual data retrieval logic
        self.lineEdit_Name.setText(instance_name)
        
        self.lineEdit_IDNumber.setText(str(instance_ID_number))

        self.lineEdit_Email.setText(instance_email)

        self.lineEdit_Program.setText(instance_program)

        self.lineEdit_CurrentLevel.setText(str(instance_level))

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