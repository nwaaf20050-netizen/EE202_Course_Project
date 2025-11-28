import random
import re

# -------------------- Classes --------------------
class Student:
    """Represents a student with ID, name, email, password, level, and registered courses."""
    def __init__(self, student_id, name, email, password, level=None):
        self.student_id = student_id
        self.name = name.strip()
        self.email = email.strip()
        self.password = password.strip()
        self.level = level
        self.registered_courses = {}  # course_code: time

    def __repr__(self):
        return f"<Student {self.student_id} | {self.name}>"

class Admin:
    """Represents an admin with admin_id, name, email, and password."""
    def __init__(self, admin_id, name, email, password):
        self.admin_id = admin_id
        self.name = name.strip()
        self.email = email.strip()
        self.password = password.strip()

    def __repr__(self):
        return f"<Admin {self.admin_id} | {self.name}>"

class Course:
    """Represents a course with a code, name, and available times."""
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.times = ["9-10", "10-12", "1-3"]  # default times

    def __repr__(self):
        return f"{self.code} - {self.name} | Times: {self.times}"

# -------------------- UserManager --------------------
class UserManager:
    """Manages students, admins, and level-wise courses."""
    def __init__(self):
        self.students = []
        self.admins = []
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

    # -------------------- ID Generators --------------------
    def generate_student_id(self):
        while True:
            sid = "25" + str(random.randint(10000, 99999))
            if not any(s.student_id == sid for s in self.students):
                return sid

    def generate_admin_id(self):
        while True:
            aid = "05" + str(random.randint(100, 999))
            if not any(a.admin_id == aid for a in self.admins):
                return aid

    # -------------------- Add Users --------------------
    def add_student(self, student):
        if any(s.email == student.email for s in self.students):
            return False, "Email already exists."
        self.students.append(student)
        return True, "Student registered successfully."

    def add_admin(self, admin):
        if any(a.email == admin.email for a in self.admins):
            return False, "Email already exists."
        self.admins.append(admin)
        return True, "Admin registered successfully."

    # -------------------- Find Users --------------------
    def find_student(self, identifier):
        for s in self.students:
            if s.student_id == identifier or s.email == identifier:
                return s
        return None

    def find_admin(self, identifier):
        for a in self.admins:
            if a.admin_id == identifier or a.email == identifier:
                return a
        return None

# -------------------- Validation --------------------
ALLOWED_DOMAINS = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "kau.edu.sa"]

def validate_fullname(name):
    return len(name.strip().split()) >= 3

def validate_email(email):
    email = email.strip()
    match = re.match(r'^[\w\.-]+@([\w\.-]+)$', email)
    if not match:
        return False
    domain = match.group(1)
    return domain in ALLOWED_DOMAINS

def validate_password(password):
    password = password.strip()
    if len(password) < 5:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-]", password):
        return False
    return True

# -------------------- AuthManager --------------------
class AuthManager:
    def __init__(self, user_manager):
        self.user_manager = user_manager

    # -------------------- Signup Student --------------------
    def signup_student(self):
        print("\n==== Student Registration ====")
        while True:
            name = input("Enter full name (3 parts) or 'back' to return: ").strip()
            if name.lower() == "back":
                return
            if validate_fullname(name):
                break
            print("Error: Name must contain at least 3 parts.")

        while True:
            email = input("Enter email or 'back' to return: ").strip()
            if email.lower() == "back":
                return
            if not validate_email(email):
                print("Error: Email not allowed. Allowed: gmail, hotmail, yahoo, outlook, kau.edu.sa")
                continue
            if any(s.email == email for s in self.user_manager.students):
                print("Error: Email already exists.")
                continue
            break

        while True:
            password = input("Enter password (5+ chars, 1 uppercase, 1 number, 1 symbol) or 'back': ").strip()
            if password.lower() == "back":
                return
            if validate_password(password):
                break
            print("Error: Password does not meet requirements.")

        student_id = self.user_manager.generate_student_id()
        new_student = Student(student_id, name, email, password)
        self.user_manager.add_student(new_student)
        print(f"Student registered! ID: {student_id}")

    # -------------------- Signup Admin --------------------
    def signup_admin(self):
        print("\n==== Admin Registration ====")
        while True:
            name = input("Enter full name (3 parts) or 'back': ").strip()
            if name.lower() == "back":
                return
            if validate_fullname(name):
                break
            print("Error: Name must contain at least 3 parts.")

        while True:
            email = input("Enter email or 'back': ").strip()
            if email.lower() == "back":
                return
            if not validate_email(email):
                print("Error: Email not allowed. Allowed: gmail, hotmail, yahoo, outlook, kau.edu.sa")
                continue
            if any(a.email == email for a in self.user_manager.admins):
                print("Error: Email already exists.")
                continue
            break

        while True:
            password = input("Enter password (5+ chars, 1 uppercase, 1 number, 1 symbol) or 'back': ").strip()
            if password.lower() == "back":
                return
            if validate_password(password):
                break
            print("Error: Password does not meet requirements.")

        admin_id = self.user_manager.generate_admin_id()
        new_admin = Admin(admin_id, name, email, password)
        self.user_manager.add_admin(new_admin)
        print(f"Admin registered! ID: {admin_id}")

    # -------------------- Login --------------------
    def login(self):
        identifier = input("Enter Student/Admin ID or Email or 'back': ").strip()
        if identifier.lower() == "back":
            return None, None
        password = input("Enter password or 'back': ").strip()
        if password.lower() == "back":
            return None, None

        student = self.user_manager.find_student(identifier)
        if student and password.strip() == student.password:
            if student.level is None:
                while True:
                    lvl = input("Enter your level (1-6) or 'back': ").strip()
                    if lvl.lower() == "back":
                        return None, None
                    if lvl.isdigit() and 1 <= int(lvl) <= 6:
                        student.level = int(lvl)
                        break
                    print("Invalid level.")
            return "student", student

        admin = self.user_manager.find_admin(identifier)
        if admin and password.strip() == admin.password:
            return "admin", admin

        print("Invalid login.")
        return None, None

# -------------------- Dashboards --------------------
def student_dashboard(student, user_manager):
    while True:
        print("\n--- Student Dashboard ---")
        print("1. Register Course")
        print("2. Drop Course")
        print("3. View My Courses")
        print("4. Back")
        choice = input("Choose: ").strip()

        if choice == "4":
            return

        elif choice == "1":
            courses = user_manager.level_courses.get(student.level, [])
            if not courses:
                print("No courses available.")
                continue
            while True:
                print("Available Courses:")
                for i, c in enumerate(courses, 1):
                    print(f"{i}. {c.code} - {c.name} | Times: {c.times}")
                print(f"{len(courses)+1}. Back")
                inp = input("Choose course number or 'back': ").strip()
                if inp.lower() == "back" or inp == str(len(courses)+1):
                    break
                if not inp.isdigit() or int(inp) < 1 or int(inp) > len(courses):
                    print("Invalid choice.")
                    continue
                course = courses[int(inp)-1]
                while True:
                    print("Available times:", course.times)
                    time_choice = input("Choose time or 'back': ").strip()
                    if time_choice.lower() == "back":
                        break
                    if time_choice not in course.times:
                        print("Invalid time.")
                        continue
                    student.registered_courses[course.code] = time_choice
                    print(f"Course {course.code} registered at {time_choice}.")
                    break
                break

        elif choice == "2":
            if not student.registered_courses:
                print("No courses registered.")
                continue
            while True:
                for i, (c, t) in enumerate(student.registered_courses.items(), 1):
                    print(f"{i}. {c} -> {t}")
                print(f"{len(student.registered_courses)+1}. Back")
                inp = input("Choose course number to drop or 'back': ").strip()
                if inp.lower() == "back" or inp == str(len(student.registered_courses)+1):
                    break
                if not inp.isdigit() or int(inp) < 1 or int(inp) > len(student.registered_courses):
                    print("Invalid choice.")
                    continue
                key = list(student.registered_courses.keys())[int(inp)-1]
                del student.registered_courses[key]
                print(f"Course {key} dropped.")
                break

        elif choice == "3":
            if not student.registered_courses:
                print("No courses registered.")
            else:
                for c, t in student.registered_courses.items():
                    print(f"{c} -> {t}")
        else:
            print("Invalid choice.")

# -------------------- Admin Dashboard --------------------
def admin_dashboard(admin, user_manager, auth):
    while True:
        print("\n--- Admin Dashboard ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Add Course")
        print("4. Delete Course")
        print("5. Add Time to Course")
        print("6. Back")
        choice = input("Choose: ").strip()

        if choice == "6":
            return
        elif choice == "1":
            auth.signup_student()
        elif choice == "2":
            for s in user_manager.students:
                print(s)
        elif choice == "3":
            while True:
                level = input("Enter level 1-6 or 'back': ").strip()
                if level.lower() == "back":
                    break
                if level.isdigit() and 1 <= int(level) <= 6:
                    code = input("Enter course code: ").strip()
                    name = input("Enter course name: ").strip()
                    user_manager.level_courses[int(level)].append(Course(code, name))
                    print(f"Course {code} added to level {level}.")
                    break
                print("Invalid level.")
        elif choice == "4":
            while True:
                level = input("Enter level 1-6 or 'back': ").strip()
                if level.lower() == "back":
                    break
                if level.isdigit() and 1 <= int(level) <= 6:
                    courses = user_manager.level_courses[int(level)]
                    for i, c in enumerate(courses, 1):
                        print(f"{i}. {c.code} - {c.name}")
                    inp = input("Choose course number to delete or 'back': ").strip()
                    if inp.lower() == "back":
                        break
                    if inp.isdigit() and 1 <= int(inp) <= len(courses):
                        removed = courses.pop(int(inp)-1)
                        print(f"Course {removed.code} removed.")
                        break
                    print("Invalid choice.")
                    break
                print("Invalid level.")
        elif choice == "5":
            while True:
                level = input("Enter level 1-6 or 'back': ").strip()
                if level.lower() == "back":
                    break
                if level.isdigit() and 1 <= int(level) <= 6:
                    courses = user_manager.level_courses[int(level)]
                    for i, c in enumerate(courses, 1):
                        print(f"{i}. {c.code} - {c.name} | Times: {c.times}")
                    inp = input("Choose course number to add time or 'back': ").strip()
                    if inp.lower() == "back":
                        break
                    if inp.isdigit() and 1 <= int(inp) <= len(courses):
                        time = input("Enter new time (e.g., 2-4): ").strip()
                        courses[int(inp)-1].times.append(time)
                        print("Time added.")
                        break
                    print("Invalid choice.")
                    break
                print("Invalid level.")
        else:
            print("Invalid choice.")

# -------------------- Main --------------------
def main():
    user_manager = UserManager()
    auth = AuthManager(user_manager)

    while True:
        print("\n=== Main Menu ===")
        print("1. Login")
        print("2. Register Student")
        print("3. Register Admin")
        print("4. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            role, user = auth.login()
            if role == "student":
                student_dashboard(user, user_manager)
            elif role == "admin":
                admin_dashboard(user, user_manager, auth)

        elif choice == "2":
            auth.signup_student()

        elif choice == "3":
            auth.signup_admin()

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
