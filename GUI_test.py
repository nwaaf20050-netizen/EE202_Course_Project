from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
#================= Nawaf_Addition =====================#
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from RegistrationSystemClass import RegistrationSystem
from NewStudentsClass import Student
from NewCourseClass import Course
from TimeBuilder import Schedule, ScheduleSystem
#================= Nawaf_Addition =====================#
import loginvalidation
import time
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
        #================= Nawaf_Addition =====================#
        self.adminPage = AdminPage(parent=self)
        #================= Nawaf_Addition =====================#

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
            #================= Nawaf_Addition =====================#
                self.hide()
                self.studentPage.show()
            #================= Nawaf_Addition =====================#
            
            elif instance_status == 'admin':
                instance_ID_number = instance_object.admin_id
                instance_name = instance_object.name
                instance_email = instance_object.email
            #================= Nawaf_Addition =====================#
                self.hide()
                self.adminPage.show()
            #================= Nawaf_Addition =====================#


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
        #================= Nawaf_Addition =====================#
        # self.hide()
        # self.studentPage.show()
        #================= Nawaf_Addition =====================#
                

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
        #================= Nawaf_Addition =====================#
        self.showTranscripts = ViewTranscripts(parent=self) # Parent: ViewTranscripts
        #================= Nawaf_Addition =====================#
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
        self.hide()
        self.showTranscripts.show_transcripts()
        self.showTranscripts.show()
        # Implement completed courses functionality here


    def openCourseRegistration(self):
        pass # Implement course registration functionality here


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

#================= Nawaf_Addition =====================#

#================= Course Registration =====================#
class CourseRegistration(QMainWindow):

    def __init__(self, parent=None):

        super(CourseRegistration, self).__init__(parent)  # Set parent for proper parenting
        # Load the UI file with error handling
        try:
            uic.loadUi("GUI_CourseRegistration.ui", self)
        except FileNotFoundError:
            print("Error: GUI_CourseRegistration.ui not found. Please ensure the file exists.")
            sys.exit(1)
        
        self.setWindowTitle("Course Registration")
    def goBack(self):
        # Hide this window and show student page (reuse instance via parent)
        self.hide()
        self.parent().show()  # Access parent (StudentPage) and show it

    def registerCourse(self):
        pass

#================= View Transcripts =====================#
class ViewTranscripts(QMainWindow,):

    def __init__(self, parent=None):

        super(ViewTranscripts, self).__init__(parent)  # Set parent for proper parenting
        # Load the UI file with error handling
        try:
            uic.loadUi("GUI_ViewTranscripts.ui", self)
        except FileNotFoundError:
            print("Error: GUI_ViewTranscripts.ui not found. Please ensure the file exists.")
            sys.exit(1)
        self.registration=RegistrationSystem()
        self.setWindowTitle("View Transcripts")
        self.pushButton_Back.clicked.connect(self.goBack)
        


    def show_transcripts(self):
        
        results=self.registration.view_transcript(instance_ID_number)
        model = QStandardItemModel()
        
        model.setHorizontalHeaderLabels(["Course Code", "Grade","Credit Hours" ])
        for row in results:
            
            items = [QStandardItem(str(x)) for x in row]
            model.appendRow(items)

        self.TextBr.setModel(model)



        # self.TextBr.setText(str(self.registration.view_transcript(instance_ID_number)))
        # print(self.registration.view_transcript(str(instance_ID_number)))

    def goBack(self):
        self.hide()
        self.parent().show()

class AdminPage(QMainWindow):
    def __init__(self, parent=None):
        super(AdminPage, self).__init__(parent)
        try:
            uic.loadUi("Admin's main page.ui", self)
        except FileNotFoundError:
            print("Error: Admin's main page.ui not found. Please ensure the file exists.")
        self.setWindowTitle("Admin Page")
        self.AdminProfile = AdminProfile(parent=self)
        self.addStudent = add_student(parent=self)
        # self.addFaculty = add_faculty(parent=self)
        self.addCourse = add_course2(parent=self)
        self.addSchdules = addSchdules(parent=self)
        # Connect buttons to their functions
        self.pushButton_AddStudent.clicked.connect(self.add_student)
        self.pushButton_AddCourse.clicked.connect(self.add_Course)
        self.pushButton_AddFaculty.clicked.connect(self.add_faculty)
        self.pushButton_AddSchedule.clicked.connect(self.addition_schdules)
        self.pushButton_AdminProfile.clicked.connect(self.adminProfile)
       
    #     self.pushButton_Logout.clicked.connect(self.logout)
    # def logout(self):
    #     self.hide()
    #     self.parent().show()


    def adminProfile(self):
        self.hide()
        self.AdminProfile.displayInformation()
        self.AdminProfile.show()


    def addition_schdules(self):
        self.hide()
        self.addSchdules.show()

    def add_student(self):
        self.hide()
        # self.addStudent.add_student()
        self.addStudent.show()

    def add_Course(self):
        self.hide()
        # self.addCourse.addition_course()
        self.addCourse.show()

    def add_faculty(self):
        pass

class AdminProfile(QMainWindow):
    def __init__(self, parent=None):
        super(AdminProfile, self).__init__(parent)
        try:
            uic.loadUi("GUI_AdminProfile.ui", self)
        except FileNotFoundError:
            print("Error: GUI_AdminProfile.ui not found. Please ensure the file exists")
            sys.exit(1)
        self.setWindowTitle("Admin Profile")
        self.pushButton_Back.clicked.connect(self.goBack)
    def goBack(self):
        self.hide()
        self.parent().show()


    def displayInformation(self):
        list_first_and_last_name=instance_name.split(" ")

        self.lineEdit_FirstName.setText(list_first_and_last_name[0])
        self.lineEdit_LastName.setText(list_first_and_last_name[1])
        self.lineEdit_IDNumber.setText(str(instance_ID_number))
        self.lineEdit_Email.setText(instance_email)


class add_student(QMainWindow):
    def __init__(self, parent=None):
        super(add_student, self).__init__(parent)
        try:
            uic.loadUi("Student.ui", self)
        except FileNotFoundError:
            print("Error: Student.ui not found. Please ensure the file exists")
            sys.exit(1)

        self.setWindowTitle("Add Student")
        self.pushButton_Back.clicked.connect(self.goBack)
        self.pushButton_Add.clicked.connect(self.add_student)
        self.registration=RegistrationSystem()

    def goBack(self):
        self.hide()
        self.parent().show()


    def add_student(self):
        student_id = self.lineEdit_StudentID.text()
        name = self.lineEdit_FullName.text()
        email = self.lineEdit_Email.text().strip()
        password = self.lineEdit_Password.text()
        program = self.comboBox_Major.currentText()
        level = str(self.comboBox_Level.currentText())
        student = Student(student_id, name, email, password, program, level)
        self.registration.add_student(student)
        self.result.setText("Student added successfully")


# class add_faculty(QMainWindow):
#     def __init__(self, parent=None):
#         super(add_faculty, self).__init__(parent)
#         try:
#             uic.loadUi("Faculty.ui", self)
#         except FileNotFoundError:
#             print("Error: Faculty.ui not found. Please ensure the file exists")
#             sys.exit(1)
        
#         self.setWindowTitle("Add Faculty")
#         self.pushButton_Back.clicked.connect(self.goBack)
#         self.pushButton_Add.clicked.connect(self.add_faculty)
#     def goBack(self):
#         self.hide()
#         self.parent().show()
#     def add_faculty(self):
#         name=self.lineEdit_Name.text()
#         email=self.lineEdit_Email.text()
#         password=self.lineEdit_Password.text() 
#         ID= self.lineEdit_ID.text()
#         pass


class add_course2(QMainWindow):
        def __init__(self, parent=None):
            super(add_course2, self).__init__(parent)
            try:
                uic.loadUi("GUI_AddingNewCourse.ui", self)
            except FileNotFoundError:
                print("Error: GUI_AddingNewCourse.ui not found. Please ensure the file exists")
                sys.exit(1)
            self.registration=RegistrationSystem()
            self.setWindowTitle("Add Course")
            self.pushButton_Back.clicked.connect(self.goBack)
            self.pushButton_AddCourse.clicked.connect(self.addition_course)
        def goBack(self):
            self.hide()
            self.parent().show()

        def addition_course(self):
            course_code = self.lineEdit_CourseCode.text()
            course_name = self.lineEdit_CourseName.text()
            credit_hours = (self.lineEdit_CourseCredit.text())
            lecture_hours = (self.lineEdit_LectureHours.text())
            lab_hours = (self.lineEdit_LabHours.text())
            prerequisites = self.lineEdit_Prerequisites.text()
            max_capacity = (self.lineEdit_MaxCapacity.text())
            level = (self.comboBox_Level.currentText())
            program = []
            if self.checkBox_Communication.isChecked():
                program.append(self.checkBox_Communication.text())
            if self.checkBox_Computer.isChecked():
                program.append(self.checkBox_Computer.text())
            if self.checkBox_Power.isChecked():
                program.append(self.checkBox_Power.text())    
            if self.checkBox_Biomedical.isChecked():
                program.append(self.checkBox_Biomedical.text())
            
            course = Course(course_code, course_name, int(credit_hours), int(lecture_hours), int(lab_hours), prerequisites, int(max_capacity),program , int(level))
            self.registration.add_course(course)

class addSchdules(QMainWindow):
    def __init__(self, parent=None):
        super(addSchdules, self).__init__(parent)
        try:
            uic.loadUi("GUI_Schdules.ui", self)
        except FileNotFoundError:
            print("Error: GUI_Schdules.ui not found. Please ensure the file exists")
            sys.exit(1)
        self.setWindowTitle("Add Schedule")
        self.pushButton_Back.clicked.connect(self.goBack)
        self.pushButton_Add.clicked.connect(self.adding_schedule)
        self.schudules=ScheduleSystem()
    def goBack(self):
        self.hide()
        self.parent().show()
    
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



        



                
#================= Nawaf_Addition =====================#





#================= Initialize the app =====================#
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())