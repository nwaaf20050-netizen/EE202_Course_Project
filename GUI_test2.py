from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow,QStackedWidget ,QApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem


import sys ,time

import loginvalidation
from RegistrationSystemClass import RegistrationSystem
from NewStudentsClass import Student
from NewCourseClass import Course
from TimeBuilder import Schedule, ScheduleSystem


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

        #Studen Transcript================================
        self.registration=RegistrationSystem()
        
        #Student Course Registration================================

        #Admin Main Page ======================================
        self.pushButton_AdminProfile.clicked.connect(self.open_adminProfile)
        self.pushButton_AddSchedule.clicked.connect(self.open_addSchedule)
        self.pushButton_AddStudent.clicked.connect(self.open_addStudent)     
        self.pushButton_AddCourse.clicked.connect(self.open_addCourse)
        self.pushButton_AddFaculty.clicked.connect(self.open_addFaculty)

        #AdminProfile =============================================

        #Admin Schedule ==========================================
        self.pushButton_AddStudent_2.clicked.connect(self.adding_schedule)
        self.schudules=ScheduleSystem()

        #Adding Students ==========================================
        self.pushButton_Add.clicked.connect(self.add_student)
        # self.registration=RegistrationSystem()

        #Adding New Course ======================================

        #The Faculty =========================================

        #Log===============================
        print("UI loaded, stackedWidget current index:", self.stackedWidget.currentIndex())
        print("Available widgets:", [self.stackedWidget.widget(i).objectName() for i in range(self.stackedWidget.count())])

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
        self.displayStudentInformation()
        self.stackedWidget.setCurrentIndex(2)
    def open_studentTranscript(self):
        self.show_transcripts()
        self.stackedWidget.setCurrentIndex(3)
    def open_studentCourseRegistration(self):
        self.stackedWidget.setCurrentIndex(4)
    def open_adminPage(self):
        self.stackedWidget.setCurrentIndex(5)
    def open_adminProfile(self):
        self.showAdminProfile()
        self.stackedWidget.setCurrentIndex(6)
    def open_addStudent(self):
        self.stackedWidget.setCurrentIndex(8)
    def open_addAdmin(self):
        pass
    def open_addFaculty(self):
        self.stackedWidget.setCurrentIndex(10)
    def open_addCourse(self):
        self.stackedWidget.setCurrentIndex(9)
    def open_addSchedule(self):
        self.stackedWidget.setCurrentIndex(7)
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

                instance_ID_number = instance_object.admin_id
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

        global instance_data, instance_status, instance_object
        global instance_ID_number, instance_name, instance_email
        global instance_program, instance_level
        instance_data = None
        instance_status = None
        instance_object = None
        instance_ID_number = None
        instance_name = None
        instance_email = None
        instance_program = None
        instance_level = None
        pass


    def closeApp(self):
        # Properly quit the application
        self.clearLoginText()
        self.clearGlobalVariables()
        QApplication.quit()

#========================= Main Window Buttons ===============================

    def openHome(self):
        if instance_status == 'student':
            self.open_studentPage()
        elif instance_status == 'admin':
            self.open_adminPage()
        elif instance_status == 'faculty':
            self.open_facultyPage()
        else:
            self.open_loginPage()  # Fallback to login if status is invalid


    def mainLogout(self):
        self.clearGlobalVariables()
        self.clearLoginText()
        self.open_loginPage()

#========================= Student Profile ================================
    def displayStudentInformation(self):

        # Example name, replace with actual data retrieval logic
        self.lineEdit_Name.setText(instance_name)
        
        self.lineEdit_IDNumber.setText(str(instance_ID_number))

        self.lineEdit_Email.setText(instance_email)

        self.lineEdit_Program.setText(instance_program)

        self.lineEdit_CurrentLevel.setText(str(instance_level))

#==========================Student Transcript ==================================

        
    def show_transcripts(self):

        if instance_ID_number is None:
            print("No student logged in, returning")
            return
        try:
            results = self.registration.view_transcript(instance_ID_number)
            # print("Transcript results:", results)
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(["Course Code", "Grade", "Credit Hours"])
            for row in results:
                if len(row) == 3:

                    items = [QStandardItem(str(x)) for x in row]
                    model.appendRow(items)
            self.tableView_Transcripts.setModel(model)
            # print("Model set on tableView_Transcripts")
        except Exception as e:
            print(f"Error in show_transcripts: {e}")





#====================================================================================================
#====================================================================================================


#====================================================================================================
#====================================================================================================



#======================================Admin Profile=====================================================

    def showAdminProfile(self):

        self.lineEdit_IDNumber_2.setText(str(instance_ID_number))
        self.lineEdit_Name_2.setText(instance_name)
        self.lineEdit_Email_2.setText(instance_email)


#=======================================Adding Schedule ==============================================
    def adding_schedule(self):
        self.course_code=self.lineEdit_CourseCode.text()
        self.numSections=self.lineEdit_numSections.text()
        self.start=self.timeEdit_start.time().toString("HH:mm")
        self.end=self.timeEdit_end.time().toString("HH:mm") 
        print(self.start)
        print(self.end)
        self.lecture_type=self.comboBox_LectureType.currentText()
        
        if self.lineEdit_InstructorName.text() =="":
            self.instructor_name=None
        else:
            self.instructor_name=self.lineEdit_InstructorName.text()

        if self.lineEdit_place.text() =="":
            self.place=None
        else:
            self.place=self.lineEdit_place.text()

        if self.lineEdit_room.text() =="":
            self.room= None
        else:
            self.room=self.lineEdit_room.text()
        self.days=[]
        if self.checkBox_mon.isChecked():
            self.days.append(self.checkBox_mon.text())
        if self.checkBox_tue.isChecked():
            self.days.append(self.checkBox_tue.text())
        if self.checkBox_wed.isChecked():
            self.days.append(self.checkBox_wed.text())
        if self.checkBox_thurs.isChecked():
            self.days.append(self.checkBox_thurs.text()) 
        if self.checkBox_sun.isChecked():
            self.days.append(self.checkBox_sun.text())
        Schedule_oject=Schedule(self.course_code,self.numSections,self.start,self.end,self.lecture_type,self.instructor_name,self.place,self.room,self.days)
        self.schudules.add_schedule(Schedule_oject)

    
#=============================Add Students Page ========================================

    def add_student(self):
        student_id = self.lineEdit_AddStudentID.text()
        name = self.lineEdit_AddFullName.text()
        email = self.lineEdit_Email.text().strip()
        password = self.lineEdit_AddPassword.text()
        program = self.comboBox_Major.currentText()
        level = str(self.comboBox_Level.currentText())
        student = Student(student_id, name, email, password, program, level)
        self.registration.add_student(student)
        self.result.setText("Student added successfully")










    














































#==========================================================================

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
