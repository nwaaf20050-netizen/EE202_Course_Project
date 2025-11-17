# StudentClass.py
# Represents a student model with attributes and methods to manage student data.

import NewUserClass
import sqlite3

class Student(NewUserClass.User):

    def __init__(self, id_number, name, email, program, level, transcript=None):
        super().__init__(name, email, id_number)
        self.program = program  # Must be from the defined list
        self.level = level

        # Transcript is a list of tuples: (course_code, grade)
        self.transcript = transcript if transcript else []

    def get_completed_credits(self):
       # Calculate total completed credits based on transcript
        try:
            connect = sqlite3.connect("RegistrationSystem.db")
            cursor = connect.cursor()

            cursor.execute("""
                SELECT course_code, grade
                FROM Transcripts
                WHERE student_id = ?
            """, (self.student_id,)) # Fetch transcript entries for the student

            rows = cursor.fetchall()

            total_credits = 0

            for course_code, grade in rows: # Iterate through transcript entries
                if grade.upper() == 'F':
                    continue

                cursor.execute("""
                    SELECT credit_hours
                    FROM Courses
                    WHERE course_code = ?
                """, (course_code,)) # Fetch credit hours for the course

                result = cursor.fetchone()

                if result is not None: # If course found, add its credits
                    credit_hours = result[0] 
                    total_credits += credit_hours  # Add credits to total
            connect.close()
            return total_credits
        except sqlite3.Error as e:
                print("Database error:", e)
                return None
        
    

    def add_to_transcript(self, course_code,grade):

      # Add a course and grade to the transcript if not already present
      try:
        existing_course_codes = [course_codes_in_transcript 
                                 for (course_codes_in_transcript, grades_in_transcript) in self.transcript]
        
        if course_code not in existing_course_codes and grade.upper() in ['A', 'B', 'C', 'D', 'F', 'A+', 'B+', 'C+', 'D+'] :
        
            self.transcript.append((course_code,grade))
        else:
            print(f"Invalid entry or course {course_code} already in transcript.")
      except Exception as e:
            print("Error adding to transcript:", e)   
    
