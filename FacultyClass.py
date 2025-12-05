# FacultyClass.py

class Faculty:
    def __init__(self, faculty_id, name,email,password, course_prefernces =None, availability = None):
        
        self.faculty_id = faculty_id
        self.name = name
        self.email = email
        self.password = password

        self.course_prefernces = course_prefernces
        self.availability = availability
        
    def __str__(self):
        return f"Faculty ID: {self.faculty_id}, Name: {self.name}"