#CoursesClass.py
import sqlite3 #import sqlite3 module to interact with SQLite databases
# DataBase file name
db_name="RegistrationSystem.db" #Database file name

class Courses: #Courses class to represent a course in the system
    def __init__(self,db_name="RegistrationSystem.db"): #Constructor to initialize course attributes
        self.connect=sqlite3.connect(db_name) #Connect to the SQLite database
        self.cursor=self.connect.cursor() #Create a cursor object to execute SQL commands
        self.create_courses_table() #Create the Courses table if it doesn't exist

    def create_courses_table(self): #Method to create the Courses table
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
                );
                            ''')   #Create the Courses table if it doesn't already exist
            self.connect.commit() #Commit the changes to the database
        except sqlite3.Error as e:
            print(f"Error creating Courses table: {e}") #Print error message


    def close_connection(self): #Method to close the database connection
        self.cursor.close() #Close the cursor
        self.connect.close() #Close the database connection




    def add_course(self,course_code,course_name,credit_hours,lecture_hours,
                   lab_hours,prerequisites,maximum_capacity,program,level): #Method to add a course to the database
        try:
            if isinstance(prerequisites, list) : #Convert prerequisites list to comma-separated string
                prerequisites = ",".join(map(str,prerequisites))  #Join list elements with commas
           
            self.cursor.execute('''INSERT INTO Courses 
             VALUES(?,?,?,?,?,?,?,?,?)''', 
             (course_code,course_name,credit_hours,lecture_hours,
              lab_hours,prerequisites,maximum_capacity,program,level)) #Insert a new course record into the Courses table
           
            self.connect.commit() #Commit the changes to the database
          
            print(f"Course {course_code} added successfully.")
        
        except sqlite3.IntegrityError as e:   #Handle integrity errors (e.g., duplicate course code)
            print(f"Error adding course {course_code}: {e}")    #Print error message




    def add_multiple_courses(self,list_of_courses): #Method to add multiple courses to the database
                    try:
                        for course in list_of_courses: #Iterate through each course in the list
                            code, name, credits, lecture, lab, prereq, maxcap, program, level = course #Unpack course tuple
                            if isinstance(prereq, list): #Throw error if prerequisites is not a list
                                prereq = ",".join(map(str,prereq)) #Convert prerequisites list to comma-separated string
                        
                            self.cursor.execute('''INSERT INTO Courses
                            VALUES(?,?,?,?,?,?,?,?,?)''', (code, name, credits, lecture, lab, prereq, maxcap, program, level)) #Insert multiple course records into the Courses table
                    
                            self.connect.commit() #Commit the changes to the database
                        
                        print(f"{len(list_of_courses)} courses added successfully.")
                    except sqlite3.IntegrityError as e:
                        print(f"Error adding multiple courses: {e}")




    def get_show_all_courses(self): #Method to retrieve all courses from the database
        try:
            self.cursor.execute("SELECT * FROM Courses ") #Retrieve all records from the Courses table
            
            all_courses = self.cursor.fetchall() #Fetch all the retrieved records
            if not all_courses: #If no courses are found
                print("No courses found in the database.") #Print message
                return [] #Return empty list
            for course in all_courses:
                prerequisites_list = course[5].split(",") if course[5] else [] 
                course = course[:5] + (prerequisites_list,) + course[6:] #Convert prerequisites string to list
                print(course) #Print each course record
            
            return all_courses #Return the list of all courses
        except sqlite3.Error as e:
            print(f"Error retrieving courses: {e}") #Print error message
            return  #Return empty list on error



    def get_course_by_code(self,course_code): #Method to retrieve a course by its code
        try:
            self.cursor.execute("SELECT * FROM Courses WHERE course_code=?", (course_code,)) #Retrieve the course record with the specified course code
            
            
            course = self.cursor.fetchone() #Fetch the retrieved record
            
            if course: #If a course record is found
            
                prerequisites_list = course[5].split(",") if course[5] else [] #Convert prerequisites string to list
            
                return course[:5] + (prerequisites_list,) + course[6:] #Return the course record with prerequisites as a list
            return None #Return None if no course is found
        except sqlite3.Error as e:
            print(f"Error retrieving course {course_code}: {e}") #Print error message
            return None #Return None on error
    


    def delete_course(self,course_code): #Method to delete a course by its code
        try:
            if not self.get_course_by_code(course_code): #Check if the course exists
                print(f"Course {course_code} does not exist.") #Print message if course does not exist
                return #Exit the method if course does not exist
            self.cursor.execute("DELETE FROM Courses WHERE course_code=?", (course_code,)) #Delete the course record with the specified course code
        
            self.connect.commit() #Commit the changes to the database
        
            print(f"Course {course_code} deleted successfully.") #Print success message
        except sqlite3.Error as e:
            print(f"Error deleting course {course_code}: {e}") #Print error message




    def update_course_info(self,course_code,course_name=None,credit_hours=None,lecture_hours=None,
                   lab_hours=None,prerequisites=None,maximum_capacity=None,program=None,level=None): #Method to update a course's information
        try:
            if isinstance(prerequisites, list): #Convert prerequisites list to comma-separated string
              prerequisites = ",".join(map(str,prerequisites))  #Join list elements with commasq
            
            if not self.get_course_by_code(course_code): #Check if the course exists
                print(f"Course {course_code} does not exist.") #Print message if course does not exist
                return #Exit the method if course does not exist
            
            if not any([course_name,credit_hours,lecture_hours,
                            lab_hours,prerequisites,maximum_capacity,program,level]): #If no fields are provided to update
                print("No fields provided to update.") #Print message
                return #Exit the method if no fields are provided to update
            
            if course_name: #Update only the provided fields
                self.cursor.execute("UPDATE Courses SET course_name=? WHERE course_code=?", (course_name, course_code))
            if credit_hours:
                self.cursor.execute("UPDATE Courses SET credit_hours=? WHERE course_code=?", (credit_hours, course_code))
            if lecture_hours :
                self.cursor.execute("UPDATE Courses SET lecture_hours=? WHERE course_code=?", (lecture_hours, course_code)) 
            if lab_hours :
                self.cursor.execute("UPDATE Courses SET lab_hours=? WHERE course_code=?", (lab_hours, course_code))
            if prerequisites :
                self.cursor.execute("UPDATE Courses SET prerequisites=? WHERE course_code=?", (prerequisites, course_code))
            if maximum_capacity :
                self.cursor.execute("UPDATE Courses SET maximum_capacity=? WHERE course_code=?", (maximum_capacity, course_code))
            if program :
                self.cursor.execute("UPDATE Courses SET program=? WHERE course_code=?", (program, course_code))
            if level :
                self.cursor.execute("UPDATE Courses SET level=? WHERE course_code=?", (level, course_code))
            
            
       
            self.connect.commit() #Commit the changes to the database
            print(f"Course {course_code} updated successfully.") #Print success message
        
        except sqlite3.IntegrityError as e:   #Handle integrity errors (e.g., invalid data)
            print(f"Error updating course {course_code}: {e}")    #Print error message

    def drop_courses_table(self): #Method to drop the Courses table
        try:
            self.cursor.execute("DROP TABLE IF EXISTS Courses") #Drop the Courses table if it exists
            self.connect.commit() #Commit the changes to the database
            print("Courses table dropped successfully.") #Print success message
        except sqlite3.Error as e:
            print(f"Error dropping Courses table: {e}") #Print error message