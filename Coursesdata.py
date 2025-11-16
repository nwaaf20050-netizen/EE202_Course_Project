# # Coursesdata.py
# # This script creates and populates the Courses database table
# # It also retrieves and prints all course records.
# import sqlite3 #import sqlite3 module to interact with SQLite databases
# from CoursesClass import Courses #import the Courses class from CoursesClass module
# Courses=Courses() #create an instance of the Courses class
# # list_of_courses=[
# #     ("CS101", "Introduction to Computer Science", 3, 3, 0, "None", 50, "Computer",1),
# #     ("EE201", "Circuit Analysis", 4, 3, 1, "PH101", 40, "Power",2),
# #     ("BM301", "Biomedical Instrumentation", 3, 2, 1, "EE201", 30, "Biomedical",3),
# #     ("CM401", "Digital Communication", 3, 2, 1, "EE201", 35, "Communication",4),
# #     ("CS202", "Data Structures", 3, 3, 0, "CS101", 45, "Computer",2),
# #     ("EE302", "Electromagnetic Fields", 4, 3, 1, "EE201", 40, "Power",3),
# #     ("BM402", "Medical Imaging", 3, 2, 1, "BM301", 30, "Biomedical",4),
# #     ("CM102", "Signals and Systems", 3, 2, 1, "None", 35, "Communication",1), 
# #     ("CS303", "Algorithms", 3, 3, 0, "CS202", 45, "Computer",3),    
# #     ("EE103", "Digital Logic Design", 4, 3, 1, "None", 40, "Power",1),
# #     ("BM203", "Human Physiology", 3, 2, 1, "None", 30, "Biomedical",2),
# #     ("CM304", "Wireless Communication", 3, 2, 1, "CM102", 35, "Communication",3),
# #     ("CS404", "Operating Systems", 3, 3, 0, "CS303", 45, "Computer",4),
# #     ("EE204", "Power Systems", 4, 3, 1, "EE103", 40, "Power",2),
# #     ("BM104", "Biomaterials", 3, 2, 1, "None", 30, "Biomedical",1),
# #     ("CM205", "Network Theory", 3, 2, 1, "CM102", 35, "Communication",2)
# # ]      #list of tuples containing course data

# Courses.drop_courses_table()      #drop the Courses table if it exists
# Courses.create_courses_table()    #create the Courses table if it doesn't exist

# Courses.add_multiple_courses(list_of_courses) #add multiple courses to the database

# Courses.add_course("CS505", "Machine Learning", 3, 3, 0,["CS404","CM205"], 40, "Computer",4) #add a single course to the database

# print(Courses.get_course_by_code("CS505")) #retrieve and print course with code CS505

# # Courses.update_course_info("CS505",credit_hours=6) #update the max_students for course CS505

# # print(Courses.get_course_by_code("CS505")) #retrieve and print course with code CS505 after update

# Courses.delete_course("CS505")  #delete course with code EE909 (non-existent course for testing)

# Courses.get_show_all_courses()  #retrieve and print all course records


# Courses.close_connection() #close the database connection
import sqlite3 #import sqlite3 module to interact with SQLite databases
from NewCourseClass import  Course   #import the Course class from CoursesClass module
from RegistrationSystemClass import RegistrationSystem #import RegistrationSystem class
from NewStudentsClass import Student #import NewStudentsClass module

# # ---------------- Power Courses ----------------
# p1 = Course("PW101", "Intro to Power Engineering", 3, 3, 1, "Power", 1, [])
# p2 = Course("PW201", "Power Systems I", 3, 3, 2, "Power", 2, ["PW101"])
# p3 = Course("PW301", "Power Electronics", 3, 3, 3, "Power", 3, ["PW201"])
# p4 = Course("PW401", "Advanced Power Systems", 3, 3, 4, "Power", 4, ["PW301"])

# # ---------------- Computer Courses ----------------
# c1 = Course("CP101", "Intro to Computer Engineering", 3, 3, 1, "Computer", 1, [])
# c2 = Course("CP201", "Data Structures", 3, 3, 2, "Computer", 2, ["CP101"])
# c3 = Course("CP301", "Operating Systems", 3, 3, 3, "Computer", 3, ["CP201"])
# c4 = Course("CP401", "Embedded Systems", 3, 3, 4, "Computer", 4, ["CP301"])

# # ---------------- Communication Courses ----------------
# cm1 = Course("CM101", "Intro to Communications", 3, 3, 1, "Communication", 1, [])
# cm2 = Course("CM201", "Signals & Systems", 3, 3, 2, "Communication", 2, ["CM101"])
# cm3 = Course("CM301", "Digital Communications", 3, 3, 3, "Communication", 3, ["CM201"])
# cm4 = Course("CM401", "Wireless Communications", 3, 3, 4, "Communication", 4, ["CM301"])

# # ---------------- Biomedical Courses ----------------
# b1 = Course("BM101", "Intro to Biomedical Engineering", 3, 3, 1, "Biomedical", 1, [])
# b2 = Course("BM201", "Human Physiology", 3, 3, 2, "Biomedical", 2, ["BM101"])
# b3 = Course("BM301", "Medical Instrumentation", 3, 3, 3, "Biomedical", 3, ["BM201"])
# b4 = Course("BM401", "Biomedical Signal Processing", 3, 3, 4, "Biomedical", 4, ["BM301"])
# # ---------------- Students ----------------

# # ---------------- Power Students ----------------
# s1  = Student("2211001", "Nawaf Power L1",  "pw1@mail.com", "Power", 1, [])
# s2  = Student("2211002", "Ali Power L2",    "pw2@mail.com", "Power", 2, [("PW101", "B+")])
# s3  = Student("2211003", "Omar Power L3",   "pw3@mail.com", "Power", 3, [("PW101", "A"), ("PW201", "B")])
# s4  = Student("2211004", "Saleh Power L4",  "pw4@mail.com", "Power", 4, [("PW101", "A+"), ("PW201", "A"), ("PW301", "B+")])


# # ---------------- Computer Students ----------------
# s5  = Student("2212001", "Nawaf Comp L1",   "cp1@mail.com", "Computer", 1, [])
# s6  = Student("2212002", "Ali Comp L2",     "cp2@mail.com", "Computer", 2, [("CP101", "B")])
# s7  = Student("2212003", "Omar Comp L3",    "cp3@mail.com", "Computer", 3, [("CP101", "A"), ("CP201", "B+")])
# s8  = Student("2212004", "Saleh Comp L4",   "cp4@mail.com", "Computer", 4, [("CP101", "A+"), ("CP201", "A-"), ("CP301", "B")])


# # ---------------- Communication Students ----------------
# ss9  = Student("2213001", "Nawaf Comm L1",   "cm1@mail.com", "Communication", 1, [])
# s10 = Student("2213002", "Ali Comm L2",     "cm2@mail.com", "Communication", 2, [("CM101", "B+")])
# s11 = Student("2213003", "Omar Comm L3",    "cm3@mail.com", "Communication", 3, [("CM101", "A"), ("CM201", "B")])
# s12 = Student("2213004", "Saleh Comm L4",   "cm4@mail.com", "Communication", 4, [("CM101", "A+"), ("CM201", "A"), ("CM301", "B+")])


# # ---------------- Biomedical Students ----------------
# s13 = Student("2214001", "Nawaf Bio L1",     "bm1@mail.com", "Biomedical", 1, [])
# s14 = Student("2214002", "Ali Bio L2",       "bm2@mail.com", "Biomedical", 2, [("BM101", "B+")])
# s15 = Student("2214003", "Omar Bio L3",      "bm3@mail.com", "Biomedical", 3, [("BM101", "A"), ("BM201", "B")])
# s16 = Student("2214004", "Saleh Bio L4",     "bm4@mail.com", "Biomedical", 4, [("BM101", "A+"), ("BM201", "A"), ("BM301", "B+")])
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



print("\n==============================")
print("   ADVANCED TEST SCENARIO")
print("==============================\n")

# ============================================================
# CLEAR DATABASE (OPTIONAL but recommended)
# ============================================================



# ============================================================
# Initialize System
# ============================================================

system = RegistrationSystem()
print("[OK] System initialized.\n")
system.drop_all_tables()
system = RegistrationSystem()
# ============================================================
# Create Students
# ============================================================

student_good = Student("2210001", "Nawaf", "nawaf@mail.com", "Computer", 4)
student_bad_program = Student("2210002", "Ali", "ali@mail.com", "Biomedical", 4)
student_low_level = Student("2210003", "Sara", "sara@mail.com", "Computer", 1)

system.add_student(student_good)
system.add_student(student_bad_program)
system.add_student(student_low_level)

print("[OK] Students added.\n")

# ============================================================
# Create Courses
# ============================================================

COE201 = Course("COE201", "Intro to Programming", 3, 3, 1, [], 40, "Computer", 1)
COE301 = Course("COE301", "Data Structures", 3, 3, 1, ["COE201"], 1, "Computer", 3)
COE350 = Course("COE350", "Operating Systems", 3, 3, 1, ["COE301"], 40, "Computer", 4)

system.add_course(COE201)
system.add_course(COE301)
system.add_course(COE350)

print("[OK] Courses added.\n")

# ============================================================
# Add Transcript Manually For Testing
# ============================================================

conn = sqlite3.connect("RegistrationSystem.db")
cur = conn.cursor()

# student_good: passed COE201 but failed COE301
cur.execute("INSERT INTO transcripts VALUES (?, ?, ?)", ("2210001", "COE201", "A"))
cur.execute("INSERT INTO transcripts VALUES (?, ?, ?)", ("2210001", "COE301", "F"))

# student_bad_program: passed everything
cur.execute("INSERT INTO transcripts VALUES (?, ?, ?)", ("2210002", "COE201", "A"))

# student_low_level: no courses
conn.commit()
conn.close()

print("[OK] Transcript entries added.\n")

# ============================================================
# 1) Test prerequisite missing
# ============================================================

print("TEST 1: Missing prerequisite (Nawaf wants COE350):")
if system.validate_schedule("2210001", ["COE350"]):
    print("[FAIL] Should NOT be allowed.\n")
else:
    print("[PASS] Correctly blocked due to missing COE301.\n")

# ============================================================
# 2) Test failed prerequisite (Grade = F)
# ============================================================

print("TEST 2: Failed prerequisite (Nawaf wants COE301 and he has F):")
if system.validate_schedule("2210001", ["COE301"]):
    print("[FAIL] Should NOT be allowed.\n")
else:
    print("[PASS] Correctly blocked due to grade F.\n")

# ============================================================
# 3) Test full capacity (COE301 capacity = 1)
# ============================================================

# Fill the course
system.register_student("2210002", "COE301")

print("TEST 3A: Course full (Nawaf wants COE301):")
if system.register_student("2210001", ["COE301"]):
    print("[FAIL] Should NOT be allowed.\n") #wrong
else:
    print("[PASS] Correctly blocked because course is full.\n") #wrong 

print("TEST 3B: Course full (Ali wants COE301):")
if system.validate_schedule("2210002", ["COE301"]):
    print("[FAIL] Should NOT be allowed.\n") #wrong
else:
    print("[PASS] Correctly blocked because course is full.\n") #wrong

# ============================================================
# 4) Test wrong program
# ============================================================

print("TEST 4: Wrong program (Biomedical student wants COE201):")
if system.validate_schedule("2210002", ["COE201"]):
    print("[PASS] Allowed since COE201 program doesn't restrict.")
else:
    print("[INFO] If your system restricts programs, BLOCK is correct.\n")

# ============================================================
# 5) Test wrong level
# ============================================================

print("TEST 5: Wrong level (Sara wants COE301 but she is level 1):")
if system.validate_schedule("2210003", ["COE301"]):
    print("[FAIL] Should NOT be allowed.\n")
else:
    print("[PASS] Correctly blocked due to level mismatch.\n")

# ============================================================
# 6) Test valid registration
# ============================================================

print("TEST 6: Valid case (Sara wants COE201):")
if system.validate_schedule("2210003", ["COE201"]):
    print("[PASS] Allowed.\n")
else:
    print("[FAIL] Should be allowed.\n")

# ============================================================
# 7) Test register_student
# ============================================================

print("TEST 7: Register Sara in COE201:")
try:
    system.register_student("2210003", "COE201")
    print("[PASS] Registration worked.\n")
except:
    print("[FAIL] Something went wrong.\n")

# ============================================================
# 8) Test delete_student
# ============================================================

print("TEST 8: Deleting student 2210001:")
try:
    system.delete_student("2210001")
    print("[PASS] Deleted with transcript + enrollment.\n")
except:
    print("[FAIL] Delete failed.\n")

print("==============================")
print(" ADVANCED TESTING COMPLETED ")
print("==============================\n")
