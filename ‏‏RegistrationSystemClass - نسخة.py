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
                program TEXT NOT NULL,
                level INTEGER NOT NULL CHECK(level IN (1, 2, 3, 4))
                );''') #create Courses table if it doesn't exist
            

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Students (
                                    student_id TEXT PRIMARY KEY NOT NULL ,
                                    name TEXT NOT NULL ,
                                    email TEXT NOT NULL CHECK (email LIKE '%_@__%.__%'),
                                    password TEXT NOT NULL, 
                                    program TEXT NOT NULL CHECK (program IN ('Computer', 'Power', 'Biomedical', 'Communication')),
                                    current_level INTEGER NOT NULL CHECK (current_level BETWEEN 1 AND 4)
                                )''') #create Students table if it doesn't exist
            
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Admin (
                                    admin_id TEXT PRIMARY KEY NOT NULL ,
                                    name TEXT NOT NULL ,
                                    email TEXT NOT NULL CHECK (email LIKE '%_@__%.__%'),
                                    password TEXT NOT NULL
                                )''') #create Admin table if it doesn't exist
            

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
            
                #Convert prerequisites to clean comma-separated string
            if isinstance(course.prerequisites, list):
                # Convert list → comma string
                prerequisites = ",".join([p.strip() for p in course.prerequisites if p.strip()])

            elif isinstance(course.prerequisites, str) and course.prerequisites.strip() != "":
                # Single string prerequisite → keep it as is
                prerequisites = course.prerequisites.strip()

            else:
                # None, empty string, or invalid type
                prerequisites = ""

                #Convert program to clean comma-separated string
            if isinstance(course.program, list):
                # Convert list → comma string
                program = ",".join([p.strip() for p in course.program if p.strip()])

            elif isinstance(course.program, str) and course.program.strip() != "":
                # Single string program → keep it as is
                program = course.program.strip()

            else:
                # None, empty string, or invalid type
                program = ""
            if prerequisites:
                for i in prerequisites.split(","):
                    i = i.strip()
                    self.cursor.execute("""
                            SELECT credit_hours, lecture_hours, lab_hours,
                                prerequisites, maximum_capacity, program, level, course_name
                            FROM Courses
                            WHERE course_code = ?
                        """, (i,))

                    data = self.cursor.fetchone()

                    if not data:
                        print(f"invalid prerequisite {i} is not found.")
                        return     

            self.cursor.execute('''INSERT INTO Courses (course_code, course_name, credit_hours, lecture_hours, lab_hours, prerequisites, maximum_capacity, program, level)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                (course.course_code, course.name, course.credits, course.lecture_hours, course.lab_hours, prerequisites, course.max_capacity, program, course.level)) #insert course data into Courses table

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

            if not (student.program == 'Computer' or student.program == 'Power' or student.program == 'Biomedical' or student.program == 'Communication'):
                print("Invalid program, Please select a valid program")
                return

            ## added parameter called password 
            self.cursor.execute('''INSERT INTO Students (student_id, name, email,password, program, current_level)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                                (student.student_id, student.name, student.email,student.password, student.program, student.level)) #insert student data into Students table
            

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
    
    def add_admin(self, admin):   
        ### adds an admin object to data base   
        try:
            self.connect=sqlite3.connect(self.db_name) #connect to the database
            self.cursor=self.connect.cursor()     #create a cursor object

        
                
                
            self.connect.commit() #commit the changes 
            print(f"Admin {admin.name} with ID {admin.adminid} added to database.")
        except sqlite3.IntegrityError as e: #handle integrity errors (e.g., duplicate admin_id)
            print(f"An integrity error occurred while adding the admin: {e}")
        except sqlite3.Error as e:
            print(f"An error occurred while adding the admin: {e}")
        finally:
            self.connect.close()#close the connection
        
    
    def get_available_courses(self, student_id):
        """
        Returns courses available for a student based on:
        - Program matching (supports multi-program courses)
        - Passed prerequisites only
        - Do NOT show courses already passed
        - Show failed courses (retake allowed)
        - Show courses with no prerequisites
        """
        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            # 1) Get student program
            self.cursor.execute(
                "SELECT program FROM Students WHERE student_id=?",
                (student_id,)
            )
            row = self.cursor.fetchone()

            if not row:
                print(f"Student {student_id} not found.")
                self.connect.close()
                return []

            student_program = row[0].strip()

            # 2) Get courses that include the student's program
            self.cursor.execute(
                """
                SELECT course_code, course_name, credit_hours, lecture_hours, lab_hours,
                    prerequisites, maximum_capacity, program, level
                FROM Courses
                WHERE instr(program, ?) > 0
                """,
                (student_program,)
            )
            all_courses = self.cursor.fetchall()

            # 3) Get transcript (only lists)
            self.cursor.execute(
                "SELECT course_code, grade FROM transcripts WHERE student_id=?",
                (student_id,)
            )
            transcript_rows = self.cursor.fetchall()

            # Passed and failed as lists (no sets or dictionaries)
            passed = []
            failed = []

            for course_code, grade in transcript_rows:
                if grade.upper() == "F":
                    failed.append(course_code)
                else:
                    passed.append(course_code)

            available = []

            # 4) Evaluate each course
            for course in all_courses:
                course_code = course[0]
                prereq_str = course[5]

                # If student already passed → do NOT show
                if course_code in passed:
                    continue

                # If no prerequisites → show directly
                if not prereq_str:
                    available.append(course)
                    continue

                # Convert prerequisites string → list
                prereq_list = [p.strip() for p in prereq_str.split(",") if p.strip()]

                # Check if ALL prerequisites are passed
                all_completed = True
                for pr in prereq_list:
                    if pr not in passed:
                        all_completed = False
                        break

                if not all_completed:
                    continue

                # Passed all rules → show course
                available.append(course)

            return available

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
            student_transcript = [row for row in self.cursor.fetchall()]
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

                credit, lec, lab, prereq_str, max_cap, program_str, level, name = data

                # Convert prerequisites string to list
                prereq_list = [p.strip() for p in prereq_str.split(",") if p.strip()]

                # Convert programs string to list
                program_list = [r.strip() for r in program_str.split(",") if r.strip()]

                # Build a Course object
                course_obj = Course(
                    course_code,name,credit,lec,lab,prereq_list,max_cap,program_list,level)

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
                
                # Check program
                self.cursor.execute('''SELECT program FROM Students WHERE student_id=?''',(student_id,))
                student_program= self.cursor.fetchone()[0]
                The_same_program=[i for i in course_obj.program if i==student_program]
                if course_obj.program  :
                    if not The_same_program:
                        print(f"Course {course_code} is not in your program, The course's programs are {course_obj.program}")
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

    def get_course_enrollment_data(self):
        """
        Returns a list of courses with their maximum capacity and current enrollment.
        Format:
            [(course_code, max_capacity, current_enrollment), ...]
        """

        try:
            # Open database connection
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            # Fetch all course codes and their maximum capacities
            self.cursor.execute(
                "SELECT course_code, maximum_capacity FROM Courses"
            )
            courses = self.cursor.fetchall()

            results = []

            # For each course, count how many students are enrolled
            for course_code, max_capacity in courses:
                self.cursor.execute(
                    "SELECT COUNT(*) FROM Enrollments WHERE course_code=?",
                    (course_code,)
                )
                count = self.cursor.fetchone()[0]

                # Append (course_code, max_capacity, current_enrollment)
                results.append((course_code, max_capacity, count))

            return results

        except sqlite3.Error as e:
            print(f"An error occurred while retrieving enrollment data: {e}")
            return []

        finally:
            # Close the database connection
            self.connect.close()
           
    def view_transcript(self, student_id):
        try:
             # Open database connection
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()
            self.cursor.execute("""
                SELECT course_code, grade
                FROM Transcripts
                WHERE student_id = ?
            """, (student_id,))
            rows = self.cursor.fetchall()
            for i in range(len(rows)):
                    self.cursor.execute("""
                        SELECT credit_hours
                        FROM Courses
                        WHERE course_code = ?
                    """, (rows[i][0],))
                    credit_hours=self.cursor.fetchone()[0]
                    rows[i]=rows[i][0],rows[i][1],credit_hours    
            return rows
        except sqlite3.Error as e:
            print(f"An error occurred while viewing transcript: {e}")
        finally:
            self.connect.close()#close the connection
            
system = RegistrationSystem()