import random
import re

# -------------------- Classes --------------------
class Student:
    def __init__(self, student_id: str, name: str, email: str, password: str, level: int = None):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.password = password
        self.level = level
        self.registered_courses = []

    def __repr__(self):
        return f"<Student {self.student_id} | {self.name}>"

class Admin:
    def __init__(self, email: str, name: str, password: str):
        self.email = email
        self.name = name
        self.password = password
        self.identifier = email

    def __repr__(self):
        return f"<Admin {self.identifier} | {self.name}>"

class Course:
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return f"{self.code} - {self.name}"

# -------------------- User Management --------------------
class UserManager:
    def __init__(self):
        self.students = []
        self.admins = [Admin("admin@ece.example", "Main Admin", "admin123")]

        # Courses per level
        self.level_courses = {
            1: [Course("COE101", "Intro to Programming"), Course("COE102", "Math I"),
                Course("COE103", "Physics I"), Course("COE104", "English I"), Course("COE105", "Drawing")],
            2: [Course("COE201", "Data Structures"), Course("COE202", "Math II"),
                Course("COE203", "Physics II"), Course("COE204", "English II"), Course("COE205", "Chemistry")],
            3: [Course("COE301", "Algorithms"), Course("COE302", "Computer Architecture"),
                Course("COE303", "Math III"), Course("COE304", "English III"), Course("COE305", "Electronics")],
            4: [Course("COE401", "Operating Systems"), Course("COE402", "Networks"),
                Course("COE403", "Database Systems"), Course("COE404", "Math IV"), Course("COE405", "Digital Logic")],
            5: [Course("COE501", "Software Engineering"), Course("COE502", "AI Basics"),
                Course("COE503", "Embedded Systems"), Course("COE504", "Computer Security"), Course("COE505", "Simulation")],
            6: [Course("COE601", "Project Management"), Course("COE602", "Machine Learning"),
                Course("COE603", "Robotics"), Course("COE604", "Cloud Computing"), Course("COE605", "Capstone Project")]
        }

    def generate_student_id(self):
        while True:
            student_id = "25" + str(random.randint(10000, 99999))
            if not any(s.student_id == student_id for s in self.students):
                return student_id

    def add_student(self, student: Student):
        if any(s.email == student.email for s in self.students):
            return False, "Email already exists."
        self.students.append(student)
        return True, "Student registered successfully."

    def find_student(self, identifier: str):
        for s in self.students:
            if s.student_id == identifier or s.email == identifier:
                return s
        return None

    def find_admin(self, identifier: str):
        for a in self.admins:
            if a.identifier == identifier:
                return a
        return None

    def register_course(self, student: Student, course_index: int):
        level_courses = self.level_courses.get(student.level, [])
        if course_index < 1 or course_index > len(level_courses):
            return False, "Invalid choice."
        course = level_courses[course_index - 1]
        if course.code in student.registered_courses:
            return False, "You already registered this course."
        student.registered_courses.append(course.code)
        return True, f"Course {course.code} registered successfully."

    def drop_course(self, student: Student, index: int):
        if index < 1 or index > len(student.registered_courses):
            return False, "Invalid choice."
        code = student.registered_courses[index - 1]
        student.registered_courses.remove(code)
        return True, f"Course {code} has been dropped."

# -------------------- Authentication --------------------
class AuthManager:
    allowed_domains = ["gmail.com","hotmail.com","yahoo.com","outlook.com","kau.edu.sa"]

    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager

    def is_valid_email(self, email):
        pattern = r'^[\w\.-]+@([\w\.-]+)$'
        match = re.match(pattern, email)
        return bool(match and match.group(1) in self.allowed_domains)

    def is_valid_password(self, password):
        return any(c.isupper() for c in password) and any(not c.isalnum() for c in password)

    def is_valid_fullname(self, name):
        return len(name.strip().split()) >= 3

    def signup_student(self):
        print("\n==== Student Registration ====")
        print("Type 'back' at any time to return to Main Menu\n")
        name = email = password = ""
        # الاسم
        inp = input("Enter Full Name (three parts at least): ").strip()
        if inp.lower() == "back":
            return
        while not self.is_valid_fullname(inp):
            print("Error: Name must contain at least 3 parts (First Middle Last).")
            inp = input("Enter Full Name (three parts at least): ").strip()
            if inp.lower() == "back":
                return
        name = inp
        # الايميل
        inp = input("Enter Email: ").strip()
        if inp.lower() == "back":
            return
        while not self.is_valid_email(inp) or any(s.email == inp for s in self.user_manager.students):
            if inp.lower() == "back":
                return
            if not self.is_valid_email(inp):
                print("Error: Email domain not allowed. Allowed: gmail, hotmail, yahoo, outlook, kau.edu.sa")
            else:
                print("Error: Email already exists. Please use a different email.")
            inp = input("Enter Email: ").strip()
        email = inp
        # الباسوورد
        inp = input("Enter Password: ").strip()
        if inp.lower() == "back":
            return
        while not self.is_valid_password(inp):
            print("Error: Password must contain at least 1 uppercase letter and 1 symbol (!,@,#, etc).")
            inp = input("Enter Password: ").strip()
            if inp.lower() == "back":
                return
        password = inp

        student_id = self.user_manager.generate_student_id()
        new_student = Student(student_id, name, email, password)
        ok, msg = self.user_manager.add_student(new_student)
        if ok:
            print(f"\nAccount registered! You can now login. Your student ID is: {student_id}\n")
        else:
            print(msg)

    def login(self):
        print("\n==== Login ====")
        print("Type 'back' at any time to return to Main Menu\n")
        identifier = input("Enter Student ID or Email: ").strip()
        if identifier.lower() == "back":
            return None, None
        password = input("Enter Password: ").strip()
        if password.lower() == "back":
            return None, None

        student = self.user_manager.find_student(identifier)
        if student:
            if student.password == password:
                if student.level is None:
                    inp = input("Enter your level (1-6): ").strip()
                    if inp.lower() == "back":
                        return None, None
                    while True:
                        try:
                            lvl = int(inp)
                            if lvl < 1 or lvl > 6:
                                raise ValueError("Level must be between 1 and 6.")
                            student.level = lvl
                            break
                        except ValueError as e:
                            print(f"Error: {e}")
                            inp = input("Enter your level (1-6): ").strip()
                            if inp.lower() == "back":
                                return None, None
                return "student", student
            else:
                print("Wrong password.")
                return None, None
        admin = self.user_manager.find_admin(identifier)
        if admin:
            if admin.password == password:
                return "admin", admin
            else:
                print("Wrong password.")
                return None, None
        print("User not found.")
        return None, None

# -------------------- Session --------------------
class SessionManager:
    def __init__(self):
        self.current_user = None
        self.current_role = None

    def login(self, role, user):
        self.current_role = role
        self.current_user = user

    def logout(self):
        self.current_user = None
        self.current_role = None

# -------------------- Dashboard --------------------
def student_dashboard(user_manager: UserManager, student: Student):
    while True:
        print("\n==== Student Dashboard ====")
        print("1) Register a Course")
        print("2) Drop a Course")
        print("3) View My Courses")
        print("4) Logout")
        print("5) Back")
        choice = input("Choose: ").strip()
        if choice == "5":
            break
        elif choice == "1":
            level_courses = user_manager.level_courses.get(student.level, [])
            while True:
                print("\nAvailable Courses:")
                for i, c in enumerate(level_courses, start=1):
                    print(f"{i}) {c.code} | {c.name}")
                print(f"{len(level_courses)+1}) Back")
                inp = input("Choose course number: ").strip()
                if inp == str(len(level_courses)+1):
                    break
                try:
                    idx = int(inp)
                    ok, msg = user_manager.register_course(student, idx)
                    print(msg)
                except:
                    print("Invalid input.")
        elif choice == "2":
            if not student.registered_courses:
                print("No courses registered.")
                continue
            while True:
                print("\nYour Registered Courses:")
                for i, c in enumerate(student.registered_courses, start=1):
                    print(f"{i}) {c}")
                print(f"{len(student.registered_courses)+1}) Back")
                inp = input("Choose course number to drop: ").strip()
                if inp == str(len(student.registered_courses)+1):
                    break
                try:
                    idx = int(inp)
                    ok, msg = user_manager.drop_course(student, idx)
                    print(msg)
                except:
                    print("Invalid input.")
        elif choice == "3":
            print("\nYour Courses:", student.registered_courses if student.registered_courses else "None")
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

# -------------------- Main --------------------
def main():
    user_manager = UserManager()
    auth = AuthManager(user_manager)
    session = SessionManager()
    while True:
        print("\n==== Main Menu ====")
        print("1) Register New Student")
        print("2) Login")
        print("3) Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            auth.signup_student()
        elif choice == "2":
            role, user = auth.login()
            if role:
                session.login(role, user)
                print(f"\nLogged in as {role} -> {user.name}")
                if role == "student":
                    student_dashboard(user_manager, user)
                if role == "admin":
                    print("\nWelcome Admin Dashboard (No features yet)")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
