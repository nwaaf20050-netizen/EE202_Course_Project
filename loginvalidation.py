import sqlite3
import re
import bcrypt
from RegistrationSystemClass import RegistrationSystem
from NewStudentsClass import Student
from FacultyClass import Faculty


class Admin:
    """Represents an admin with admin_id, name, email, and password."""
    def __init__(self, admin_id, name, email, password):
        self.admin_id = admin_id
        self.name = name.strip()
        self.email = email.strip()
        self.password = password.strip()

class LoginSystem:
    def __init__(self, db_name="RegistrationSystem.db"):
        self.db_name = db_name
        self.connect = sqlite3.connect(self.db_name)
        self.cursor = self.connect.cursor()

    ## checking if password is strong function
    try: 
        def is_strong_password(self, password):

            ## check if password has one uppercase one lowercase one digit one special char
                if len(password) < 8:
                    return False
                if not re.search(r"[A-Z]", password): ## check if password contains capital letters
                    return False
                if not re.search(r"[a-z]", password): ## check if password contains small letters
                    return False
                if not re.search(r"[0-9]", password): ## check if contains numbers
                    return False
                if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): ## check if cotains symbols
                    return False
                return True
    except Exception:
            print("unexpected password entered")


    ######## login validation function 
    def login(self, user_id, password):
        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

                ## checking if entered id is student 
            self.cursor.execute(
                "SELECT student_id, name, email, password, program, current_level FROM Students WHERE student_id=?",
                (user_id,)
            )
                ## fetch from student database table if id is student and store in (row) variable
            row = self.cursor.fetchone()

            if row:
                hashed_password = row[3]  ## taking password value from student database table storing it in stored_hash variable

                if bcrypt.checkpw(password.encode(), hashed_password):   ## check if entered password is correct and similar to password in database table
                    ### build a student object from fetched database student (row)
                    fetched_student = Student(
                        student_id=row[0],
                        name=row[1],
                        email=row[2],
                        password=row[3],
                        program=row[4], 
                        level=row[5],
                    )
                    self.connect.close()
                    ## return found object
                    # return ("student", fetched_student)
                    return ["student", fetched_student]

                ## if password isn't correct return message
                self.connect.close()
                return "Invalid ID or password."


                ## checking if entered id is admin
            self.cursor.execute(
                "SELECT admin_id, name, email, password FROM Admin WHERE admin_id=?",
                (user_id,)
            )
                ## fetch from admin database table if id is admin and store in (row) variable
            row = self.cursor.fetchone()

            if row:
                hashed_password = row[3]

                if bcrypt.checkpw(password.encode(), hashed_password):  ## check if entered password is correct and similar to password in database table
                        ## create and return admin object
                    fetched_admin = Admin(
                        admin_id=row[0],
                        name=row[1],
                        email=row[2],
                        password=row[3]
                    )
                    self.connect.close()
                    # return ("admin", fetched_admin)
                    return ["admin",fetched_admin]

                self.connect.close()
                ## if password is not correct return
                # return "Invalid ID or password."
                return ["invalid",None]
                #############################################
                ## checking if entered id is faculty member
                #############################################
            self.cursor.execute(
                "SELECT faculty_id, name, email, password FROM Faculty WHERE faculty_id=?",
                (user_id,)
            )
                ## fetch from faculty database table if id is faculty and store in (row) variable
            row = self.cursor.fetchone()

            if row:
                hashed_password = row[3]

                if bcrypt.checkpw(password.encode(), hashed_password):  ## check if entered password is correct and similar to password in database table
                        ## create and return faculty object
                    fetched_faculty = Faculty(
                        faculty_id=row[0],
                        name=row[1],
                        email=row[2],
                        password=row[3]
                    )
                    self.connect.close()
                    # return ("faculty", fetched_faculty)
                    return ["faculty",fetched_faculty]

                self.connect.close()
                ## if password is not correct return
                # return "Invalid ID or password."
                return ["invalid",None]

            ## if id is not student or admin or faculty return message
            self.connect.close()
            return ["Invalid ID or password.",None]
        
        except Exception as exception:
            return f"login has failed: {exception}"
        
        finally: 
            self.connect.close()



            



### testing code 
RegistrationSystem()
reg = RegistrationSystem()
student1 = Student(2444333,"abdulrahman","abdulrahman@gmail.com","@Aa123456","Power", 2)
admin1 = Admin(2444123,"mohammed","mohammed@gmail.com","@Mm123456")
faculty1 = Faculty(22230,"Dr.ahmad","ahmad@gmail.com","@Am112233")

system = LoginSystem()

reg.add_student(student1)
reg.add_admin(admin1)
reg.add_faculty(faculty1)

print(system.login(student1.student_id, student1.password))
print(system.login(admin1.admin_id, admin1.password))
print(system.login(faculty1.faculty_id, faculty1.password))

system = LoginSystem()
