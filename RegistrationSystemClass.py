import sqlite3
from NewCourseClass import Course
from NewStudentsClass import Student


class RegistrationSystem:
    def __init__(self,db_name="RegistrationSystem.db"):
        self.db_name=db_name
        self.connect=sqlite3.connect(self.db_name) #connect to the database
        self.cursor=self.connect.cursor()     #create a cursor object
        self.create_tables() #Create Courses and Students tables in the database if they don't exist
        
    def create_tables(self): #Method to create Courses and Students tables in the database
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Courses (
                course_code TEXT NOT NULL PRIMARY KEY,
                course_name TEXT NOT NULL,
                credit_hours INTEGER NOT NULL CHECK(credit_hours > 0),
                lecture_hours INTEGER NOT NULL CHECK(lecture_hours >= 0),
                lab_hours INTEGER NOT NULL CHECK(lab_hours >= 0),
                prerequisites TEXT NOT NULL,
                maximum_capacity INTEGER NOT NULL CHECK(maximum_capacity > 0),
                program TEXT NOT NULL CHECK(program IN ('Computer', 'Power', 'Biomedical', 'Communication')),
                level INTEGER NOT NULL CHECK(level IN (1, 2, 3, 4))
                );''') #create Courses table if it doesn't exist
            

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Students (
                                    student_id TEXT PRIMARY KEY NOT NULL ,
                                    name TEXT NOT NULL ,
                                    email TEXT NOT NULL CHECK (email LIKE '%_@__%.__%'),
                                    program TEXT NOT NULL CHECK (program IN ('Computer', 'Power', 'Biomedical', 'Communication')),
                                    current_level INTEGER NOT NULL CHECK (current_level BETWEEN 1 AND 4)
                                )''') #create Students table if it doesn't exist
            

            self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS transcripts (
                                student_id TEXT NOT NULL,
                                course_code TEXT NOT NULL,
                                grade TEXT  NOT NULL CHECK (grade IN ('A', 'B', 'C', 'D', 'F', 'A+', 'B+', 'C+', 'D+')),
                                FOREIGN KEY(student_id) REFERENCES students(student_id),
                                FOREIGN KEY(course_code) REFERENCES courses(course_code)
                                )
                                """) #create Transcript table if it doesn't exist 
            self.cursor.execute('''
                                CREATE TABLE IF NOT EXISTS Enrollments (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    student_id TEXT NOT NULL,
                                    course_code TEXT NOT NULL,
                                    FOREIGN KEY(student_id) REFERENCES Students(student_id),
                                    FOREIGN KEY(course_code) REFERENCES Courses(course_code)
                                );
                            ''') #create Enrollments table if it doesn't exist
          
            
            # Faculty Module Tables==================================================================
            # Faculty table - stores basic faculty information
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS faculty (
                    faculty_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            ''')
            
            # Faculty preferences table - stores preferred courses for each faculty
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS faculty_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    faculty_id TEXT,
                    course_code TEXT,
                    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
                    UNIQUE(faculty_id, course_code)
                )
            ''')
            
            # Faculty availability table - stores available time slots for each faculty
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS faculty_availability (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    faculty_id TEXT,
                    day TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
                )
            ''')
            
            # Faculty assignments table - stores course assignments to faculty
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS faculty_assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    faculty_id TEXT,
                    course_code TEXT,
                    semester TEXT,
                    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
                    FOREIGN KEY (course_code) REFERENCES Courses(course_code),
                    UNIQUE(course_code, semester)
                )
            ''')
#=======================================================================================================
            self.connect.commit() #commit the changes
        except sqlite3.Error as e:
            print(f"An error occurred while creating the tables: {e}")


    def add_course(self, course):
        """
        Adds a Course object to the Courses table in the database.
        """
        try:
            self.connect=sqlite3.connect(self.db_name) #connect to the database
            self.cursor=self.connect.cursor()     #create a cursor object

            if isinstance(course.prerequisites, list) : #Convert prerequisites list to comma-separated string
                prerequisites = ",".join(map(str,course.prerequisites))  #Join list elements with commas
            else:
                prerequisites=""

            self.cursor.execute('''INSERT INTO Courses (course_code, course_name, credit_hours, lecture_hours, lab_hours, prerequisites, maximum_capacity, program, level)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                (course.course_code, course.name, course.credits, course.lecture_hours, course.lab_hours, prerequisites, course.max_capacity, course.program, course.level)) #insert course data into Courses table

            self.connect.commit() #commit the changes 
            print(f"Course {course.name} with code {course.course_code} added to database.")
        except sqlite3.IntegrityError as e: #handle integrity errors (e.g., duplicate course_code)
            print(f"An integrity error occurred while adding the course: {e}")
        except sqlite3.Error as e:
            print(f"An error occurred while adding the course: {e}")
        finally:
            self.connect.close()#close the connection



    def add_student(self, student):
        """
        Adds a Student object to the Students table in the database.
        """
        try:
            self.connect=sqlite3.connect(self.db_name) #connect to the database
            self.cursor=self.connect.cursor()     #create a cursor object

            self.cursor.execute('''INSERT INTO Students (student_id, name, email, program, current_level)
                                VALUES (?, ?, ?, ?, ?)''',
                                (student.student_id, student.name, student.email, student.program, student.level)) #insert student data into Students table
            

            for course_code, grade in student.transcript:
                self.cursor.execute('''INSERT INTO transcripts (student_id, course_code, grade)
                                    VALUES (?, ?, ?)''',
                                    (student.student_id, course_code, grade)) #insert transcript data into transcripts table
                
                
            self.connect.commit() #commit the changes 
            print(f"Student {student.name} with ID {student.student_id} added to database.")
        except sqlite3.IntegrityError as e: #handle integrity errors (e.g., duplicate student_id)
            print(f"An integrity error occurred while adding the student: {e}")
        except sqlite3.Error as e:
            print(f"An error occurred while adding the student: {e}")
        finally:
            self.connect.close()#close the connection
    
    def get_available_courses(self, program, level):
        """
        Retrieves a list of available courses for a given program and level.
        """
        try:
            self.connect=sqlite3.connect(self.db_name) #connect to the database
            self.cursor=self.connect.cursor()     #create a cursor object

            self.cursor.execute('''SELECT * FROM Courses WHERE program=? AND level=?''', (program, level))
            courses = self.cursor.fetchall() #fetch all matching courses

            return courses
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving available courses: {e}")
            return []
        finally:
            self.connect.close()#close the connection
        

    def  validate_schedule(self, student_id, selected_courses):
        """
        Validates if a student can register for the selected courses.
        Checks prerequisites and maximum capacity.
        selected_courses: list of course_codes
        """
        try:
            self.connect=sqlite3.connect(self.db_name) #connect to the database
            self.cursor=self.connect.cursor()     #create a cursor object

            # Fetch student's completed courses
            self.cursor.execute('''SELECT course_code, grade FROM transcripts WHERE student_id=?''', (student_id,))
            student_transcript = [(row[0],row[1]) for row in self.cursor.fetchall()]
            for course_code in selected_courses:
                

                # Get course data directly
                self.cursor.execute("""
                    SELECT credit_hours, lecture_hours, lab_hours,
                        prerequisites, maximum_capacity, program, level, course_name
                    FROM Courses
                    WHERE course_code = ?
                """, (course_code,))

                data = self.cursor.fetchone()

                if not data:
                    print(f"Course {course_code} not found.")
                    return False

                credit, lec, lab, prereq_str, max_cap, program, level, name = data

                # Convert prerequisites string to list
                prereq_list = [p for p in prereq_str.split(",") if p.strip()]

                # Build a Course object
                course_obj = Course(
                    course_code,name,credit,lec,lab,prereq_list,max_cap,program,level)

                # Now use the required method
                if not course_obj.check_prerequisites(student_transcript):
                    print(f"Student does NOT meet prerequisites for {course_code}.")
                    return False


                # Check maximum capacity
                self.cursor.execute('''SELECT COUNT(*) FROM Enrollments WHERE course_code=?''', (course_code,))
                enrolled_count = self.cursor.fetchone()[0]
                if enrolled_count >= int(max_cap):
                    print(f"Course {course_code} has reached maximum capacity.")
                    return False
                
            return True  # All checks passed
        except sqlite3.Error as e:
            print(f"An error occurred while validating schedule: {e}")
            return False
        finally:
            self.connect.close()#close the connection
        
        
    def register_student(self, student_id, selected_courses):
        """
        Registers a student for the selected courses if validation passes.
        selected_courses: list of course_codes
        """
        if not self.validate_schedule(student_id, selected_courses):
            print(f"Registration failed for student {student_id}.")
            return False

        try:
            self.connect=sqlite3.connect(self.db_name) #connect to the database
            self.cursor=self.connect.cursor()     #create a cursor object

            for course_code in selected_courses:
                self.cursor.execute('''INSERT INTO Enrollments (student_id, course_code) VALUES (?, ?)''', (student_id, course_code))
            self.connect.commit() #commit the changes

            print(f"Student {student_id} successfully registered for courses: {', '.join(selected_courses)}.")
            return True
        except sqlite3.Error as e:
            print(f"An error occurred while registering student: {e}")
            return False
        finally:
            self.connect.close() #close the connection

    #abdullah-eduit-for the conect the data ===========================================================
    def get_course_enrollment_data(self):
    """
    Fetches the course code, maximum capacity, and current number of enrolled 
    students for all courses by joining the Courses and Enrollments tables.

    Returns:
        A list of tuples: [(course_code, max_capacity, current_enrollment), ...]
    """
    conn = None
    try:
        # Re-establish connection for thread safety/proper closing
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # SQL Query to aggregate enrollment data
        query = """
        SELECT
            c.course_code,
            c.maximum_capacity,
            COUNT(e.student_id) AS current_enrollment
        FROM
            Courses c
        LEFT JOIN
            Enrollments e ON c.course_code = e.course_code
        GROUP BY
            c.course_code, c.maximum_capacity
        ORDER BY
            c.course_code;
        """
        cursor.execute(query)
        data = cursor.fetchall()
        
        return data
    
    except sqlite3.Error as e:
        print(f"Database error while fetching enrollment data: {e}")
        return []
    
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()
#================================================================================================================
        
    def delete_student(self, student_id):
        """
        Deletes a student from the Students table in the database.
        """
        try:
            self.connect=sqlite3.connect(self.db_name) #connect to the database
            self.cursor=self.connect.cursor()     #create a cursor object

            self.cursor.execute('''DELETE FROM Enrollments WHERE student_id=?''', (student_id,)) #delete student's enrollment records

            self.cursor.execute('''DELETE FROM transcripts WHERE student_id=?''', (student_id,)) #delete student's transcript records

            self.cursor.execute('''DELETE FROM Students WHERE student_id=?''', (student_id,)) #delete student from Students table

            self.connect.commit() #commit the changes
            print(f"Student with ID {student_id} deleted from database.")
        except sqlite3.Error as e:
            print(f"An error occurred while deleting the student: {e}")
        finally:
            self.connect.close()#close the connection
    
    def drop_all_tables(self):
        """
        Drops all tables in the database.
        """
        try:
            self.connect=sqlite3.connect(self.db_name) #connect to the database
            self.cursor=self.connect.cursor()     #create a cursor object

            self.cursor.execute('''DROP TABLE IF EXISTS Enrollments''')
            self.cursor.execute('''DROP TABLE IF EXISTS transcripts''')
            self.cursor.execute('''DROP TABLE IF EXISTS Students''')
            self.cursor.execute('''DROP TABLE IF EXISTS Courses''')

            self.connect.commit() #commit the changes
            
            print("All tables dropped from database.")
        except sqlite3.Error as e:
            print(f"An error occurred while dropping tables: {e}")
        finally:
            self.connect.close()#close the connection
