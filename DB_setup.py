from RegistrationSystemClass import RegistrationSystem
from NewCourseClass import Course
from loginvalidation import Admin
from TimeBuilder import Schedule
from TimeBuilder import ScheduleSystem
from FacultyClass import Faculty
from FacultyModule import FacultyAdminModule


################### seeding courses
def seed_courses():
    system = RegistrationSystem()
    courses = [

        # ===== Level 1 – Shared foundation courses (no prerequisites) =====
        Course(
            "ENG101",
            "Introduction to Electrical and Computer Engineering",
            3, 3, 0,
            [], 40,
            ["Computer", "Power", "Biomedical", "Communication"],
            1
        ),
        Course(
            "MATH101",
            "Calculus I for Engineers",
            3, 3, 0,
            [], 40,
            ["Computer", "Power", "Biomedical", "Communication"],
            1
        ),
        Course(
            "PHYS101",
            "Physics I for Engineers",
            3, 3, 0,
            [], 40,
            ["Computer", "Power", "Biomedical", "Communication"],
            1
        ),
        Course(
            "CIR101",
            "Electric Circuits I",
            3, 3, 1,
            [], 40,
            ["Computer", "Power", "Biomedical", "Communication"],
            1
        ),

        # ===== Computer Engineering – program specific =====
        Course(
            "CPE201",
            "Digital Logic Design",
            3, 3, 1,
            ["CIR101"], 40,
            ["Computer"],
            2
        ),

        Course(
            "CPE250",
            "Digital Logic Design",
            3, 3, 1,
            ["CIR101"], 40,
            ["Computer"],
            2
        ),
        Course(
            "CPE301",
            "Microprocessors and Interfacing",
            3, 3, 1,
            ["CPE201"], 40,
            ["Computer"],
            3
        ),
        Course(
            "CPE401",
            "Embedded Systems Design Project",
            3, 2, 3,
            ["CPE301"], 40,
            ["Computer"],
            4
        ),

        # ===== Power Engineering – program specific =====
        Course(
            "PWE201",
            "Introduction to Power Systems",
            3, 3, 0,
            ["CIR101"], 40,
            ["Power"],
            2
        ),
        Course(
            "PWE250",
            "Introduction to Power Systems",
            3, 3, 0,
            ["CIR101"], 40,
            ["Power"],
            2
        ),
        Course(
            "PWE301",
            "Electrical Machines and Drives",
            3, 3, 1,
            ["PWE201"], 40,
            ["Power"],
            3
        ),
        Course(
            "PWE401",
            "Power System Protection",
            3, 3, 0,
            ["PWE301"], 40,
            ["Power"],
            4
        ),

        # ===== Biomedical Engineering – program specific =====
        Course(
            "BME201",
            "Biomedical Signals and Systems",
            3, 3, 0,
            ["CIR101"], 40,
            ["Biomedical"],
            2
        ),
        Course(
            "BME250",
            "Biomedical Signals and Systems",
            3, 3, 0,
            ["CIR101"], 40,
            ["Biomedical"],
            2
        ),
        Course(
            "BME301",
            "Medical Instrumentation",
            3, 3, 1,
            ["BME201"], 40,
            ["Biomedical"],
            3
        ),
        Course(
            "BME401",
            "Biomedical Imaging Systems",
            3, 3, 0,
            ["BME301"], 40,
            ["Biomedical"],
            4
        ),

        # ===== Communication Engineering – program specific =====
        Course(
            "COM201",
            "Signals and Systems",
            3, 3, 0,
            ["CIR101"], 40,
            ["Communication"],
            2
        ),
        Course(
            "COM250",
            "Signals and Systems",
            3, 3, 0,
            ["CIR101"], 40,
            ["Communication"],
            2
        ),
        Course(
            "COM301",
            "Digital Communication",
            3, 3, 0,
            ["COM201"], 40,
            ["Communication"],
            3
        ),
        Course(
            "COM401",
            "Wireless Communication Systems",
            3, 3, 0,
            ["COM301"], 40,
            ["Communication"],
            4
        ),
    ]
    for course in courses:
        # This will use your RegistrationSystem.add_course logic
        system.add_course(course)
    print("Sucuessfully added courses")

################# seeding faculty
def seed_faculty():
    faculty = RegistrationSystem()

    faculty_data = [
        Faculty(10001,"Dr.Omar","Omar_O@example.com","@Oo112233"),
        Faculty(10002,"Dr.Mohammed","Mohammed_M@example.com","@Mm112233"),
        Faculty(10003,"Dr.Khalid","Khalid_K@example.com","@Kk112233"),
        Faculty(10004,"Dr.Ahmad","Ahmad_A@example.com","@Aa112233")

    ]
    for f in faculty_data:
        faculty.add_faculty(f)

    print("faculty 4 members added")


##### seeding schedule 
def seed_schedule():
        courseschedule_data = [
        
        ## general courses
        Schedule("ENG101", 2, '08:00','10:00',["Sun","Tue","Thu"], "Lecture", "Dr.Omar","ENG40","107"),
        Schedule("MATH101", 2, '10:00','11:00',["Sun","Tue","Thu"], "Lecture", "Dr.Mohammed","ENG40","106"),
        Schedule("PHYS101", 2, '11:00','12:00',["Mon","Wed"], "Lecture", "Dr.Khalid","ENG40","105"),
        Schedule("CIR101", 2, '01:00','02:00',["Sun","Tue","Thu"], "Lecture", "Dr.Khalid","ENG40","107"),


        ## computer courses
        Schedule("CPE201", 2, '08:00','10:00',["Sun","Tue","Thu"], "Lecture", "Dr.Omar","ENG40","108"),
        Schedule("CPE250", 2, '08:00','10:00',["Sun","Tue","Thu"], "Lecture", "Dr.Ahmad","ENG40","108"),
        Schedule("CPE301", 2, '09:00','11:00',["Sun","Tue","Thu"], "Lecture", "Dr.Mohammed","ENG40","104"),
        Schedule("CPE401", 2, '11:00','12:00',['Mon','Wed'], "Lecture", "Dr.Khalid","ENG40","102"),

        # power courses

        Schedule("PWE201", 2, '10:00','12:00',['Sun','Tue','Thu'], "Lecture", "Dr.Omar","ENG40","107"),
        Schedule("PWE250", 2, '09:00','11:00',['Sun','Tue','Thu'], "Lecture", "Dr.Ahmad","ENG40","108"),
        Schedule("PWE301", 2, '11:00','02:00',['Sun','Tue','Thu'], "Lecture", "Dr.Mohammed","ENG40","104"),
        Schedule("PWE401", 2, '11:00','02:00',['Mon','Wed'], "Lecture", "Dr.Khalid","ENG40","102"),

        ## biomedical courses
        Schedule("BME201", 2, '10:00','12:00',["Sun","Tue","Thu"], "Lecture", "Dr.Omar","ENG40","107"),
        Schedule("BME250", 2, '09:00','11:00',['Sun','Tue','Thu'], "Lecture", "Dr.Ahmad","ENG40","108"),
        Schedule("BME301", 2, '01:00','03:00',['Sun','Tue','Thu'], "Lecture", "Dr.Omar","ENG40","104"),
        Schedule("BME401", 2, '11:00','02:00',['Mon','Wed'], "Lecture", "Dr.Omar","ENG40","105"),

        Schedule("COM201", 2, '10:00','12:00',['Sun','Tue','Thu'], "Lecture", "Dr.Omar","ENG40","102"),
        Schedule("COM250", 2, '09:00','11:00',['Sun','Tue','Thu'], "Lecture", "Dr.Ahmad","ENG40","108"),
        Schedule("COM301", 2, '01:00','03:00',['Sun','Tue','Thu'], "Lecture", "Dr.Omar","ENG40","104"),
        Schedule("COM401", 2, '11:00','02:00',['Mon','Wed'], "Lecture", "Dr.Omar","ENG40","103"),
        ]

        schedule_builder = ScheduleSystem()
        for schedule in courseschedule_data:
            schedule_builder.add_schedule(schedule)

        print("Course 16 Schedule added")


import sqlite3
import random

from RegistrationSystemClass import RegistrationSystem
from NewStudentsClass import Student
import random
import NewUserClass


# All possible passing grades
GRADES = ["D", "D+", "C", "C+", "B", "B+", "A", "A+"]


def get_completed_courses(program, level):
    """
    Returns completed courses for the student according to:
    - shared level 1 courses
    - program-specific courses for levels 2–4
    """

    # Level 1 shared foundation courses
    level1 = ["ENG101", "MATH101", "PHYS101", "CIR101"]

    # Program-specific courses
    programs = {
        "Computer": ["CPE201", "CPE301", "CPE401"],
        "Power": ["PWE201", "PWE301", "PWE401"],
        "Biomedical": ["BME201", "BME301", "BME401"],
        "Communication": ["COM201", "COM301", "COM401"],
    }

    prog_courses = programs.get(program, [])

    if level == 1:
        return []  # no history
    elif level == 2:
        return level1
    elif level == 3:
        return level1 + prog_courses[:1]  # only level 2 course
    elif level == 4:
        return level1 + prog_courses[:2]  # level 2 + level 3
    else:
        return []


def seed_students():
    system = RegistrationSystem()

    # 4 students for each program (levels 1–4)
    students_data = [
        # Computer
        ("2210001", "Nawaf Alshamrani", "nawaf@example.com",'@Nawaf_1', "Computer", 1),
        ("2210002", "Fahad Alqahtani", "fahad@example.com","fahad", "Computer", 2),
        ("2210003", "Saud Alharbi", "saud@example.com","saud", "Computer", 3),
        ("2210004", "Turki Almutairi", "turki@example.com","Turki@1", "Computer", 4),

        # Power
        ("2211001", "Abdullah Alsubaie", "abdullah@example.com","abdullah", "Power", 1),
        ("2211002", "Mohammed Alosaimi", "mohammed@example.com","mohammed", "Power", 2),
        ("2211003", "Sultan Alshammari", "sultan@example.com","sultan", "Power", 3),
        ("2211004", "Rakan Alenazi", "rakan@example.com","rakan", "Power", 4),

        # Biomedical
        ("2212001", "Yousef Alotaibi", "yousef@example.com","yousef", "Biomedical", 1),
        ("2212002", "Faisal Alghamdi", "faisal@example.com","faisal", "Biomedical", 2),
        ("2212003", "Bader Alsharif", "bader@example.com","bader", "Biomedical", 3),
        ("2212004", "Talal Alzahrani", "talal@example.com","talal", "Biomedical", 4),

        # Communication
        ("2213001", "Omar Aljohani", "omar@example.com","omar", "Communication", 1),
        ("2213002", "Mansour Alsaadi", "mansour@example.com","mansour", "Communication", 2),
        ("2213003", "Khalid Alshatti", "khalid@example.com","khalid", "Communication", 3),
        ("2213004", "Saad Alomari", "saad@example.com","saad", "Communication", 4),
    ]

    for sid, name, email,password, program, level in students_data:
        # Generate transcript as list of tuples (course_code, grade)
        completed = get_completed_courses(program, level)
        transcript_list = [(c, random.choice(GRADES)) for c in completed]

        # create student object properly
        student = Student(
            sid,
            name,
            email,
            password,
            program,
            level,
            transcript_list  # pass transcript directly
        )
        # add student + transcript through the system
        system.add_student(student)

    print("Successfully added 16 students + transcripts!")

def seed_admin():
    system = RegistrationSystem()
    admin_data = [
        ("22220", "Mohammed Alzahrani", "Mohammed_S@example.com",'@Mm112233'),
        ("22221", "Khalid Alsulami", "Khalid_S@example.com","@Kk112233"),
        ("22222", "Abdulaziz Alharbi", "Abdulaziz_H@example.com","@Aa112233"),
        ("22223", "Ahmad Almutairi", "Ahmad_M@example.com","@Aa112233"),    
    ]
    for admin_id, name, email,password, in admin_data:
        admin = Admin(
            admin_id,
            name,
            email,
            password
        )

        # add admin through the system
        system.add_admin(admin)

    print("Successfully added 4 admins")
############ seeding enrollements

def seed_enrollments():
    system = RegistrationSystem()
    enrollments = [
        ("2210002", [("ENG101", "A"), ("MATH101", "B")]),
        ("2210003", [("CIR101", "B")]),
        ("2211002", [("ENG101", "A"), ("PHYS101", "B")]),
        ("2212003", [("BME201", "B")]),
        ("2213004", [("COM201", "A")]),
    ]
    
    for student_id, courses in enrollments:
        print(f"Registering {student_id}...")
        system.register_student(student_id, courses)

    print("Enrollments seeded successfully.")




system=RegistrationSystem()
# seed_students() 
# seed_faculty()
# seed_admin()
# seed_courses()
# seed_schedule()
seed_enrollments()
