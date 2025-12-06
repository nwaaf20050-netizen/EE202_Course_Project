import os
import sqlite3

from RegistrationSystemClass import RegistrationSystem
from TimeBuilder import ScheduleSystem, Schedule
from NewCourseClass import Course
from NewStudentsClass import Student
from FacultyClass import Faculty
from loginvalidation import Admin
from NewStudentsClass import Student




system = RegistrationSystem()
sched = ScheduleSystem()

print("System Initialized\n")


## testing function 
def test(name, func):
    print(f"Testing: {name}")
    try:
        result = func()
        print("Result:", result)
    except Exception as e:
        print("error:", e)
    print()




## registering a new admin method

def test_add_admin():
    admin = Admin(22230, "Ayman", "Ayman@gmail.com", "@Ay112233")
    return system.add_admin(admin)

test("Add Admin", test_add_admin)

######## adding a new faculty member
def test_add_faculty():
    f = Faculty(1010, "Dr.Ayman", "Ayman@gmail.com", "@Ay112233")
    return system.add_faculty(f)

test("Add Faculty", test_add_faculty)


############# testing add course method  
def test_add_course():
    c1 = Course("ENG101", "English", 3, 3, 0, [], 40, ["Computer"], 1)
    c2 = Course("MATH101", "Calculus", 3, 3, 0, [], 40, ["Computer"], 1)
    system.add_course(c1)
    system.add_course(c2)

    return "Courses Added"

test("Add Courses", test_add_course)


################ testing add student
def test_add_student():
    s = Student("2210010", "Ali Ahmed", "ali@uni.com", "@A123456", "Computer", 1, [])
    return system.add_student(s)

test("Add Student", test_add_student)

################ testing get student info method by id 
def test_get_student_info():
    return system.get_student_info("2210010")

test("Get Student Info", test_get_student_info)


############# testing schdule system class

## generating random lables for based on number of sections 
def test_generate_section_labels():
    return sched.generate_section_labels(3)

test("Generate Section Labels", test_generate_section_labels)

### validating if course time is in ["HH:MM"] format 
def test_validate_time():
    sched.validate_time("09:30")
    return "OK"

test("Validate Time", test_validate_time)

## validating if course is in [Sun Mon Tue Wed Thu] format 
def test_validate_days():
    sched.validate_days(["Sun", "Tue"])
    return "OK"

test("Validate Days", test_validate_days)

## Validate if lecture is in ["lecture online lab"] format
def test_validate_lecture_type():
    sched.validate_lecture_type("Lecture")
    return "OK"

test("Validate Lecture Type", test_validate_lecture_type)


# ADD SCHEDULES
#### set schedule for a specfic course 
def test_add_schedule():
    sc = Schedule("MATH101", 1, "08:00", "09:00", ["Sun", "Tue"], "Lecture", "Dr.Ayman", "Computer", "101")
    sc2 = Schedule("ENG101", 1, "10:00", "12:00", ["Sun", "Tue"], "Lecture", "Dr.Ayman", "Computer", "101")

    sched.add_schedule(sc)
    sched.add_schedule(sc2)

    return sched.get_course_sections("ENG101")

test("Add Schedule", test_add_schedule)

### testing enrollments

## testing get available courses for student 
def test_get_available_courses():
    return system.get_available_courses("2210001")

test("Get Available Courses", test_get_available_courses)


# testing if student can register specfic course without conflicts
def test_validate_schedule():
    return system.validate_schedule("2210001", [("ENG101", "A")])

test("Validate Schedule", test_validate_schedule)

##  testing registering a student for a course method
def test_register_student():
    return system.register_student("2210001", [("ENG101", "A")])

test("Register Student", test_register_student)

## testing getting the current schedule for student
def test_get_student_schedule():
    return system.get_student_schedule("2210001")

test("Get Student Schedule", test_get_student_schedule)


#testing credit hours and conflict methods

## getting total hours enrolled for specfic student
def test_total_hours():
    return sched.get_total_enrolled_hours("2210001")

test("Get Total Enrolled Hours", test_total_hours)


## testing if student exceeded hour limits 
def test_credit_limit():
    return sched.exceeds_credit_limit("2210001", [1])

test("Exceeds Credit Limit", test_credit_limit)


# FACULTY ASSIGNMENTS & CONFLICTS

## set the prefered day and time faculty prefers 
def test_set_availability():
    return system.set_availability(1001, ["Sun 10:00-12:00", "Tue 14:00-16:00"])

test("Faculty Set Availability", test_set_availability)


## set prefered courses for faculty member 
def test_set_course_preferences():
    return system.set_course_preferences(1001, ["MATH101", "ENG101"])

test("Faculty Set Course Preferences", test_set_course_preferences)

## admin assigning a course to a faculty member and making sure it's within his days and time preference 
def test_assign_course_to_faculty():
    try:
        return system.assign_course_to_faculty(1001,"MATH101")
    except Exception as e:
        return f"Expected Error (course missing): {e}"

test("Assign Course To Faculty", test_assign_course_to_faculty)

### get currently assigned courses for faculty
def test_get_assigned_courses():
    return system.get_assigned_courses(1001)

test("Get Assigned Courses", test_get_assigned_courses)


## check if new assignments to faculty by admin conflict with current assignments
def test_detect_conflicts():
    return system.detect_faculty_conflicts(1001,"ENG101")
test("Detect Faculty Conflicts", test_detect_conflicts)


## detect if course added to faculty is within time and day 
def test_is_course_in_preferences():
    return system.is_course_in_preferences(1001,"ENG101")
test("Detect Faculty preferences", test_detect_conflicts)




## transcript testing

## view transcripts for student method
def test_view_transcript():
    return system.view_transcript("2210001")

test("View Transcript", test_view_transcript)


## testing enrollment data function

def test_course_enrollment_data():
    return system.get_course_enrollment_data()

test("Course Enrollment Data", test_course_enrollment_data)


## deleting student from db function

def test_delete_student():
    return system.delete_student("2210001")

test("Delete Student", test_delete_student)

print("test complete")



# Courses.close_connection() #close the database connection
import sqlite3 #import sqlite3 module to interact with SQLite databases
from NewCourseClass import  Course   #import the Course class from CoursesClass module
from RegistrationSystemClass import RegistrationSystem #import RegistrationSystem class
from NewStudentsClass import Student #import NewStudentsClass module


# ---------------- Registration System ----------------
# system = RegistrationSystem()

# print("[OK] System initialized.\n")

# # ============================================================
# # 2) Add Student
# # ============================================================
# try:
#     student1 = Student(
#         student_id="2210001",
#         name="Nawaf",
#         email="nawaf@example.com",
#         program="Computer",
#         current_level=3
#     )
#     system.add_student(student1)
#     print("[OK] Student added.\n")

# except Exception as e:
#     print("[ERROR] Adding student:", e)

# # ============================================================
# # 3) Add Courses
# # ============================================================
# try:
#     course1 = Course(
#         course_code="COE201",
#         name="Intro to Programming",
#         credits=3,
#         lecture_hours=3,
#         lab_hours=1,
#         prerequisites=[],
#         max_capacity=40,
#         program="Computer",
#         level=3
#     )
#     system.add_course(course1)
#     print("[OK] COE201 added.")

#     course2 = Course(
#         course_code="COE301",
#         name="Data Structures",
#         credits=3,
#         lecture_hours=3,
#         lab_hours=1,
#         prerequisites=["COE201"],
#         max_capacity=40,
#         program="Computer",
#         level=3
#     )
#     system.add_course(course2)
#     print("[OK] COE301 added.\n")

# except Exception as e:
#     print("[ERROR] Adding courses:", e)

# # ============================================================
# # IMPORTANT: Close system connection before manual transcript
# # ============================================================

# # ============================================================
# # 4) Add Transcript Entry MANUALLY
# # ============================================================
# try:
#     conn = sqlite3.connect("RegistrationSystem.db")
#     cur = conn.cursor()

#     cur.execute(
#         "INSERT INTO transcripts (student_id, course_code, grade) VALUES (?, ?, ?)",
#         ("2210001", "COE201", "A")
#     )

#     conn.commit()
#     conn.close()
#     print("[OK] Transcript entry added (COE201 = A).\n")

# except Exception as e:
#     print("[ERROR] Adding transcript:", e)

# # ============================================================
# # Re-open system for remaining tests
# # ============================================================
# system = RegistrationSystem()
# print("[INFO] System connection re-opened.\n")

# # ============================================================
# # 5) Test validate_schedule
# # ============================================================
# try:
#     print("Testing validate_schedule for COE301...")
#     selected = ["COE301"]

#     if system.validate_schedule("2210001", selected):
#         print("[OK] validate_schedule passed.\n")
#     else:
#         print("[FAIL] validate_schedule failed.\n")

# except Exception as e:
#     print("[ERROR] validate_schedule:", e)

# # ============================================================
# # 6) Test register_student
# # ============================================================
# try:
#     system.register_student("2210001", "COE301")
#     print("[OK] Student registered in COE301.\n")

# except Exception as e:
#     print("[ERROR] register_student:", e)

# # ============================================================
# # 7) Test is_full()
# # ============================================================
# try:
#     course_obj = Course(
#         "COE301",
#         "Data Structures",
#         3, 3, 1,
#         ["COE201"],
#         40,
#         "Computer",
#         3
#     )

#     if course_obj.is_full():
#         print("[INFO] COE301 is full.\n")
#     else:
#         print("[INFO] COE301 is NOT full.\n")

# except Exception as e:
#     print("[ERROR] is_full:", e)

# # ============================================================
# # 8) Test delete_student
# # ============================================================
# try:
#     system.delete_student("2210001")
#     print("[OK] Student 2210001 fully deleted.\n")

# except Exception as e:
#     print("[ERROR] delete_student:", e)

# print("==============================")
# print("   TESTING FINISHED SUCCESSFULLY")
# print("==============================\n")



# print("\n==============================")
# print("   ADVANCED TEST SCENARIO")
# print("==============================\n")



# ============================================================
# Initialize System
# ============================================================

# system = RegistrationSystem()
# print("[OK] System initialized.\n")
# system.drop_all_tables()
# system = RegistrationSystem()
# ============================================================
# Create Students
# ============================================================

# student_good = Student("2210001", "Nawaf", "nawaf@mail.com", "Computer", 4)
# student_bad_program = Student("2210002", "Ali", "ali@mail.com", "Computer", 4)
# student_low_level = Student("2210003", "Sara", "sara@mail.com", "Biomedical", 1)

# system.add_student(student_good)
# system.add_student(student_bad_program)
# system.add_student(student_low_level)

# print("[OK] Students added.\n")

# ============================================================
# Create Courses
# ============================================================

# COE201 = Course("COE201", "Intro to Programming", 3, 3, 1, [], 40, "Computer", 1)
# COE301 = Course("COE301", "Data Structures", 3, 3, 1, "COE201", 1, ["Power"], 3)
# COE350 = Course("COE350", "Operating Systems", 3, 3, 1, ["COE301","COE201"], 40, ["Computer"], 4)
# # cc=Course()

# system.add_course(COE201)
# system.add_course(COE301)
# system.add_course(COE350)

# print("[OK] Courses added.\n")

# ============================================================
# Add Transcript Manually For Testing
# ============================================================

# conn = sqlite3.connect("RegistrationSystem.db")
# cur = conn.cursor()

# # student_good: passed COE201 but failed COE301
# cur.execute("INSERT INTO transcripts VALUES (?, ?, ?)", ("2210001", "COE201", "A"))
# cur.execute("INSERT INTO transcripts VALUES (?, ?, ?)", ("2210001", "COE301", "F"))

# # student_bad_program: passed everything
# cur.execute("INSERT INTO transcripts VALUES (?, ?, ?)", ("2210002", "COE201", "A"))

# # student_low_level: no courses
# conn.commit()
# conn.close()

# print("[OK] Transcript entries added.\n")

# # # ============================================================
# # 1) Test prerequisite missing
# # ============================================================

# print("TEST 1: Missing prerequisite (Nawaf wants COE350):")
# if system.validate_schedule("2210001", ["COE350"]):
#     print("[FAIL] Should NOT be allowed.\n")
# else:
#     print("[PASS] Correctly blocked due to missing COE301.\n")

# # ============================================================
# # 2) Test failed prerequisite (Grade = F)
# # ============================================================

# print("TEST 2: Failed prerequisite (Nawaf wants COE301 and he has F):")
# if system.validate_schedule("2210001", ["COE301"]):
#     print("[PASS] Should be allowed to take the course again.\n")
# else:
#     print("[FAIL] he should be able to take the course again even if he get grade F first time .\n")

# # ============================================================
# # 3) Test full capacity (COE301 capacity = 1)
# # ============================================================

# # Fill the course
# # system.register_student("2210002", "COE301")

# print("TEST 3A: Course register bc there are one place lift (Nawaf wants COE301):")
# if system.register_student("2210001", ["COE301"]):
#     print("[PASS] there are one place lift \n") #wrong
# else:
#     print("[FAIL] there are still a place he should be able to register\n") #wrong 

# print("TEST 3B: Course full (Ali wants COE301):")
# if system.validate_schedule("2210002", ["COE301"]):
#     print("[FAIL] Should NOT be allowed.\n") #wrong
# else:
#     print("[PASS] Correctly blocked because course is full.\n") #wrong

# # ============================================================
# # 4) Test wrong program
# # ============================================================

# print("TEST 4: Wrong program (Biomedical student wants COE201):")
# if system.validate_schedule("2210002", ["COE201"]):
#     print("[PASS] Allowed since COE201 program doesn't restrict.")
# else:
#     print("[INFO] If your system restricts programs, BLOCK is correct.\n")

# # ============================================================
# # 5) Test wrong level
# # ============================================================

# print("TEST 5: Wrong level (Sara wants COE301 but she is level 1):")
# if system.validate_schedule("2210003", ["COE301"]):
#     print("[FAIL] Should NOT be allowed.\n")
# else:
#     print("[PASS] Correctly blocked due to level mismatch.\n")

# # ============================================================
# # 6) Test valid registration
# # ============================================================

# print("TEST 6: Valid case (Sara wants COE201):")
# if system.validate_schedule("2210003", ["COE201"]):
#     print("[PASS] Allowed.\n")
# else:
#     print("[FAIL] Should be allowed.\n")

# # ============================================================
# # 7) Test register_student
# # ============================================================

# print("TEST 7: Register Sara in COE201:")
# try:
#     system.register_student("2210003", "COE201")
#     print("[PASS] Registration worked.\n")
# except:
#     print("[FAIL] Something went wrong.\n")

# # ============================================================
# # 8) Test delete_student
# # ============================================================

# print("TEST 8: Deleting student 2210001:")
# try:
#     system.delete_student("2210001")
#     print("[PASS] Deleted with transcript + enrollment.\n")
# except:
#     print("[FAIL] Delete failed.\n")

# print("==============================")
# print(" ADVANCED TESTING COMPLETED ")
# print("==============================\n")


