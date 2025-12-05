# FacultyModule.py

from RegistrationSystemClass import RegistrationSystem
from FacultyClass import Faculty 
import sqlite3


class FacultyAdminModule:
    def __init__(self, system: RegistrationSystem):
        self.system = system
        
    def setup_and_test(self):

        print("\n--- ADDING FACULTY ---")
        f1 = Faculty(1001, "Dr. Ahmed","drahmad@gmail.com","@Aa112233")
        f2 = Faculty(1002, "Dr. Omar", "dromar@gmail.com","@Oo112233")
        self.system.add_faculty(f1)
        self.system.add_faculty(f2)

        # ---------------------------------------
        # Use ONLY system connection (NO new sqlite3.connect)
        # ---------------------------------------
        print("\n--- INSERTING COURSE AND SECTIONS ---")
        self.system.connect = sqlite3.connect(self.system.db_name)
        self.system.cursor = self.system.connect.cursor()

        self.system.cursor.execute("""
            INSERT INTO Courses VALUES
            ('CPE401','Programming I',3,3,0,'',30,'Computer',1)
        """)

        self.system.cursor.execute("""
            INSERT INTO CourseSchedule(course_code,section,start_time,end_time,lecture_type,days)
            VALUES ('CPE401','A','10:00','12:00','Lecture','Sun, Tue')
        """)

        self.system.cursor.execute("""
            INSERT INTO CourseSchedule(course_code,section,start_time,end_time,lecture_type,days)
            VALUES ('CPE401','B','14:00','16:00','Lecture','Mon, Wed')
        """)

        self.system.connect.commit()
        self.system.connect.close()

        # ---------------------------------------
        # Preferences and Availability
        # ---------------------------------------
        print("\n--- SETTING PREFERENCES ---")
        self.system.set_course_preferences(1001, ["CPE401"])

        print("\n--- SETTING AVAILABILITY ---")
        self.system.set_availability(1001, ["Sun 09:00-13:00", "Tue 09:00-13:00"])

        # ---------------------------------------
        # Assign
        # ---------------------------------------
        print("\n--- ASSIGNING COURSE CPE401 ---")
        success = self.system.assign_course_to_faculty(1001, "CPE401")
        print("Assignment result:", success)

        # ---------------------------------------
        # Show output
        # ---------------------------------------
        print("\n--- FACULTY ASSIGNED COURSES ---")
        print(self.system.get_assigned_courses(1001))


        print("\nTEST COMPLETE.")



# Example Usage:
if __name__ == '__main__':
    reg_system = RegistrationSystem()
    
    admin_module = FacultyAdminModule(reg_system)
    admin_module.setup_and_test()
