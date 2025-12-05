# FacultyModule.py

from RegistrationSystemClass import RegistrationSystem
from FacultyClass import Faculty 
from TimeBuilder import ScheduleSystem
import sqlite3


class FacultyAdminModule:
    def __init__(self,db_name="RegistrationSystem.db"):
        self.db_name = db_name
        self.connect = sqlite3.connect(self.db_name)
        self.cursor = self.connect.cursor()
        
    def add_faculty(self,faculty):
        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            ## insert faculty object to database
            self.cursor.execute('''
                INSERT INTO Faculty (faculty_id,name,email,password)
                VALUES (?, ?, ?, ?)
            ''',
            (faculty.faculty_id,faculty.name,faculty.email,faculty.password))

            self.connect.commit()
            print(f"Faculty {faculty.name} with code {faculty.faculty_id} added to database.")

        except sqlite3.IntegrityError as e:
            # Handles duplicate faculty id or other integrity constraints
            print(f"An integrity error occurred while adding the faculty: {e}")
        except sqlite3.Error as e:
            print(f"An error occurred while adding the faculty: {e}")
        finally:
            # Always close the connection at the end
            self.connect.close()


    def set_course_preferences(self, faculty_id, course_list):

        pref_str = ",".join(course_list)  ## create a string from courses list

        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            self.cursor.execute("""
                UPDATE Faculty
                SET course_preferences = ?
                WHERE faculty_id = ?
            """, (pref_str, faculty_id))  ## change course preferences in database

            self.connect.commit()
            print("Course preferences updated.")

        except sqlite3.Error as e:
            print("Error:", e)

        finally:
            self.connect.close()

    def set_availability(self, faculty_id, availability_blocks):

        ## availability blocks must be entered this way: 
        ## ["Sun 10:00-12:00", "Tue 14:00-16:00"]

        availability_string = ",".join(availability_blocks) ## create availability string from list 

        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            self.cursor.execute("""
                UPDATE Faculty
                SET availability = ?
                WHERE faculty_id = ?
            """, (availability_string, faculty_id))  ## set availability in database

            self.connect.commit()
            print("Availability updated.")

        except sqlite3.Error as e:
            print("Error:", e)

        finally:
            self.connect.close()        

    def assign_course_to_faculty(self, faculty_id, course_code):
        ##Checks: faculty availability and course schedule and noo schedule conflicts with other assigned courses


        ## fetch currently assigned courses to faculty member
        assigned = self.get_assigned_courses(faculty_id)

        # add new courses to currently assigned
        new_assignment = assigned + [course_code]

        
        ## check conflicts using detect faculty conflicts method
        if not self.detect_faculty_conflicts(faculty_id, new_assignment):
            print("conflict detected failed to add course")
            return False

        ## save assignment as commas string 
        assigned_str = ",".join(new_assignment)


        ## store in database
        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            self.cursor.execute("""
                UPDATE Faculty
                SET assigned_courses = ?
                WHERE faculty_id = ?
            """, (assigned_str, faculty_id))

            self.connect.commit()
            print(f"Course {course_code} assigned to faculty {faculty_id}.")

            return True

        except sqlite3.Error as e:
            print("Error assigning course:", e)
            return False

        finally:
            self.connect.close()


    def get_assigned_courses(self, faculty_id):
        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            self.cursor.execute("""
                SELECT assigned_courses
                FROM Faculty
                WHERE faculty_id = ?
            """, (faculty_id,))
            row = self.cursor.fetchone()

            if not row or not row[0]:
                return []

            return [c.strip() for c in row[0].split(",") if c.strip()]

        except sqlite3.Error as e:
            print("Error:", e)
            return []

        finally:
            self.connect.close()


    def detect_faculty_conflicts(self, faculty_id, course_list):

        ## Checks time conflicts between all assigned courses and the new course being assigned
        schedule_sys = ScheduleSystem(self.db_name)

        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            # Build all schedule_id packages for the faculty
            all_schedule_ids = []

            for course in course_list:
                self.cursor.execute("""
                    SELECT schedule_id
                    FROM CourseSchedule
                    WHERE course_code = ?
                """, (course,))
                rows = self.cursor.fetchall()

                for r in rows:
                    all_schedule_ids.append(r[0])

            # Use TimeBuilder conflict checker
            status = schedule_sys.has_conflict("any_id", all_schedule_ids)   ## using has conflict in time builder class 

            # has conflict method requires student id as parameter but we send a mock id to use function

            return status == "OK"

        except sqlite3.Error as e:
            print("Conflict check error:", e)
            return False

        finally:
            self.connect.close()
