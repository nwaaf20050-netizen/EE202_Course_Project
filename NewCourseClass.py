# CourseClass.py
# Represents a course model with attributes and methods to manage course data.
import sqlite3
class Course:

    def __init__(self,course_code,name,credits,lecture_hours,lab_hours,prerequisites,max_capacity,program,level):
        # Attributes defined in project requirements
        self.course_code = course_code
        self.name = name
        self.credits = credits
        self.lecture_hours = lecture_hours
        self.lab_hours = lab_hours
        self.prerequisites = prerequisites  # list of course codes
        self.max_capacity = max_capacity
        self.program = program
        self.level = level

        # System-managed attribute
        self.enrolled_students = 0  

    def is_full(self):
        """Checks if the course reached maximum capacity"""
        try:
            connect= sqlite3.connect("RegistrationSystem.db")
            cursor= connect.cursor()

            cursor.execute('''SELECT COUNT(*) FROM Enrollments WHERE course_code=?''', (self.course_code,))

            self.enrolled_students=cursor.fetchone()[0]

            connect.close()

            return self.enrolled_students >= self.max_capacity
        
        except sqlite3.Error as e:
            print(f"error checking course capacity: {e}")
            return False

            

    def check_prerequisites(self, student_transcript):
        """
        Checks if the student has completed all prerequisite courses with a passing grade.
        
        student_transcript format:
            [
                ("EE201", "B"),
                ("MATH101", "A"),
                ("PHY101", "F")
            ]
        """
        try:
            # Extract only passed courses (grade != 'F')
            passed_courses = [
                course_code for (course_code, grade) in student_transcript if grade.upper() != 'F'
            ]
            # Check if ALL prerequisites are in the passed courses list
            return all(req in passed_courses 
                       for req in self.prerequisites)
        
        except (ValueError,TypeError) as e:
            print(f"error checking prerequisites: {e}")
            return False