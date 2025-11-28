# FacultyClass.py

class Faculty:
    def __init__(self, faculty_id, name):
        # Faculty unique ID
        self.faculty_id = faculty_id
        # Faculty Name
        self.name = name

    def __str__(self):
        return f"Faculty ID: {self.faculty_id}, Name: {self.name}"
