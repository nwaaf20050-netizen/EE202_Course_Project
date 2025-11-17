# StudentClass.py
# Represents a student model with attributes and methods to manage student data.
import sqlite3
class User:

    def __init__(self, id_number, name, email ,role,department ):

        List_of_Valid_Roles=["ADMIN","Administrative","Faculty","Student"] #Valid Role list
        List_of_Valid_Departments=["Student Affairs","Engineering","Medical"] #Valid Department list
        self.id_number = id_number
        self.name = name
        self.email = email
        self.role = role  # Must be from the defined list
        self.department = department

        # Transcript is a list of tuples: (course_code, grade)
        # self.transcript = transcript if transcript else []


