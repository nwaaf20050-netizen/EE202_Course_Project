# FacultyModule.py

from RegistrationSystemClass import RegistrationSystem
from FacultyClass import Faculty 
import sqlite3

class FacultyAdminModule:
    def __init__(self, system: RegistrationSystem):
        self.system = system
        
    def setup_and_test(self):
        """Runs the setup and assignment tests for Faculty Management."""
        print("\n--- Running Faculty Management Tests (Requirement 6) ---")
        
        # 1. Add Faculty
        f1 = Faculty("F101", "Dr. Ahmed")
        f2 = Faculty("F102", "Dr. Sara")
        self.system.add_faculty(f1)
        self.system.add_faculty(f2)
        
        # 2. Add sample course (Required for assignment check to pass)
        # Using simple direct DB insert for test data setup:
        conn = sqlite3.connect("RegistrationSystem.db")
        cursor = conn.cursor()
        # Add a dummy course if it doesn't exist
        cursor.execute("INSERT OR IGNORE INTO Courses (course_code, course_name, credit_hours, lecture_hours, lab_hours, prerequisites, maximum_capacity, program, level) VALUES ('COE301', 'Data Structures', 3, 3, 1, 'None', 40, 'Computer', 3)")
        conn.commit()
        conn.close()
        
        # 3. TEST 1: Successful assignment
        print("\nTEST 1: Assign COE301 to F101 (Expected Success)")
        self.system.assign_course_to_faculty(course_code="COE301", faculty_id="F101")
        
        # 4. TEST 2: Conflict Check (Assign the same course again)
        print("\nTEST 2: Assign COE301 to F102 (Expected Fail - Conflict)")
        self.system.assign_course_to_faculty(course_code="COE301", faculty_id="F102")

        # 5. TEST 3: Assign a non-existent course
        print("\nTEST 3: Assign XYZ999 to F101 (Expected Fail - Course Not Found)")
        self.system.assign_course_to_faculty(course_code="XYZ999", faculty_id="F101")


# Example Usage:
if __name__ == '__main__':
    reg_system = RegistrationSystem()
    
    admin_module = FacultyAdminModule(reg_system)
    admin_module.setup_and_test()