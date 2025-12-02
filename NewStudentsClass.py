# StudentClass.py
# Represents a student model with attributes and methods to manage student data.
# from NewUserClass import User 
import sqlite3

class Student():  

    def __init__(self, student_id, name, email,password, program, level, transcript=None):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.password=password
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
                FROM transcripts
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


        conn = sqlite3.connect("RegistrationSystem.db")
        cursor = conn.cursor()
        cursor.execute(""" SELECT student_id FROM Students WHERE student_id = ? """, (self.student_id,)) # see if the student is in the data base

        student_id = cursor.fetchone()
        if student_id: # if the student in the database add to transcript
            cursor.execute("""
                INSERT INTO transcripts (student_id, course_code, grade)
                VALUES (?, ?, ?)
            """, (self.student_id, course_code, grade))
            conn.commit()

      except Exception as e:
            print("Error adding to transcript:", e)  
      except sqlite3.Error as e:
            print("Database error:", e) 
      finally:
            conn.close()

    
