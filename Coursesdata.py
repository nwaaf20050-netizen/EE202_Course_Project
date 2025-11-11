# Coursesdata.py
# This script creates and populates the Courses database table
# It also retrieves and prints all course records.
import sqlite3 #import sqlite3 module to interact with SQLite databases
from CoursesClass import Courses #import the Courses class from CoursesClass module
Courses=Courses() #create an instance of the Courses class
list_of_courses=[
    ("CS101", "Introduction to Computer Science", 3, 3, 0, "None", 50, "Computer",1),
    ("EE201", "Circuit Analysis", 4, 3, 1, "PH101", 40, "Power",2),
    ("BM301", "Biomedical Instrumentation", 3, 2, 1, "EE201", 30, "Biomedical",3),
    ("CM401", "Digital Communication", 3, 2, 1, "EE201", 35, "Communication",4),
    ("CS202", "Data Structures", 3, 3, 0, "CS101", 45, "Computer",2),
    ("EE302", "Electromagnetic Fields", 4, 3, 1, "EE201", 40, "Power",3),
    ("BM402", "Medical Imaging", 3, 2, 1, "BM301", 30, "Biomedical",4),
    ("CM102", "Signals and Systems", 3, 2, 1, "None", 35, "Communication",1), 
    ("CS303", "Algorithms", 3, 3, 0, "CS202", 45, "Computer",3),    
    ("EE103", "Digital Logic Design", 4, 3, 1, "None", 40, "Power",1),
    ("BM203", "Human Physiology", 3, 2, 1, "None", 30, "Biomedical",2),
    ("CM304", "Wireless Communication", 3, 2, 1, "CM102", 35, "Communication",3),
    ("CS404", "Operating Systems", 3, 3, 0, "CS303", 45, "Computer",4),
    ("EE204", "Power Systems", 4, 3, 1, "EE103", 40, "Power",2),
    ("BM104", "Biomaterials", 3, 2, 1, "None", 30, "Biomedical",1),
    ("CM205", "Network Theory", 3, 2, 1, "CM102", 35, "Communication",2)
]      #list of tuples containing course data

Courses.drop_courses_table()      #drop the Courses table if it exists
Courses.create_courses_table()    #create the Courses table if it doesn't exist

Courses.add_multiple_courses(list_of_courses) #add multiple courses to the database

Courses.add_course("CS505", "Machine Learning", 3, 3, 0,["CS404",111], 40, "Computer",4) #add a single course to the database

print(Courses.get_course_by_code("CS505")) #retrieve and print course with code CS505

# Courses.update_course_info("CS505",credit_hours=6) #update the max_students for course CS505

# print(Courses.get_course_by_code("CS505")) #retrieve and print course with code CS505 after update

Courses.delete_course("CS505")  #delete course with code EE909 (non-existent course for testing)

Courses.get_show_all_courses()  #retrieve and print all course records


Courses.close_connection() #close the database connection