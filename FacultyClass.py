# FacultyClass.py

class Faculty:
    def __init__(self, faculty_id, name,email,password, course_preferences =None, availability = None):
        
        self.faculty_id = faculty_id
        self.name = name
        self.email = email
        self.password = password

        self.course_preferences = course_preferences
        self.availability = availability
        
    def __str__(self):
        return f"Faculty ID: {self.faculty_id}, Name: {self.name}"