import sqlite3
import re
import bcrypt
from RegistrationSystemClass import RegistrationSystem

class student:
    """Represents a student with ID, name, email, password, program, level, and registered courses."""
    def __init__(self, student_id, name, email, password, program =None, level=None):
        self.student_id = student_id
        self.name = name.strip()
        self.email = email.strip()
        self.password = password.strip()
        self.program = program
        self.level = level

class admin:
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


    ######## sign up function
    ## the (user) parameter sent here can either be student or admin object
    def signup(self, user):
        self.connect = sqlite3.connect(self.db_name)
        self.cursor = self.connect.cursor()

        # check if sent object is admin or student using hasattr function 
        is_student = hasattr(user, "student_id")
        is_admin = hasattr(user, "admin_id")

        # Extract info based on role student or admin
        if is_student:
            table = "students"
            user_id = user.student_id
            email = user.email
            password = user.password

        elif is_admin:
            table = "admin"
            user_id = user.admin_id
            email = user.email
            password = user.password

        else:
            return "Invalid user object."

        # using is strong function to check password
        if not self.is_strong_password(password):
            return "Password is not strong enough."

        # Check if email already exists
        self.cursor.execute(
            f"SELECT email FROM {table} WHERE email=?",
            (email,)
        )
        ## fetch selected email and return message if exists
        if self.cursor.fetchone():
            return "Duplicate email or ID exists."

        # incrypt the password using methods from bycrypt class 
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        # if role is student insert student into student table
        if is_student:
            self.cursor.execute(
                """INSERT INTO Students 
                (student_id, name, email, password, program, current_level)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (user.student_id, user.name, user.email, hashed, user.program, user.level)
            )

        # if role is admin insert admin into admin table
        else:
            self.cursor.execute(
                "INSERT INTO Admin (admin_id, name, email, password) VALUES (?, ?, ?, ?)",
                (user.admin_id, user.name, user.email, hashed)
            )

        self.connect.commit()
        self.connect.close()

        return "Signup successful."


    ######## login validation function 
    def login(self, user_id, password):

        self.connect = sqlite3.connect(self.db_name)
        self.cursor = self.connect.cursor()

            ## checking if entered id is student 
        self.cursor.execute(
            "SELECT student_id, name, email, password, current_level FROM Students WHERE student_id=?",
            (user_id,)
        )
            ## fetch from student database table if id is student and store in (row) variable
        row = self.cursor.fetchone()

        if row:
            hashed_password = row[3]  ## taking password value from student database table storing it in stored_hash variable

            if bcrypt.checkpw(password.encode(), hashed_password):   ## check if entered password is correct and similar to password in database table
                ### build a student object from fetched database student (row)
                fetched_student = student(
                    student_id=row[0],
                    name=row[1],
                    email=row[2],
                    password=row[3],
                    level=row[4],
                )
                self.connect.close()
                ## return found object
                return ("student", fetched_student)

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
                fetched_admin = admin(
                    admin_id=row[0],
                    name=row[1],
                    email=row[2],
                    password=row[3]
                )
                self.connect.close()
                return ("admin", fetched_admin)

            self.connect.close()
            ## if password is not correct return
            return "Invalid ID or password."
        

        ## if id is not student or admin return message
        self.connect.close()
        return "Invalid ID or password."



### testing code 
RegistrationSystem()

student1 = student(2444333,"abdulrahman","abdulrahman@gmail.com","@Aa123456","Computer", 2)
admin1 = admin(2444123,"mohammed","mohammed@gmail.com","@Mm123456")

system = LoginSystem()

print(system.signup(student1))
print(system.signup(admin1))

print(system.login(student1.student_id, student1.password))
print(system.login(admin1.admin_id, admin1.password))


