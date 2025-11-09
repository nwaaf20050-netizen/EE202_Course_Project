#StudentsClass.py
import sqlite3
# DataBase file name
db_name="RegistrationSystem.db"

class Studnets :
    list_Of_Valid_Programs=["Computer","Power","Biomedical","Communication"]
    def __init__(self,name,student_id,email,program,current_level):
        #Basic student attributes
        self.name=name
        self.student_id=student_id
        self.email=email
        self.current_level=current_level
        self.program=program
        self.transcript = []                  # List of completed courses (filled later)

    def add_to_db(self):
        if self.program not in Studnets.list_Of_Valid_Programs:
            print("Please select a valid program (Computer, Communication, Power, Biomedical).")
            return
        try:
            pass
        except:
            pass
        finally:
            pass