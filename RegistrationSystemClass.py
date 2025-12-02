import sqlite3
from NewCourseClass import Course
from NewStudentsClass import Student
# from loginvalidation import Admin
from TimeBuilder import Schedule, ScheduleSystem
import bcrypt





class RegistrationSystem:
    """Main registration system for managing courses, students, admins, transcripts and enrollments."""

    def __init__(self, db_name="RegistrationSystem.db"):
        # Store database name
        self.db_name = db_name
        # Open initial connection to the database
        self.connect = sqlite3.connect(self.db_name)
        # Cursor used to execute SQL commands
        self.cursor = self.connect.cursor()
        # Create all required tables if they do not exist
        self.create_tables()

    def create_tables(self):
        """
        Create all database tables:
        - Courses
        - Students
        - Admin
        - transcripts
        - Enrollments
        """
        try:
            # Create Courses table (course catalog)
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
                );
            ''')

            # Create Students table (basic student information)
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Students (
                    student_id TEXT PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL CHECK (email LIKE '%_@__%.__%'),
                    password TEXT NOT NULL,
                    program TEXT NOT NULL CHECK (program IN ('Computer', 'Power', 'Biomedical', 'Communication')),
                    current_level INTEGER NOT NULL CHECK (current_level BETWEEN 1 AND 4)
                );
            ''')

            # Create Admin table (system administrators)
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Admin (
                    admin_id TEXT PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL CHECK (email LIKE '%_@__%.__%'),
                    password TEXT NOT NULL
                );
            ''')

            # Create transcripts table (grades history per course)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS transcripts (
                    student_id TEXT NOT NULL,
                    course_code TEXT NOT NULL,
                    grade TEXT NOT NULL CHECK (grade IN ('A', 'B', 'C', 'D', 'F', 'A+', 'B+', 'C+', 'D+')),
                    FOREIGN KEY(student_id) REFERENCES students(student_id),
                    FOREIGN KEY(course_code) REFERENCES courses(course_code)
                );
            """)

            # Create Enrollments table (current registered courses per student)
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Enrollments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    course_code TEXT NOT NULL,
                    section TEXT NOT NULL,
                    FOREIGN KEY(student_id) REFERENCES Students(student_id),
                    FOREIGN KEY(course_code) REFERENCES Courses(course_code)
                );
            ''')
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS CourseSchedule (
                    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_code TEXT NOT NULL,
                    section TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    days TEXT NOT NULL,
                    lecture_type TEXT NOT NULL,
                    instructor_name TEXT,
                    place TEXT,
                    room TEXT,
                    FOREIGN KEY(course_code) REFERENCES Courses(course_code)
                );
            """)


            # Save changes
            self.connect.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while creating the tables: {e}")

    def add_course(self, course):
        """
        Add a Course object into the Courses table.

        - Cleans prerequisites into a comma-separated string
        - Cleans program into a comma-separated string
        - Validates that each prerequisite exists in the Courses table
        """
        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            # Convert prerequisites to a clean comma-separated string
            if isinstance(course.prerequisites, list):
                # List of prerequisites -> "CIR101,CPE201"
                prerequisites = ",".join([p.strip() for p in course.prerequisites if p.strip()])
            elif isinstance(course.prerequisites, str) and course.prerequisites.strip() != "":
                # NEW: normalize any prerequisites string
                prerequisites = ",".join(
                    [p.strip() for p in course.prerequisites.split(",") if p.strip()]
                                        )
            else:
                # No prerequisites
                prerequisites = ""

            # Convert program to a clean comma-separated string
            if isinstance(course.program, list):
                # List of programs -> "Computer,Power"
                program = ",".join([p.strip() for p in course.program if p.strip()])
            elif isinstance(course.program, str) and course.program.strip() != "":
                # normalize any program string
                program = ",".join(
                    [p.strip() for p in course.program.split(",") if p.strip()]
                )
            else:
                # No program (should not usually happen)
                program = ""

            # Validate that each prerequisite course actually exists in the database
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

                    # If any prerequisite is missing, stop and show message
                    if not data:
                        print(f"invalid prerequisite {i} is not found.")
                        return

            # Insert course data into Courses table
            self.cursor.execute('''
                INSERT INTO Courses (course_code, course_name, credit_hours, lecture_hours, lab_hours,
                                     prerequisites, maximum_capacity, program, level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                course.course_code,
                course.name,
                course.credits,
                course.lecture_hours,
                course.lab_hours,
                prerequisites,
                course.max_capacity,
                program,
                course.level
            ))

            self.connect.commit()
            print(f"Course {course.name} with code {course.course_code} added to database.")
        except sqlite3.IntegrityError as e:
            # Handles duplicate course_code or other integrity constraints
            print(f"An integrity error occurred while adding the course: {e}")
        except sqlite3.Error as e:
            print(f"An error occurred while adding the course: {e}")
        finally:
            # Always close the connection at the end
            self.connect.close()

    def add_student(self, student):
        """
        Add a Student object to the Students table and insert its transcript.

        - Validates program name
        - Inserts basic student data
        - Inserts each (course_code, grade) from transcript list
        """
        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            # Validate that the program is valid
            if not (student.program == 'Computer' or
                    student.program == 'Power' or
                    student.program == 'Biomedical' or
                    student.program == 'Communication'):
                print("Invalid program, Please select a valid program")
                return 
            # Hash the password using bcrypt
            
            password_hash = bcrypt.hashpw(student.password.encode(), bcrypt.gensalt())

            # Insert student data
            self.cursor.execute('''
                INSERT INTO Students (student_id, name, email, password, program, current_level)
                VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                student.student_id,
                student.name,
                student.email,
                password_hash,
                student.program,
                student.level
            ))

            # Insert transcript rows (previous completed courses and grades)
            for course_code, grade in student.transcript:
                self.cursor.execute('''
                    INSERT INTO transcripts (student_id, course_code, grade)
                    VALUES (?, ?, ?)
                ''',
                (student.student_id, course_code, grade))

            self.connect.commit()
            print(f"Student {student.name} with ID {student.student_id} added to database.")
        except sqlite3.IntegrityError as e:
            # Duplicate student_id or invalid foreign key
            print(f"An integrity error occurred while adding the student: {e}")
        except sqlite3.Error as e:
            print(f"An error occurred while adding the student: {e}")
        finally:
            self.connect.close()

    def add_admin(self, admin):
        """
        Add an Admin object to the Admin table.
        """
        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            # Insert admin data
            self.cursor.execute('''
                INSERT INTO Admin (admin_id, name, email, password)
                VALUES (?, ?, ?, ?)
            ''',
            (admin.admin_id, admin.name, admin.email, admin.password))

            self.connect.commit()
            print(f"Admin {admin.name} with ID {admin.adminid} added to database.")
        except sqlite3.IntegrityError as e:
            print(f"An integrity error occurred while adding the admin: {e}")
        except sqlite3.Error as e:
            print(f"An error occurred while adding the admin: {e}")
        finally:
            self.connect.close()

    def get_available_courses(self, student_id):
        """
        Return all courses that are available for a specific student.

        A course is available if:
        - It matches the student's program (plan)
        - All prerequisites are completed with passing grades
        - The course is not already passed
        - Sections are returned with schedule and capacity info

        Structure returned:
        [
            (
                course_code,
                course_name,
                credit_hours,
                [
                    (
                        section,
                        days,
                        start_time,
                        end_time,
                        instructor_name,
                        place,
                        room,
                        enrolled_count,
                        capacity
                    ),
                    ...
                ]
            ),
            ...
        ]
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
                return []

            student_program = row[0]

            # 2) Get student transcript (for prerequisites + passed/failed)
            self.cursor.execute(
                "SELECT course_code, grade FROM transcripts WHERE student_id=?",
                (student_id,)
            )
            transcript_rows = self.cursor.fetchall()
            student_transcript = list(transcript_rows)

            passed = []
            failed = []

            for course_code, grade in transcript_rows:
                if grade.upper() == "F":
                    failed.append(course_code)
                else:
                    passed.append(course_code)

            # 3) Get all courses from Courses table
            self.cursor.execute(
                """
                SELECT course_code, course_name, credit_hours,
                       lecture_hours, lab_hours,
                       prerequisites, maximum_capacity,
                       program, level
                FROM Courses
                """
            )
            all_courses = self.cursor.fetchall()

            available_courses = []

            # 4) Filter courses based on program + prerequisites + passed
            for (
                course_code,
                course_name,
                credit_hours,
                lecture_hours,
                lab_hours,
                prereq_str,
                max_capacity,
                program_str,
                level
            ) in all_courses:

                # --- Check program match (course must include student's program) ---
                # program_str stored as comma-separated list, e.g. "Computer,Power"
                course_programs = [
                    p.strip() for p in program_str.split(",") if p.strip()
                ]
                if course_programs and student_program not in course_programs:
                    continue  # not from student's plan

                # --- Skip if course already passed ---
                if course_code in passed:
                    continue

                # --- Build prerequisite list ---
                prereq_list = [
                    p.strip() for p in prereq_str.split(",") if p.strip()
                ]

                # --- Use Course.check_prerequisites() to validate ---
                course_obj = Course(
                    course_code,
                    course_name,
                    credit_hours,
                    lecture_hours,
                    lab_hours,
                    prereq_list,
                    max_capacity,
                    course_programs,
                    level
                )

                if not course_obj.check_prerequisites(student_transcript):
                    # student does not meet prerequisites
                    continue

                # At this point: course is allowed for this student.
                # Next: gather section + schedule info from CourseSchedule.
                self.cursor.execute(
                    """
                    SELECT section, days, start_time, end_time,
                           instructor_name, place, room
                    FROM CourseSchedule
                    WHERE course_code=?
                    """,
                    (course_code,)
                )
                sections_info = self.cursor.fetchall()

                section_data = []

                for (
                    section,
                    days,
                    start_time,
                    end_time,
                    instructor_name,
                    place,
                    room
                ) in sections_info:

                    # Count how many students are enrolled in this section
                    self.cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM Enrollments
                        WHERE course_code=? AND section=?
                        """,
                        (course_code, section)
                    )
                    enrolled_count = self.cursor.fetchone()[0]

                    # Optional: skip full sections
                    if enrolled_count >= int(max_capacity):
                        continue

                    # Append full section info
                    section_data.append(
                        (
                            section,
                            days,
                            start_time,
                            end_time,
                            instructor_name,
                            place,
                            room,
                            enrolled_count,
                            max_capacity
                        )
                    )

                # If there are no available sections, skip the course
                if not section_data:
                    continue

                # Add course + its available sections
                available_courses.append(
                    (course_code, course_name, credit_hours, section_data)
                )

            return available_courses

        except sqlite3.Error as e:
            print(f"An error occurred while retrieving available courses: {e}")
            return []

        finally:
            self.connect.close()


    def validate_schedule(self, student_id, chosen_course_sections):
        """
        Validate a list of (course_code, section) before registration.

        chosen_course_sections example:
            [("CPE201", "A"), ("MATH101", "B")]

        Checks:
        - Convert (course + section) to schedule_id
        - Use ScheduleSystem.has_conflict() for time & credit hour checking
        - Prerequisites check
        - Capacity per section
        - Course must belong to student's program
        - Student cannot register same course twice (must delete first)
        """

        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()
            # -------------------------------
            # 0) Prevent selecting multiple sections for the same course
            # -------------------------------
            course_codes = [course_code for course_code, section in chosen_course_sections]
            for code in set(course_codes):
                if course_codes.count(code) > 1:
                    print(
                        f"You selected multiple sections for the same course {code}. "
                        "Please choose only one section per course."
                    )
                    return False

            # -------------------------------
            # 1) Convert (course_code, section) → schedule_id
            # -------------------------------
            schedule_ids = []
            for course_code, section in chosen_course_sections:
                self.cursor.execute(
                    """
                    SELECT schedule_id
                    FROM CourseSchedule
                    WHERE course_code = ? AND section = ?
                    LIMIT 1
                    """,
                    (course_code, section)
                )
                row = self.cursor.fetchone()
                if not row:
                    print(f"No schedule found for {course_code} section {section}.")
                    return False

                schedule_ids.append(row[0])

            # -------------------------------
            # 2) Time conflict + credit hour limit
            # -------------------------------
            schedule_system = ScheduleSystem(self.db_name)
            status = schedule_system.has_conflict(student_id, schedule_ids)

            if status != "OK":
                print(status)
                return False

            # -------------------------------
            # 3) Get student transcript for prereqs
            # -------------------------------
            self.cursor.execute(
                '''SELECT course_code, grade FROM transcripts WHERE student_id=?''',
                (student_id,)
            )
            student_transcript = self.cursor.fetchall()

            # -------------------------------
            # 4) Get student's program
            # -------------------------------
            self.cursor.execute(
                '''SELECT program FROM Students WHERE student_id=?''',
                (student_id,)
            )
            row = self.cursor.fetchone()
            if not row:
                print(f"Student {student_id} not found.")
                return False

            student_program = row[0]

            # -------------------------------
            # 5) Validation for each (course_code, section)
            # -------------------------------
            for course_code, section in chosen_course_sections:

                # --- Course info ---
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

                prereq_list = [p.strip() for p in prereq_str.split(",") if p.strip()]
                program_list = [p.strip() for p in program_str.split(",") if p.strip()]

                # --- Create course object to check prereqs ---
                course_obj = Course(
                    course_code, name, credit, lec, lab,
                    prereq_list, max_cap, program_list, level
                )

                # --- Prerequisites ---
                if not course_obj.check_prerequisites(student_transcript):
                    print(f"Student does NOT meet prerequisites for {course_code}.")
                    return False

                # --- Capacity (per section) ---
                self.cursor.execute(
                    '''
                    SELECT COUNT(*) 
                    FROM Enrollments 
                    WHERE course_code=? AND section=?
                    ''',
                    (course_code, section)
                )
                count_in_section = self.cursor.fetchone()[0]

                if count_in_section >= int(max_cap):
                    print(f"Section {section} of {course_code} is full.")
                    return False

                # --- Program match ---
                if program_list and student_program not in program_list:
                    print(f"Course {course_code} is not in your program.")
                    return False

                # --- Already enrolled in this course? ---
                self.cursor.execute(
                    """
                    SELECT 1 
                    FROM Enrollments 
                    WHERE student_id=? AND course_code=?
                    """,
                    (student_id, course_code)
                )
                if self.cursor.fetchone():
                    print(
                        f"You are already enrolled in {course_code}. "
                        f"Delete it first before choosing another section."
                    )
                    return False

            return True

        except sqlite3.Error as e:
            print(f"Error in validate_schedule: {e}")
            return False

        finally:
            self.connect.close()

    def register_student(self, student_id, chosen_course_sections):
        """
        Register a student in a list of (course_code, section).

        Example:
            chosen_course_sections = [
                ("CPE201", "A"),
                ("MATH101", "B")
            ]

        Steps:
        - Validate using validate_schedule()
        - Insert (student_id, course_code, section) into Enrollments
        """

        
        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            # --- Validate selections first ---
            if not self.validate_schedule(student_id, chosen_course_sections):
                print(f"Registration failed for student {student_id}.")
                return False

            # --- Insert each (course_code, section) pair ---
            for course_code, section in chosen_course_sections:
                self.cursor.execute(
                    '''
                    INSERT INTO Enrollments (student_id, course_code, section)
                    VALUES (?, ?, ?)
                    ''',
                    (student_id, course_code, section)
                )

            self.connect.commit()

            # --- Nicely formatted output ---
            formatted = ", ".join([f"{c}-{s}" for c, s in chosen_course_sections])
            print(f"Student {student_id} successfully registered for: {formatted}.")
            return True

        except sqlite3.Error as e:
            print(f"An error occurred while registering student: {e}")
            return False

        finally:
            self.connect.close()


    def delete_student(self, student_id):
        """
        Delete a student and all related records immediately.
        Removes:
        - Enrollments
        - Transcripts
        - Student information
        """

        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            # Delete student's enrollments
            self.cursor.execute(
                "DELETE FROM Enrollments WHERE student_id=?",
                (student_id,)
            )

            # Delete student's transcript records
            self.cursor.execute(
                "DELETE FROM transcripts WHERE student_id=?",
                (student_id,)
            )

            # Delete student from Students table
            self.cursor.execute(
                "DELETE FROM Students WHERE student_id=?",
                (student_id,)
            )

            self.connect.commit()

            return f"Student {student_id} has been deleted."

        except sqlite3.Error as e:
            return f"Error while deleting student: {e}"

        finally:
            self.connect.close()


    def drop_all_tables(self):
        """
        Drop all database tables used by the registration system.
        This resets the entire system.
        """

        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            # Drop in safe order (relations first)
            self.cursor.execute("DROP TABLE IF EXISTS Enrollments")
            self.cursor.execute("DROP TABLE IF EXISTS transcripts")
            self.cursor.execute("DROP TABLE IF EXISTS CourseSchedule")
            self.cursor.execute("DROP TABLE IF EXISTS Courses")
            self.cursor.execute("DROP TABLE IF EXISTS Students")
            self.cursor.execute("DROP TABLE IF EXISTS Admin")

            self.connect.commit()

            print("All tables dropped successfully.")

        except sqlite3.Error as e:
            print(f"Error while dropping tables: {e}")

        finally:
            self.connect.close()


    def get_course_enrollment_data(self):
        """
        Return enrollment info for each course WITHOUT using dictionaries.

        Structure returned:
        [
            (
                course_code,
                [
                    (section, enrolled_count, capacity_per_section),
                    (section, enrolled_count, capacity_per_section),
                    ...
                ],
                total_enrolled,
                total_capacity
            ),
            ...
        ]
        """

        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            # Get all courses
            self.cursor.execute(
                "SELECT course_code, maximum_capacity FROM Courses"
            )
            courses = self.cursor.fetchall()

            final_results = []

            for course_code, max_capacity in courses:

                # Get distinct sections for this course
                self.cursor.execute(
                    """
                    SELECT DISTINCT section
                    FROM Enrollments
                    WHERE course_code=?
                    """,
                    (course_code,)
                )
                section_rows = self.cursor.fetchall()
                section_list = [s[0] for s in section_rows]

                sections_data = []
                total_enrolled = 0

                # Count enrolled students for each section
                for section in section_list:
                    self.cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM Enrollments
                        WHERE course_code=? AND section=?
                        """,
                        (course_code, section)
                    )
                    enrolled = self.cursor.fetchone()[0]

                    total_enrolled += enrolled

                    # Append tuple (section, enrolled, capacity)
                    sections_data.append(
                        (section, enrolled, max_capacity)
                    )

                total_capacity = max_capacity * len(section_list)

                # Append final tuple for this course
                final_results.append(
                    (course_code, sections_data, total_enrolled, total_capacity)
                )

            return final_results

        except sqlite3.Error as e:
            print(f"Error retrieving enrollment data: {e}")
            return []

        finally:
            self.connect.close()


    def view_transcript(self, student_id):
        """
        Return a list of rows for the student's transcript in the form:
        (course_code, grade, credit_hours)
        """
        try:
            self.connect = sqlite3.connect(self.db_name)
            self.cursor = self.connect.cursor()

            # Get list of (course_code, grade) for the student
            self.cursor.execute("""
                SELECT course_code, grade
                FROM Transcripts
                WHERE student_id = ?
            """, (student_id,))
            rows = self.cursor.fetchall()

            # For each course, fetch its credit_hours and attach to result
            for i in range(len(rows)):
                self.cursor.execute("""
                    SELECT credit_hours
                    FROM Courses
                    WHERE course_code = ?
                """, (rows[i][0],))
                credit_hours = self.cursor.fetchone()[0]
                rows[i] = (rows[i][0], rows[i][1], credit_hours)

            return rows
        except sqlite3.Error as e:
            print(f"An error occurred while viewing transcript: {e}")
        finally:
            self.connect.close()

    def get_student_info(self, student_id):
        """
        Placeholder for future implementation:
        Should return basic student info + maybe transcript / enrollments.
        """
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM Students WHERE student_id=?",
            (student_id,)
        )
        return cur.fetchone()


# Create a system instance when the module is imported
system = RegistrationSystem()
