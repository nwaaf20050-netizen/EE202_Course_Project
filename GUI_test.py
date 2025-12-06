# GUI_test.py
from platform import system
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from RegistrationSystemClass import RegistrationSystem
from NewStudentsClass import Student
from NewCourseClass import Course
from FacultyClass import Faculty
from TimeBuilder import Schedule, ScheduleSystem
from PyQt5.QtCore import QLocale
from AnalyticsModule import Analytics
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
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
        self.facultyPage = FacultyPage(parent=self)
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
        global instance_course_preferences, instance_availability
 
        
        try:
            instance_data = loginvalidation.system.login(username, password)
            instance_status = instance_data[0]
            instance_object = instance_data[1]

            print(instance_data)
            print(instance_status)

            # student login
            if instance_status == 'student':


                instance_ID_number = instance_object.student_id
                instance_name = instance_object.name
                instance_email = instance_object.email
                instance_program = instance_object.program
                instance_level =  instance_object.level

                self.hide()
                self.studentPage.show()

            # admin login
            elif instance_status == 'admin':
                instance_ID_number = instance_object.admin_id
                instance_name = instance_object.name
                instance_email = instance_object.email
           
                self.hide()
                self.adminPage.show()
            # faculty login
            elif instance_status == 'faculty':
                instance_ID_number = instance_object.faculty_id
                instance_name=instance_object.name
                instance_email=instance_object.email
                instance_course_preferences=instance_object.course_preferences
                instance_availability=instance_object.availability
                # instance_assigned_courses=instance_object.assigned_courses
                self.hide()
                self.facultyPage.show()
            

            # invalid login
            elif instance_data != 'student' or instance_data != 'admin' or instance_data != 'faculty':
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

    # clear global variables
    def clearGlobalVariables(self):
        instance_data, instance_status, instance_object = None, None, None
        instance_ID_number, instance_name, instance_email, instance_program, instance_level = None, None, None, None, None

    # Close the application properly
    def closeApp(self):
        # Properly quit the application
        self.clearLoginText
        self.clearGlobalVariables
        QApplication.quit()

    # Override the close event to ensure proper cleanup
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
        self.showTranscripts = ViewTranscripts(parent=self) # Parent: ViewTranscripts
        self.courseRegistration = CourseRegistration(parent=self) # Parent: CourseRegistration
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
        self.hide()
        self.courseRegistration.show_data()
        self.courseRegistration.show()
        
    
        # Implement course registration functionality here


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

#================= Course Registration =====================#
class CourseRegistration(QMainWindow):

    def __init__(self, parent=None):

        super(CourseRegistration, self).__init__(parent)  # Set parent for proper parenting
        # Load the UI file with error handling
        try:
            uic.loadUi("GUI_Student Course Registration.ui", self)
        except FileNotFoundError:
            print("Error: GUI_Student Course Registration.ui not found. Please ensure the file exists.")
            sys.exit(1)
        self.registraion=RegistrationSystem()
        self.setWindowTitle("Course Registration")
        self.pushButton_Back.clicked.connect(self.goBack)
        self.pushButton.clicked.connect(self.register)
        self.pushButton_Delete.clicked.connect(self.delete)
        


    def goBack(self):
        # Hide this window and show student page (reuse instance via parent)
        self.hide()
        self.parent().show()  # Access parent (StudentPage) and show it

    def show_data(self): # load data into tableviews

        results=self.registraion.get_available_courses(instance_ID_number)
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["course_code",
                            "course_name",
                            "credit_hours",
                            "section",
                            "days",
                            "start_time",
                            "end_time",
                            "instructor_name",
                            "place",
                            "room",
                            "enrolled_count",
                            "max_capacity" ])
        for row in results:
            
            items = [QStandardItem(str(x)) for x in row]
            model.appendRow(items)
    

        self.tableView.setModel(model)
        # registred courses
        results1=self.registraion.get_student_schedule(instance_ID_number)
        model1 = QStandardItemModel()
        
        model1.setHorizontalHeaderLabels(["course_code",
                            "course_name",
                            "credit_hours",
                            "section",
                            "days",
                            "start_time",
                            "end_time",
                            "instructor_name",
                            "place",
                            "room",
                            "enrolled_count",
                            "max_capacity"])
        for row1 in results1:
            
            items1 = [QStandardItem(str(x1)) for x1 in row1]
            model1.appendRow(items1)

        self.tableView_2.setModel(model1)
    def register(self): # register for a course
       self.code=self.lineEdit_code.text()
       self.section=self.lineEdit_section.text()
       list_of_courses=[(self.code,self.section)]
       self.registraion.register_student(instance_ID_number,list_of_courses)
       self.load_get_available_courses()
       self.load_get_student_schedule()
    def delete(self): # delete a course registration
        self.code2=self.lineEdit_code2.text()
        self.section2=self.lineEdit_section2.text()
        self.registraion.delete_register_student(instance_ID_number,self.code2,self.section2)
        self.load_get_available_courses()
        self.load_get_student_schedule()
    def load_get_available_courses(self): # load available courses into tableview

        results=self.registraion.get_available_courses(instance_ID_number) # load data into tableviews
        model = QStandardItemModel()
        # set headers
        model.setHorizontalHeaderLabels(["course_code",
                            "course_name",
                            "credit_hours",
                            "section",
                            "days",
                            "start_time",
                            "end_time",
                            "instructor_name",
                            "place",
                            "room",
                            "enrolled_count",
                            "max_capacity" ])
        for row in results:
            
            items = [QStandardItem(str(x)) for x in row]
            model.appendRow(items)
    

        self.tableView.setModel(model)
    def load_get_student_schedule(self): # load student schedule into tableview
        results1=self.registraion.get_student_schedule(instance_ID_number)
        model1 = QStandardItemModel()
        
        model1.setHorizontalHeaderLabels(["course_code",
                            "course_name",
                            "credit_hours",
                            "section",
                            "days",
                            "start_time",
                            "end_time",
                            "instructor_name",
                            "place",
                            "room",
                            "enrolled_count",
                            "max_capacity"])
        for row1 in results1:
            
            items1 = [QStandardItem(str(x1)) for x1 in row1]
            model1.appendRow(items1)

        self.tableView_2.setModel(model1)



        

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
        


    def show_transcripts(self): # load data into tableviews
        
        results=self.registration.view_transcript(instance_ID_number)
        model = QStandardItemModel()
        
        model.setHorizontalHeaderLabels(["Course Code", "Grade","Credit Hours" ]) # set headers
        for row in results:
            
            items = [QStandardItem(str(x)) for x in row]
            model.appendRow(items)

        self.TextBr.setModel(model) # set model to tableview


    def goBack(self): # Hide this window and show student page (reuse instance via parent)
        self.hide()
        self.parent().show()
#================= AdminPage =====================#
class AdminPage(QMainWindow): 
    def __init__(self, parent=None):
        super(AdminPage, self).__init__(parent)
        try:
            uic.loadUi("Admin's main page.ui", self)
        except FileNotFoundError:
            print("Error: Admin's main page.ui not found. Please ensure the file exists.")
        self.setWindowTitle("Admin Page")
        self.AdminProfile = AdminProfile(parent=self) # Parent: AdminPage
        self.addStudent = add_student(parent=self) # Parent: add_student
        self.addFaculty = add_faculty(parent=self) # Parent: add_faculty
        self.addCourse = add_course2(parent=self) # Parent: add_course2
        self.addSchdules = addSchdules(parent=self) # Parent: addSchdules
        self.ShowEnrollment=Show_Erollment_data(parent=self) # Parent: Show_Erollment_data
        self.showFaculty=Show_Faculty_Preferences(parent=self) # Parent: Show_Faculty_Preferences
        self.assignFaculty=AssignFaculty(parent=self) # Parent: AssignFaculty
        # Connect buttons to their functions
        self.pushButton_AddStudent.clicked.connect(self.add_student) # Connect to add_student window
        self.pushButton_AddCourse.clicked.connect(self.add_Course) # Connect to add_course window
        self.pushButton_AddFaculty.clicked.connect(self.add_faculty) # Connect to add_faculty window
        self.pushButton_AddSchedule.clicked.connect(self.addition_schdules) # Connect to addSchdules window
        self.pushButton_AdminProfile.clicked.connect(self.adminProfile) # Connect to adminProfile window
        self.pushButton_Enrollment.clicked.connect(self.Show_Enrollment) # Connect to ShowEnrollment window
        self.pushButton_Preferences.clicked.connect(self.Show_Faculty) # Connect to Show_Faculty_Preferences window
        self.pushButton_Logout.clicked.connect(self.logout) # Connect to logout function
        self.pushButton_Assign.clicked.connect(self.assignFaculty_show) # Connect to assignFaculty window
    def logout(self): # Hide this window and show main app (reuse instance via parent)
        self.hide() # Hide AdminPage window
        self.parent().show() # Access parent (MainApp) and show it


    def adminProfile(self):# Hide this window and show adminProfile (reuse instance)
        self.hide() 
        self.AdminProfile.displayInformation() # display admin information
        self.AdminProfile.show()


    def addition_schdules(self): # Hide this window and show addSchdules (reuse instance)
        self.hide()
        self.addSchdules.show()

    def add_student(self): # Hide this window and show add_student (reuse instance)
        self.hide()
        self.addStudent.show()

    def add_Course(self): # Hide this window and show add_course (reuse instance)
        self.hide()
        self.addCourse.show()

    def add_faculty(self): # Hide this window and show add_faculty (reuse instance)
        self.hide()
        self.addFaculty.show()
    def Show_Enrollment(self):  # Hide this window and show ShowEnrollment (reuse instance)
        self.hide()
        self.ShowEnrollment.show()
    def Show_Faculty(self): # Hide this window and show Show_Faculty_Preferences (reuse instance)
        self.hide()
        self.showFaculty.show_faculty_preferences()
        self.showFaculty.show()
    def assignFaculty_show(self): # Hide this window and show assignFaculty (reuse instance)
        self.hide()
        self.assignFaculty.load_data()
        self.assignFaculty.show()



# ================= Admin Profile Window =====================#
class AdminProfile(QMainWindow): # Admin Profile Window
    def __init__(self, parent=None):
        super(AdminProfile, self).__init__(parent)
        try:
            uic.loadUi("GUI_AdminProfile.ui", self) # Load the UI file with error handling
        except FileNotFoundError:
            print("Error: GUI_AdminProfile.ui not found. Please ensure the file exists")
            sys.exit(1)
        self.setWindowTitle("Admin Profile")
        self.pushButton_Back.clicked.connect(self.goBack)
    def goBack(self): # Hide this window and show admin page (reuse instance via parent)
        self.hide()
        self.parent().show()


    def displayInformation(self): # Display admin information
        list_first_and_last_name=instance_name.split(" ")

        self.lineEdit_FirstName.setText(list_first_and_last_name[0])
        self.lineEdit_LastName.setText(list_first_and_last_name[1])
        self.lineEdit_IDNumber.setText(str(instance_ID_number))
        self.lineEdit_Email.setText(instance_email)

#================= Add Student Window =====================#
class add_student(QMainWindow): # Add Student Window
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

    def goBack(self): # Hide this window and show admin page (reuse instance via parent)
        self.hide()
        self.parent().show()


    def add_student(self):  # Add student to the system
        student_id = self.lineEdit_StudentID.text()
        name = self.lineEdit_FullName.text()
        email = self.lineEdit_Email.text().strip()
        password = self.lineEdit_Password.text()
        program = self.comboBox_Major.currentText()
        level = str(self.comboBox_Level.currentText())
        student = Student(student_id, name, email, password, program, level)
        self.registration.add_student(student)
        self.result.setText("Student added successfully")


class add_faculty(QMainWindow): # Add Faculty Window
    def __init__(self, parent=None):
        super(add_faculty, self).__init__(parent)
        try:
            uic.loadUi("GUI_add_Faculty.ui", self)
        except FileNotFoundError:
            print("Error: GUI_add_Faculty.ui not found. Please ensure the file exists")
            sys.exit(1)
        self.registration=RegistrationSystem()
        self.setWindowTitle("Add Faculty")
        self.pushButton_Back.clicked.connect(self.goBack)
        self.pushButton_Add.clicked.connect(self.add_faculty)
    def goBack(self): # Hide this window and show admin page (reuse instance via parent)
        self.hide()
        self.parent().show()
    def add_faculty(self): # Add faculty to the system
        name=self.lineEdit_Name.text()
        email=self.lineEdit_email.text()
        password=self.lineEdit_password.text() 
        faculty_id= self.lineEdit_id.text()
        faculty=Faculty(faculty_id,name,email,password)
        self.registration.add_faculty(faculty)

        
        


class add_course2(QMainWindow): # Add Course Window
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
        def goBack(self):   # Hide this window and show admin page (reuse instance via parent)
            self.hide()
            self.parent().show()

        def addition_course(self): # Add course to the system
            course_code = self.lineEdit_CourseCode.text()
            course_name = self.lineEdit_CourseName.text()
            credit_hours = (self.lineEdit_CourseCredit.text())
            lecture_hours = (self.lineEdit_LectureHours.text())
            lab_hours = (self.lineEdit_LabHours.text())
            prerequisites = self.lineEdit_Prerequisites.text()
            max_capacity = (self.lineEdit_MaxCapacity.text())
            level = (self.comboBox_Level.currentText())
            program = []
            if self.checkBox_Communication.isChecked():     # Check if Communication program is selected
                program.append(self.checkBox_Communication.text())
            if self.checkBox_Computer.isChecked():    # Check if Computer program is selected
                program.append(self.checkBox_Computer.text())
            if self.checkBox_Power.isChecked():   # Check if Power program is selected
                program.append(self.checkBox_Power.text())    
            if self.checkBox_Biomedical.isChecked():  # Check if Biomedical program is selected
                program.append(self.checkBox_Biomedical.text())
            
            course = Course(course_code, course_name, int(credit_hours), int(lecture_hours), int(lab_hours), prerequisites, int(max_capacity),program , int(level))
            self.registration.add_course(course) # Add course to the system
#================= Schedule Window =====================#
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
        english_locale = QLocale(QLocale.English)
        self.timeEdit_start.setLocale(english_locale)
        self.timeEdit_end.setLocale(english_locale)
        self.timeEdit_start.setDisplayFormat("HH:mm")
        self.timeEdit_end.setDisplayFormat("HH:mm")

    def goBack(self): # Hide this window and show admin page (reuse instance via parent)
        self.hide()
        self.parent().show()
    
    def adding_schedule(self): # Add schedule to the system
        self.course_code=self.lineEdit_CourseCode.text()
        self.numSections=self.lineEdit_numSections.text()
        
        self.start=self.timeEdit_start.text()
        self.end=self.timeEdit_end.text()

    
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

        if self.checkBox_sun.isChecked():
            self.days.append('Sun')

        if self.checkBox_mon.isChecked():
            self.days.append('Mon')

        if self.checkBox_tue.isChecked():
            self.days.append('Tue')

        if self.checkBox_wed.isChecked():
            self.days.append('Wed')

        if self.checkBox_thurs.isChecked():
            self.days.append('Thu')
        Schedule_oject=Schedule(self.course_code,int(self.numSections),self.start,self.end,self.days,self.lecture_type,self.instructor_name,self.place,self.room,)
        self.schudules.add_schedule(Schedule_oject)
#================= Show Enrollment Data Window =====================#
class Show_Erollment_data(QMainWindow): 
    def __init__(self, parent=None):
        super(Show_Erollment_data, self).__init__(parent)
    
        try:
            uic.loadUi("GUI_AnalyticsModule.ui", self)
        except FileNotFoundError:
            print("Error: GUI_AnalyticsModule.ui not found. Please ensure the file exists")
        self.setWindowTitle("Show Enrollment")
        self.registration=RegistrationSystem()
        self.analytics = Analytics(self.registration)
        self.canvas = None
        
        self.btn_showChart.clicked.connect(self.display_fill_rate_chart)
        self.pushButton_Back.clicked.connect(self.goBack)    
        
        
    def display_fill_rate_chart(self): # Display fill rate chart
        course_code=self.lineEdit_courseCode.text()
        # Get the filled canvas from analytics module
        canvas = self.analytics.calculate_section_chart(course_code)
        if canvas is None:
            print("No data available for chart visualization")
            self.label_M.setText("No data available for chart visualization")
            return
        
        # Remove old canvas if exists (Refresh)
        if self.canvas:
            self.chartFrame.layout().removeWidget(self.canvas)
            self.canvas.deleteLater()
        
        self.canvas = canvas
        
        # If frame has no layout -> create one
        if not self.chartFrame.layout():
            layout = QVBoxLayout(self.chartFrame)
            self.chartFrame.setLayout(layout)
        else:
            layout = self.chartFrame.layout()
        
        # Add Toolbar + Chart to layout
        toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        
        # Redraw chart
        self.canvas.draw()
        self.label_M.setText("The graph was successfully drawn")
    def goBack(self): # Hide this window and show admin page (reuse instance via parent)
        self.hide()
        self.parent().show()
        self.label_M.setText("")
        self.lineEdit_courseCode.setText("")
        self.canvas = None
#================= Show Faculty Preferences Window =====================#
class Show_Faculty_Preferences(QMainWindow): 
    def __init__(self, parent=None):
        super(Show_Faculty_Preferences, self).__init__(parent)
        try:
            uic.loadUi("GUI_Show_Faculty_Preferences.ui", self)
        except FileNotFoundError:   
            print("Error: GUI_Show_Faculty_Preferences.ui not found. Please ensure the file exists")
            sys.exit(1)
        self.setWindowTitle("Show Faculty Preferences")
        self.registration=RegistrationSystem()
        self.pushButton_Back.clicked.connect(self.goBack)
    def goBack(self): # Hide this window and show admin page (reuse instance via parent)
        self.hide()
        self.parent().show()
    def show_faculty_preferences(self): # load data into tableviews
        results=self.registration.show_all_prefreferences()
        model = QStandardItemModel()
        print(results)

        model.setHorizontalHeaderLabels(["faculty_id","name","availability","assigned_courses","course_preferences" ])

        for row in results:
            
            items = [QStandardItem(str(x)) for x in row]
            model.appendRow(items)

        self.tableView_Preferences.setModel(model)
#================= Assign Faculty Window =====================#
class AssignFaculty(QMainWindow): 
    def __init__(self, parent=None):
        super(AssignFaculty, self).__init__(parent)
        try:
            uic.loadUi("GUI_Assign_Faculty.ui",self)
        except FileNotFoundError:   
            print("Error: GUI_Assign_Faculty.ui not found. Please ensure the file exists")
            sys.exit(1)
        self.setWindowTitle("Assign Facultys")
        self.registration=RegistrationSystem()
        self.pushButton_Back.clicked.connect(self.goBack)
        self.pushButton_Assign.clicked.connect(self.assign_faculty)
    def goBack(self): # Hide this window and show admin page (reuse instance via parent)
        self.hide()
        self.parent().show()
    def Show_data(self): # load data into tableviews
        results=self.registration.show_all_prefreferences()
        model = QStandardItemModel()
        print(results)

        model.setHorizontalHeaderLabels(["faculty_id","name","availability","assigned_courses","course_preferences" ])

        for row in results:
            
            items = [QStandardItem(str(x)) for x in row]
            model.appendRow(items)

        self.tableView_Preferences.setModel(model)

        results1=self.registration.show_all_assigned()
        model1 = QStandardItemModel()
        print(results1)

        model1.setHorizontalHeaderLabels(["faculty_id","name","availability","assigned_courses","course_preferences" ])

        for row in results1:
            
            items1 = [QStandardItem(str(x)) for x in row]
            model1.appendRow(items1)

        self.tableView_Assigned.setModel(model1)

        results2=self.registration.All_courses_schedule()
        model2 = QStandardItemModel()
        print(results2)

        model2.setHorizontalHeaderLabels(["course_code",
                            "course_name",
                            "credit_hours",
                            "section",
                            "days",
                            "start_time",
                            "end_time",
                            "instructor_name",
                            "place",
                            "room",
                            "enrolled_count",
                            "max_capacity"])

        for row in results2:
            
            items2 = [QStandardItem(str(x)) for x in row]
            model2.appendRow(items2)

        self.tableView_courses.setModel(model2)
    def load_data(self): # load data into tableviews
        self.Show_data()
    def assign_faculty(self): # assign course to faculty
        faculty_id=self.lineEdit_FacultyID.text()
        course_code=self.lineEdit_CourseCode.text()
        section=self.lineEdit_Section.text()
        self.registration.assign_course_to_faculty(faculty_id,course_code,section)
        self.load_data()



#================= Faculty Page Window =====================#
class FacultyPage(QMainWindow):
    def __init__(self, parent=None):
        super(FacultyPage, self).__init__(parent)
        try:
            uic.loadUi("GUI_Faculty_dashbord.ui", self)
        except FileNotFoundError:
            print("Error: GUI_Faculty_dashbord.ui not found. Please ensure the file exists")
            sys.exit(1)
        self.setWindowTitle("Faculty Page")
        self.facultyProfile = FacultyProfile(parent=self)
        # self.set_availability=setAvailability(parent=self)
        self.set_preferences=set_preferences(parent=self)
        self.Show_assigned_courses=show_assigned_courses(parent=self)
        self.pushButton_FacultyProfile.clicked.connect(self.openFacultyProfile)
        # self.pushButton_availability.clicked.connect(self.setting_availability)
        self.pushButton_preferences.clicked.connect(self.setting_preferences)
        self.pushButton_ShowAssignedCourses.clicked.connect(self.assign_course_to_faculty)
        self.pushButton_Logout.clicked.connect(self.logout)

    def openFacultyProfile(self):   # Open faculty profile window
        self.hide()
        self.facultyProfile.displayInformation()
        self.facultyProfile.show()

    def logout(self):   # Logout and return to main app
        self.hide()
        self.parent().show()
    # def setting_availability(self):  # Set availability window
    #     self.hide()
    #     self.set_availability.show()
    def setting_preferences(self): # Set preferences window
        self.hide()
        self.set_preferences.show_All_courses()
        self.set_preferences.show()
    def assign_course_to_faculty(self): # Show assigned courses window
        self.hide()
        self.Show_assigned_courses.show_assigned_courses()
        self.Show_assigned_courses.show()




#================= Faculty Profile Window =====================#
class FacultyProfile(QMainWindow):
    def __init__(self, parent=None):
        super(FacultyProfile, self).__init__(parent) 
        try:
            uic.loadUi("GUI_Faculty_profile.ui", self)
        except FileNotFoundError:
            print("Error: GUI_Faculty_profile.ui not found. Please ensure the file exists")
            sys.exit(1)
        self.setWindowTitle("Faculty Profile")
        self.pushButton_Back.clicked.connect(self.goBack)
        self.registration=RegistrationSystem()
    def goBack(self): # Hide this window and show faculty page (reuse instance via parent)
        self.hide()
        self.parent().show()
    def displayInformation(self): # Display faculty information
        self.lineEdit_Name.setText(instance_name)
        self.lineEdit_IDNumber.setText(str(instance_ID_number))
        self.lineEdit_Email.setText(instance_email)
        self.lineEdit_Availability.setText(str(instance_availability))
        self.lineEdit_CoursePreferences.setText(str(instance_course_preferences))
        assigned_courses=str(self.registration.get_assigned_courses(instance_ID_number))
        self.lineEdit_AssignedCourses.setText(assigned_courses)
#================= Show Assigned Courses Window =====================#
class show_assigned_courses(QMainWindow):
    def __init__(self, parent=None):
        super(show_assigned_courses, self).__init__(parent)
        try:
            uic.loadUi("GUI_Assigned_Courses.ui", self)
        except FileNotFoundError:
            print("Error: GUI_Assigned_Courses.ui not found. Please ensure the file exists")
            sys.exit(1)
        self.setWindowTitle("Show Assigned Courses")
        self.pushButton_Back.clicked.connect(self.goBack)
    def goBack(self): # Hide this window and show faculty page (reuse instance via parent)
        self.hide()
        self.parent().show()
    def show_assigned_courses(self): # load data into tableviews
        self.registration=RegistrationSystem()
        results=self.registration.get_assigned_courses(instance_ID_number)
        model = QStandardItemModel()
        print(results)

        model.setHorizontalHeaderLabels(["course_code",
                            "course_name",
                            "credit_hours",
                            "section",
                            "days",
                            "start_time",
                            "end_time",
                            "instructor_name",
                            "place",
                            "room",
                            "enrolled_count",
                            "max_capacity"])

        for row in results:
            
            items = [QStandardItem(str(x)) for x in row]
            model.appendRow(items)

        self.tableView_AssignedCourses.setModel(model)
#================= Set Availability Window =====================#
# class setAvailability(QMainWindow):
#     def __init__(self, parent=None):
#         super(setAvailability, self).__init__(parent)
#         try:
#             uic.loadUi("GUI_setAvailability.ui", self)
#         except FileNotFoundError:   
#             print("Error: GUI_setAvailability.ui not found. Please ensure the file exists")
#             sys.exit(1)
#         self.setWindowTitle("Set Availability")
#         self.pushButton_Back.clicked.connect(self.goBack)
#     def goBack(self):
#         self.hide()
#         self.parent().show()
#================= Set Preferences Window =====================#
class set_preferences(QMainWindow):     # Set preferences window
    def __init__(self, parent=None):
        super(set_preferences, self).__init__(parent)
        try:
            uic.loadUi("GUI_set_preferences.ui", self)
        except FileNotFoundError:
            print("Error: GUI_set_preferences.ui not found. Please ensure the file exists")
            sys.exit(1)
        self.setWindowTitle("Set Preferences")
        self.pushButton_Back.clicked.connect(self.goBack)
        self.pushButton_SetPreferences.clicked.connect(self.setting_preferences)
        self.registration=RegistrationSystem()
    def goBack(self): # Hide this window and show faculty page (reuse instance via parent)  
        self.hide()
        self.parent().show()
    def show_All_courses(self): # load data into tableviews
        results=self.registration.All_courses_schedule()
        model = QStandardItemModel()
        print(results)

        model.setHorizontalHeaderLabels(["course_code",
                            "course_name",
                            "credit_hours",
                            "section",
                            "days",
                            "start_time",
                            "end_time",
                            "instructor_name",
                            "place",
                            "room",
                            "enrolled_count",
                            "max_capacity"])

        for row in results:
            
            items = [QStandardItem(str(x)) for x in row]
            model.appendRow(items)

        self.tableView_AllCourses.setModel(model)
        #now show my preferences in view Table
        results1=self.registration.get_assigned_courses(instance_ID_number)
        list_courses=[]
        for i in results1:
            data=self.registration.get_course_data(i)
            list_courses.append(data)
        model1 = QStandardItemModel()
        print(results1)
        model1.setHorizontalHeaderLabels(["course_code",
                            "course_name",
                            "credit_hours",
                            "section",
                            "days",
                            "start_time",
                            "end_time",
                            "instructor_name",
                            "place",
                            "room",
                            "enrolled_count",
                            "max_capacity"])

        for row in list_courses:
            
            items = [QStandardItem(str(x)) for x in row]
            model1.appendRow(items)

        self.tableView_AssignedCourses.setModel(model1)
        
    def setting_preferences(self): # set course preferences
        course_code=self.lineEdit_CourseCode.text()
        self.registration.set_course_preferences(instance_ID_number,course_code)
        self.load_data() 
    def load_data(self):        # load data into tableviews
        self.show_All_courses() 
        

        



                






#================= Initialize the app =====================#
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())