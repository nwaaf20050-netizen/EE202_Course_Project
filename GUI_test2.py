from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow,QStackedWidget ,QApplication

import sys ,time

import loginvalidation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI_MainWindows.ui", self)

        self.stackedWidget.setCurrentIndex(0)


        #Main Window===========================
        self.pushButton_Home.clicked.connect(self.openHome)
        self.pushButton_Logout.clicked.connect(self.mainLogout)

        #Login Page============================
        self.pushButton_Login.clicked.connect(self.loginButtonPressed)
        self.pushButton_Close.clicked.connect(self.closeApp)

        #Student Page=========================
        self.commandLinkButton_StudentProfile.clicked.connect(self.open_studentProfile)
        self.commandLinkButton_CompletedCourses.clicked.connect(self.open_studentTranscript)
        self.commandLinkButton_CourseRegistration.clicked.connect(self.open_studentCourseRegistration)
        self.commandLinkButton_Logout.clicked.connect(self.mainLogout)

        #Student Profile=================================
        self.pushButton_Back.clicked.connect(self.openHome)

        #Studen Transcript================================

        #Student Course Registration================================

    def closeEvent(self, event):
        # Override to quit the app when the main window closes (e.g., via X button)
        self.clearLoginText()
        self.clearGlobalVariables()
        QApplication.quit()
        event.accept()

    #=========================Opening the pages methods================================
    def open_loginPage(self):
        self.stackedWidget.setCurrentIndex(0)
    def open_studentPage(self):
        self.stackedWidget.setCurrentIndex(1)
    def open_studentProfile(self):
        self.displayInformation()
        self.stackedWidget.setCurrentIndex(2)
    def open_studentTranscript(self):
        self.stackedWidget.setCurrentIndex(3)
    def open_studentCourseRegistration(self):
        # self.stackedWidget.setCurrentIndex(4)
        pass
    def open_adminPage(self):
        pass
    def open_adminProfile(self):
        pass
    def open_addStudent(self):
        pass
    def open_addAdmin(self):
        pass
    def open_addFaculty(self):
        pass
    def open_addCourse(self):
        pass
    def open_addSchedule(self):
        pass
    def open_facultyPage(self):
        pass



    #=============================LoginPage========================================


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
            
            if instance_status == 'student':

                instance_ID_number = instance_object.student_id
                instance_name = instance_object.name
                instance_email = instance_object.email
                instance_program = instance_object.program
                instance_level =  instance_object.level


                self.open_studentPage()
            
            elif instance_status == 'admin':

                instance_ID_number = instance_object.student_id
                instance_name = instance_object.name
                instance_email = instance_object.email



                self.open_adminPage()

            else:
                self.lineEdit_Username.clear()
                self.lineEdit_Password.clear()
                self.lineEdit_Username.setPlaceholderText("Invalid login, try again.")
                self.lineEdit_Password.setPlaceholderText("Invalid login, try again.")
                print("Invalid login status")
        except Exception as e:
            self.lineEdit_Username.clear()
            self.lineEdit_Password.clear()
            self.lineEdit_Username.setPlaceholderText("Login error, try again.")
            self.lineEdit_Password.setPlaceholderText("Login error, try again.")
            print(f"Login failed: {e}")
        
#========================= Main App Prperties ================================
    def clearGlobalVariables(self):

        # instance_data, instance_status, instance_object = None, None,None 
        # instance_ID_number, instance_name, instance_email, instance_program, instance_level = None,None,None,None,None
        pass


    def closeApp(self):
        # Properly quit the application
        self.clearLoginText()
        self.clearGlobalVariables()
        QApplication.quit()

#========================= Main Window Buttons ===============================

    def openHome(self):

        if instance_status == None or instance_status != 'student' or instance_status != 'admin' or instance_status != 'faculty':
            pass
        elif instance_status == 'student':
            self.open_studentPage()

        elif instance_status == 'admin':
            self.open_adminPage()

        elif instance_status == 'faculty':
            self.open_facultyPage()
        else:
            print("Unwanted variable from instance_status at openHome method")

    def mainLogout(self):
        self.clearGlobalVariables()
        self.clearLoginText()
        self.open_loginPage()

#========================= Student Profile ================================
    def displayInformation(self):

        # Example name, replace with actual data retrieval logic
        self.lineEdit_Name.setText(instance_name)
        
        self.lineEdit_IDNumber.setText(str(instance_ID_number))

        self.lineEdit_Email.setText(instance_email)

        self.lineEdit_Program.setText(instance_program)

        self.lineEdit_CurrentLevel.setText(str(instance_level))



    
        











    














































#==========================================================================

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
