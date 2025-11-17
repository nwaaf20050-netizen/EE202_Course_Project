
class Student:
    def __init__(self, student_id: str, name: str, email: str, password: str, program: str, level: int):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.password = password
        self.program = program
        self.level = level

    def __repr__(self):
        return f"<Student {self.student_id} | {self.name}>"



class Admin:
    def __init__(self, Email: str, name: str, password: str):
        self.Email = Email
        self.name = name
        self.password = password
        self.identifier = Email 

    def __repr__(self):
        return f"<Admin {self.identifier} | {self.name}>"



class UserManager:
    def __init__(self):
        self.students = []
        self.admins = []
        self.admins.append(Admin("admin@ece.example", "Main Admin", "admin123"))

    def add_student(self, student: Student):
        for s in self.students:
            if s.student_id == student.student_id:
                return False, "Student ID already exists."
            if s.email == student.email:
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



class AuthManager:
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager

    def signup_student(self):
        print("\n==== Student Registration ====")
        student_id = input("Enter Student ID: ").strip()
        name = input("Enter Name: ").strip()
        email = input("Enter Email: ").strip()
        password = input("Enter Password: ").strip()
        program = input("Enter Program: ").strip()
        level = int(input("Enter Level: ").strip())

        new_student = Student(student_id, name, email, password, program, level)

        ok, msg = self.user_manager.add_student(new_student)
        print(msg)

    def login(self):
        print("\n==== Login ====")
        identifier = input("Enter Student ID or Email: ").strip()
        password = input("Enter Password: ").strip()

        student = self.user_manager.find_student(identifier)
        if student:
            if student.password == password:
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

    def is_logged_in(self):
        return self.current_user is not None

    def get_user(self):
        return self.current_user



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
                    print("\nWelcome Student Dashboard")
                    print(f"Your Program: {user.program}")
                    print(f"Your Level: {user.level}")

                if role == "admin":
                    print("\nWelcome Admin Dashboard")

        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()

