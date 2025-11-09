#CoursesClass.py
import sqlite3
# DataBase file name
db_name="RegistrationSystem.db"

class Courses:
    def __init__(self,Course_code, name, credits, lecture_lab_hours, prerequisites,maximum_capacity):
        self.Course_code=Course_code
        self.name=name
        self.credits=credits
        self.lecture_lab_hours=lecture_lab_hours
        self.prerequisites=prerequisites
        self.maximum_capacity=maximum_capacity