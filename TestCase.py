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

