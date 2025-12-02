import sqlite3

# ============================================================
# Schedule Class
# ------------------------------------------------------------
# This class represents the blueprint for creating multiple
# sections of the same course. The system automatically converts
# num_sections into alphabetical labels:
#
#   Example:
#       num_sections = 4  →  ["A", "B", "C", "D"]
#
# Days:
#   - MUST be provided by the user.
#   - Must be chosen from the allowed list:
#         ["Sun", "Mon", "Tue", "Wed", "Thu"]
#   - Must be given as a Python list:
#         ["Sun", "Tue"]
#
# Times:
#   - Must be in strict "HH:MM" format.
#
# Lecture Type:
#   - Allowed:
#         ["Lecture", "Lab", "Online"]
#   - Default = "Lecture"
#
# Instructor:
#   - Can be:
#         a single instructor name → applied to ALL sections
#         OR a list of names → one per section
#
# Room:
#   - Same logic as instructor (single value OR list)
#
# Purpose:
#   - This class ONLY holds raw schedule data.
#   - Validation and database writing is performed by ScheduleSystem.
# ============================================================

class Schedule:

    # Allowed choices for validation
    ALLOWED_DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu"]
    ALLOWED_TYPES = ["Lecture", "Lab", "Online"]

    def __init__(
        self,
        course_code,              # course identifier (e.g., "CPE201")
        num_sections,             # number of sections → labels A,B,C...
        start_time,               # "HH:MM"
        end_time,                 # "HH:MM"
        days,                     # required list of meeting days
        lecture_type="Lecture",   # Lecture / Lab / Online
        instructor_name=None,     # string or list for each section
        place=None,               # building/location
        room=None                 # string or list per section
    ):
        self.course_code = course_code
        self.num_sections = num_sections

        self.start_time = start_time      # shared start time
        self.end_time = end_time          # shared end time
        self.days = days                  # required list of days
        self.lecture_type = lecture_type  # type of session

        self.instructor_name = instructor_name  # shared or per-section
        self.place = place                      # shared building
        self.room = room                        # shared or per-section



# ============================================================
# ScheduleSystem Class
# ------------------------------------------------------------
# Responsible for:
#   - Validating schedule data:
#         ✔ Allowed days
#         ✔ Allowed lecture types
#         ✔ Time format "HH:MM"
#         ✔ Instructor must exist in Admin table
#
#   - Generating alphabetical section labels (A,B,C,…)
#
#   - Inserting multiple sections for a course into
#     CourseSchedule table (one row per section)
#
# Validation:
#   - All validation errors raise ValueError
#   - This prevents invalid data from entering the database
#
# Section Insertion:
#   - instructor_name and room support two modes:
#         1) Single string → applied to all sections
#         2) List → one value per section
# ============================================================

class ScheduleSystem:

    def __init__(self, db_name="RegistrationSystem.db"):
        self.db_name = db_name

    # ------------------------------------------------------------
    # Convert number of sections to alphabetical labels
    # ------------------------------------------------------------
    def generate_section_labels(self, count):
        try:
            return [chr(65 + i) for i in range(count)]  # 65 = ASCII 'A'
        except ValueError as e:
            print(e)
            raise ValueError(e)

    # ------------------------------------------------------------
    # Validate HH:MM format
    # ------------------------------------------------------------
    def validate_time(self, time_str):
        try:
            # Must be exactly 5 characters: "HH:MM"
            if len(time_str) != 5 or time_str[2] != ":":
                raise ValueError(f"Invalid time format '{time_str}'. Must be 'HH:MM'.")

            hh, mm = time_str.split(":")

            # Hours and minutes must be digits
            if not (hh.isdigit() and mm.isdigit()):
                raise ValueError(
                    f"Invalid time '{time_str}'. Hours and minutes must be numbers."
                )

            hours = int(hh)
            minutes = int(mm)

            # Hours: 0–23, Minutes: 0–59
            if not (0 <= hours <= 23):
                raise ValueError(
                    f"Invalid hour value '{hours}' in time '{time_str}'. "
                    "Hour must be between 0 and 23."
                )

            if not (0 <= minutes <= 59):
                raise ValueError(
                    f"Invalid minute value '{minutes}' in time '{time_str}'. "
                    "Minutes must be between 0 and 59."
                )
        except ValueError as e:
            print(e)
            raise ValueError(e)






    # ------------------------------------------------------------
    # Validate allowed days
    # ------------------------------------------------------------
    def validate_days(self, days):
        try:
            for d in days:
                if d not in Schedule.ALLOWED_DAYS:
                    raise ValueError(
                        f"Invalid day '{d}'. Allowed days: {Schedule.ALLOWED_DAYS}"
                    )
        except ValueError as e:
            print(e)
            raise ValueError(e)




    # ------------------------------------------------------------
    # Validate allowed lecture types
    # ------------------------------------------------------------
    def validate_lecture_type(self, lecture_type):
        try:
            if lecture_type not in Schedule.ALLOWED_TYPES:
                raise ValueError(
                    f"Invalid lecture type '{lecture_type}'. "
                    f"Allowed types: {Schedule.ALLOWED_TYPES}"
                )
        except ValueError as e:
            print(e)
            raise ValueError(e)


    # ------------------------------------------------------------
    # Validate instructor exists in Admin table
    # ------------------------------------------------------------
    def validate_instructor(self, instructor_name, num_sections):
        try:
            conn = sqlite3.connect(self.db_name)
            cur = conn.cursor()

            # Case 1: No instructor assigned → allowed
            if instructor_name is None:
                return

            # Case 2: Instructor list must match num_sections exactly
            if isinstance(instructor_name, list):
                if len(instructor_name) != num_sections:
                    raise ValueError(
                        f"Instructor list length must equal num_sections ({num_sections})."
                    )
                instructors_to_check = instructor_name
            else:
                # Single instructor must match: one instructor for ALL sections
                instructors_to_check = [instructor_name]

            # Validate each instructor name in the list
            for inst in instructors_to_check:

                cur.execute(
                    "SELECT admin_id FROM Admin WHERE name=?",
                    (inst,)
                )
                row = cur.fetchone()

                if row is None:
                    raise ValueError(
                        f"Instructor '{inst}' does not exist in Admin table. "
                        "Add the instructor before assigning."
                    )

        except sqlite3.Error as e:
            print("Database Error:", e)

        finally:
            conn.close()






    # ------------------------------------------------------------
    # Insert ALL sections (A,B,C,...) with full validation
    # ------------------------------------------------------------
    def add_schedule(self, schedule):

        try:
            conn = sqlite3.connect(self.db_name)
            cur = conn.cursor()

            # ---- COURSE EXISTENCE CHECK ----
            cur.execute(
                "SELECT course_code FROM Courses WHERE course_code=?",
                (schedule.course_code,)
            )
            course_exists = cur.fetchone()

            if not course_exists:
                raise ValueError(
                    f"Cannot add schedule: course '{schedule.course_code}' does not exist "
                    "in Courses table. Add the course first."
                )

                # ---- VALIDATION ----
            self.validate_days(schedule.days)
            self.validate_lecture_type(schedule.lecture_type)
            self.validate_time(schedule.start_time)
            self.validate_time(schedule.end_time)

            # Validate instructor(s)
            
            self.validate_instructor(schedule.instructor_name, schedule.num_sections)



            # ---- END VALIDATION ----

            days_str = ",".join(schedule.days)
            labels = self.generate_section_labels(schedule.num_sections)

            instructor_list = (
                schedule.instructor_name if isinstance(schedule.instructor_name, list) else None
            )
            room_list = (
                schedule.room if isinstance(schedule.room, list) else None
            )
            # ------------------------------------------------------------
            # PRE-CHECK: prevent conflicts within the same package (section)
            # ------------------------------------------------------------

            # Get existing shapes (Lecture/Lab/Online) for same course & section
            cur.execute(
                """
                SELECT start_time, end_time, days, lecture_type
                FROM CourseSchedule
                WHERE course_code=? AND num_sections=?
                """,
                (schedule.course_code, schedule.num_sections)
            )
            existing_shapes = cur.fetchall()

            # Convert new schedule times
            def to_mins(t): 
                h, m = map(int, t.split(":"))
                return h*60 + m

            new_start_m = to_mins(schedule.start_time)
            new_end_m   = to_mins(schedule.end_time)
            new_days    = set(schedule.days)

            # Compare against all existing shapes in same section
            for e_start, e_end, e_days_raw, e_type in existing_shapes:
                e_start_m = to_mins(e_start)
                e_end_m   = to_mins(e_end)
                e_days    = set(e_days_raw.split(","))

                overlap = new_days & e_days

                if overlap:
                    if new_start_m < e_end_m and new_end_m > e_start_m:
                        days_text = ", ".join(overlap)
                        raise ValueError(
                            f"CONFLICT WITHIN PACKAGE (section {schedule.num_sections}): "
                            f"{schedule.course_code} {schedule.lecture_type} conflicts with existing {e_type}\n"
                            f"Days: {days_text}\n"
                            f"New: {schedule.start_time}–{schedule.end_time}\n"
                            f"Existing: {e_start}–{e_end}"
                        )

            # Insert each section individually
            for index, label in enumerate(labels):

                # Instructor for this section
                instr_name = (
                    instructor_list[index] if instructor_list and index < len(instructor_list)
                    else schedule.instructor_name
                )

                # Room for this section
                room_value = (
                    room_list[index] if room_list and index < len(room_list)
                    else schedule.room
                )

                # Resolve instructor_id (safe because validated earlier)
                instructor_id = None
                if instr_name:
                    conn2 = sqlite3.connect(self.db_name)
                    cur2 = conn2.cursor()

                    cur2.execute("SELECT admin_id FROM Admin WHERE name=?", (instr_name,))
                    row = cur2.fetchone()
                    conn2.close()

                    instructor_id = row[0]

                # Insert final section row
                cur.execute(
                    """
                    INSERT INTO CourseSchedule
                        (course_code, section, start_time, end_time,
                         lecture_type, instructor_name, instructor_id,
                         days, place, room)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        schedule.course_code,
                        label,                       # A/B/C/D...
                        schedule.start_time,
                        schedule.end_time,
                        schedule.lecture_type,
                        instr_name,
                        instructor_id,
                        days_str,
                        schedule.place,
                        room_value
                    )
                )

            conn.commit()

        except sqlite3.Error as e:
            print("Database Error:", e)

        finally:
            conn.close()



    # ------------------------------------------------------------
    # Fetch ALL sections for a specific course
    # ------------------------------------------------------------
    def get_course_sections(self, course_code):
        try:
            conn = sqlite3.connect(self.db_name)
            cur = conn.cursor()

            cur.execute(
                "SELECT * FROM CourseSchedule WHERE course_code=?",
                (course_code,)
            )
            return cur.fetchall()

        except sqlite3.Error as e:
            print("Error fetching course sections:", e)
            return []

        finally:
            conn.close()



    # ------------------------------------------------------------
    # Fetch ONE schedule by its ID
    # ------------------------------------------------------------
    def get_schedule_by_id(self, schedule_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cur = conn.cursor()

            cur.execute(
                "SELECT * FROM CourseSchedule WHERE schedule_id=?",
                (schedule_id,)
            )
            return cur.fetchone()

        except sqlite3.Error as e:
            print("Error fetching schedule:", e)
            return None

        finally:
            conn.close()



# ============================================================
    # has_conflict
    # ------------------------------------------------------------
    # Checks if a student can register one schedule or multiple
    # schedules without:
    #     1) Time conflicts with existing or new schedules
    #     2) Exceeding the 18-credit-hour limit
    #
    # Input:
    #   student_id    → ID of the student
    #   schedule_package_ids  → int (single schedule) OR list of schedules
    #
    # Logic:
    #   - Converts single ID into a list for unified processing
    #   - First checks total credit hours (existing + new)
    #       → returns "CREDIT_LIMIT_EXCEEDED" if > 18
    #   - Checks new schedules against existing schedules
    #   - Checks new schedules against EACH OTHER
    #       → returns detailed "TIME_CONFLICT" if conflict found
    #
    # Output:
    #       "OK"                     → registration allowed
    #       "TIME_CONFLICT"          → overlapping schedule with details
    #       "CREDIT_LIMIT_EXCEEDED"  → credit hours > 18
    #       "INVALID_SCHEDULE_ID"    → invalid schedule passed
    #
    # Note:
    #   This method only validates. It does NOT register the student.
    # ============================================================

    def has_conflict(self, student_id, schedule_ids):

        try:
            # ===============================================
            # Open connection (single DB connection only)
            # ===============================================
            conn = sqlite3.connect(self.db_name)
            cur = conn.cursor()

            # Normalize to list
            if isinstance(schedule_ids, int):
                schedule_ids = [schedule_ids]

            # ===============================================
            # CREDIT LIMIT CHECK
            # ===============================================
            if self.exceeds_credit_limit(student_id, schedule_ids):
                return "CREDIT_LIMIT_EXCEEDED"

            # Helper
            def to_minutes(t):
                h, m = map(int, t.split(":"))
                return h * 60 + m

            # ===============================================
            # Fetch EXISTING schedules for the student
            # ===============================================
            cur.execute(
                "SELECT course_code, section FROM Enrollments WHERE student_id=?",
                (student_id,)
            )
            existing_enrollments = cur.fetchall()

            existing = []
            for (old_course, old_section) in existing_enrollments:
                cur.execute(
                    """
                    SELECT course_code, start_time, end_time, days, lecture_type
                    FROM CourseSchedule
                    WHERE course_code=? AND section=?

                    """,
                    (old_course, old_section)
                )
                row = cur.fetchone()
                if row:
                    existing.append(row)

            # ===============================================
            # Process EACH requested schedule_id as a PACKAGE
            # ===============================================
            # A package means: Lecture + Lab + Tutorial belonging to SAME course + SAME section
            # ===============================================

            packages = {}  # schedule_id -> list of shapes

            for new_id in schedule_ids:

                # Get its course + section
                cur.execute(
                    "SELECT course_code, section FROM CourseSchedule WHERE schedule_id=?",
                    (new_id,)
                )
                base = cur.fetchone()
                if not base:
                    return "INVALID_SCHEDULE_ID"

                course_code, section = base

                # Fetch ALL shapes belonging to this package
                cur.execute(
                    """
                    SELECT course_code, start_time, end_time, days, lecture_type
                    FROM CourseSchedule
                    WHERE course_code=? AND section=?
                    """,
                    (course_code, section)
                )
                shapes = cur.fetchall()

                # Store as cleaned list for later
                # Each shape → (course, start, end, days, type)
                shapes = [(s[0], s[1], s[2], s[3], s[4]) for s in shapes]
                packages[new_id] = shapes

                # ===============================================
                # INTERNAL PACKAGE CONFLICT CHECK
                # (Lecture vs Lab inside same section)
                # ===============================================
                for i in range(len(shapes)):
                    for j in range(i+1, len(shapes)):
                        c1, s1, e1, d1, t1 = shapes[i]
                        c2, s2, e2, d2, t2 = shapes[j]

                        days1 = set(d1.split(","))
                        days2 = set(d2.split(","))
                        overlap = days1 & days2
                        if overlap:
                            if to_minutes(s1) < to_minutes(e2) and to_minutes(e1) > to_minutes(s2):
                                return (
                                    "TIME_CONFLICT_WITHIN_PACKAGE: "
                                    f"{c1} {t1} conflicts with {c2} {t2}"
                                    f"Days: {', '.join(overlap)}"
                                    f"{t1}: {s1}-{e1}"
                                    f"{t2}: {s2}-{e2}"
                                )

            # ===============================================
            # CHECK PACKAGE vs EXISTING STUDENT SCHEDULES
            # ===============================================
            for new_id, pkg in packages.items():
                for (new_course, new_start, new_end, new_days_raw, new_type) in pkg:

                    new_days_raw_set = set(new_days_raw.split(","))
                    new_start_m = to_minutes(new_start)
                    new_end_m   = to_minutes(new_end)


                    for (old_course, old_start, old_end, old_days_raw, old_type) in existing:
                        if new_course == old_course:
                            continue

                        old_days_raw_set = set(old_days_raw.split(","))
                        overlap = new_days_raw_set & old_days_raw_set
                        if overlap:
                            if new_start_m < to_minutes(old_end) and new_end_m > to_minutes(old_start):
                                return (
                                    "TIME_CONFLICT: "
                                    f"{new_course} ({new_type}) conflicts with existing {old_course}"
                                    f"Days: {', '.join(overlap)}"
                                    f"New: {new_start}-{new_end}"
                                    f"Existing: {old_start}-{old_end}"
                                )

            # ===============================================
            # CHECK PACKAGE vs PACKAGE (new vs new)
            # ===============================================
            ids = list(packages.keys())
            for i in range(len(ids)):
                for j in range(i+1, len(ids)):

                    shapesA = packages[ids[i]]
                    shapesB = packages[ids[j]]


                    for (courseA, startA, endA, daysA_raw, typeA) in shapesA:
                        for (courseB, startB, endB, daysB_raw, typeB) in shapesB:

                            if courseA == courseB:
                                continue

                            daysA_raw_set = set(daysA_raw.split(","))
                            daysB_raw_set = set(daysB_raw.split(","))
                            overlap = daysA_raw_set & daysB_raw_set

                            if overlap:
                                if to_minutes(startA) < to_minutes(endB) and to_minutes(endA) > to_minutes(startB):
                                    return (
                                        "TIME_CONFLICT: "
                                        f"{courseA} ({typeA}) conflicts with {courseB} ({typeB})"
                                        f"Days: {', '.join(overlap)}"
                                        f"{courseA}: {startA}-{endA}"
                                        f"{courseB}: {startB}-{endB}"
                                    )

            return "OK"

        except sqlite3.Error:
            return "TIME_CONFLICT"

        finally:
            conn.close()







    # ------------------------------------------------------------
    # NEW: get total hours student is enrolled in
    # ------------------------------------------------------------
    def get_total_enrolled_hours(self, student_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cur = conn.cursor()

            cur.execute(
                """
                SELECT C.credit_hours
                FROM Enrollments E
                JOIN Courses C ON E.course_code = C.course_code
                WHERE E.student_id=?
                """,
                (student_id,)
            )
            rows = cur.fetchall()

            return sum(r[0] for r in rows)

        except:
            return 0

        finally:
            conn.close()



    # ------------------------------------------------------------
    # NEW: check if adding new schedules exceeds 18 hours
    # ------------------------------------------------------------
    def exceeds_credit_limit(self, student_id, schedule_ids):
        try:
            conn = sqlite3.connect(self.db_name)
            cur = conn.cursor()

            # total already enrolled
            cur.execute(
                """
                SELECT C.credit_hours
                FROM Enrollments E
                JOIN Courses C ON E.course_code = C.course_code
                WHERE E.student_id=?
                """,
                (student_id,)
            )
            existing = sum(r[0] for r in cur.fetchall())

            # hours of new schedules
            added_hours = 0
            for sid in schedule_ids:
                cur.execute(
                    """
                    SELECT C.credit_hours
                    FROM CourseSchedule S
                    JOIN Courses C ON S.course_code = C.course_code
                    WHERE S.schedule_id=?
                    """,
                    (sid,)
                )
                row = cur.fetchone()
                if row:
                    added_hours += row[0]

            return (existing + added_hours) > 18

        except:
            return True  # safer = block

        finally:
            conn.close()

