#StudentsClass.py
import sqlite3
# DataBase file name
db_name="RegistrationSystem.db"

class Studnets : #Students class to represent a student in the system
    list_Of_Valid_Programs=["Computer","Power","Biomedical","Communication"] #Valid programs list
    def __init__(self,name,student_id,email,program,current_level): #Constructor to initialize student attributes
        self.name=name
        self.student_id=student_id
        self.email=email
        self.current_level=current_level
        self.program=program
        self.transcript = []                  # List of completed courses (filled later)

    def add_to_db(self): #Method to add student to the database
        if self.program not in Studnets.list_Of_Valid_Programs: #Check if the program is valid
            print("Please select a valid program (Computer, Communication, Power, Biomedical).")  
            return #Exit the method if the program is invalid
        try:
            pass
        except:
            pass
        finally:
            pass