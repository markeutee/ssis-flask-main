#Models/Student.py
from ..extension import mysql
import MySQLdb.cursors

class Student():
    def __init__(self, id=None, firstname=None, lastname=None, course_code=None, year=None, gender=None, college=None, picture=None):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.course_code = course_code
        self.year = year
        self.gender = gender
        self.college = college
        self.connection = mysql.connection
        self.picture = picture

    def add(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO student (id, firstname, lastname, course_code, year, gender, picture)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (self.id, self.firstname, self.lastname, self.course_code, self.year, self.gender, self.picture))
        self.connection.commit()
        cursor.close()
    
    def update(self, id):
        cursor = self.connection.cursor()

        if self.picture:
            # Update including picture
            cursor.execute("""
                UPDATE student
                SET id=%s, firstname=%s, lastname=%s, course_code=%s, year=%s, gender=%s, picture=%s
                WHERE id=%s
            """, (self.id, self.firstname, self.lastname, self.course_code, self.year, self.gender, self.picture, id))
        else:
            # Update without changing picture
            cursor.execute("""
                UPDATE student
                SET id=%s, firstname=%s, lastname=%s, course_code=%s, year=%s, gender=%s
                WHERE id=%s
            """, (self.id, self.firstname, self.lastname, self.course_code, self.year, self.gender, id))

        self.connection.commit()
        cursor.close()


    def delete(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM student WHERE id=%s", (self.id,))
        self.connection.commit()
        cursor.close()

    @classmethod
    def search(cls, input, filter, page=1, per_page=10):
        cursor = mysql.connection.cursor()
        students = []
        offset = (page - 1) * per_page

        base_query = """
            SELECT student.id, student.firstname, student.lastname, student.course_code, student.year, student.gender,
                   course.college_code, student.picture
            FROM student
            LEFT JOIN course ON student.course_code = course.code
            LEFT JOIN college ON course.college_code = college.code
        """

        if filter == "0":
            query = base_query + """
                WHERE student.id LIKE %s OR student.firstname LIKE %s OR student.lastname LIKE %s
                OR student.course_code LIKE %s OR student.year LIKE %s OR student.gender LIKE %s
            """
            params = tuple([f"%{input}%"] * 6)
        elif filter == "1":
            query = base_query + " WHERE student.id LIKE %s"
            params = (f"%{input}%",)
        elif filter == "2":
            query = base_query + " WHERE student.firstname LIKE %s"
            params = (f"%{input}%",)
        elif filter == "3":
            query = base_query + " WHERE student.lastname LIKE %s"
            params = (f"%{input}%",)
        elif filter == "4":
            query = base_query + " WHERE student.course_code LIKE %s"
            params = (f"%{input}%",)
        elif filter == "5":
            query = base_query + " WHERE student.year LIKE %s"
            params = (f"%{input}%",)
        elif filter == "6":
            query = base_query + " WHERE student.gender = %s"
            params = (f"{input}",)
        elif filter == "7":
            query = base_query + """
                WHERE college.name LIKE %s OR college.code LIKE %s
            """
            params = (f"%{input}%", f"%{input}%")
        else:
            query = base_query
            params = ()

        query += " ORDER BY student.id LIMIT %s OFFSET %s"
        cursor.execute(query, params + (per_page, offset))

        for student_data in cursor.fetchall():
            students.append(Student(
                id=student_data[0],
                firstname=student_data[1],
                lastname=student_data[2],
                course_code=student_data[3],
                year=student_data[4],
                gender=student_data[5],
                college=student_data[6],
                picture=student_data[7]
            ))
        cursor.close()
        return students

    

    @classmethod
    def check_existing_id(cls, id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM student WHERE id = %s", (id,))
        student_data = cursor.fetchone()
        cursor.close()
        return student_data is not None

    
    
    @classmethod
    def get_all(cls,table_name = 'student'):
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT student.id, student.firstname, student.lastname, student.course_code, student.year, student.gender, course.college_code , student.picture FROM student LEFT JOIN course ON student.course_code = course.code LEFT JOIN college ON course.college_code = college.code ORDER BY student.id")
        student = []
        for student_data in cursor.fetchall():
            courses = Student(id = student_data[0] , firstname = student_data[1], lastname=student_data[2], course_code=student_data[3], year=student_data[4], gender=student_data[5], college=student_data[6], picture = student_data[7])
            student.append(courses)
        cursor.close()
        return student
    
    @classmethod
    def check_existing_id(cls,id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM student WHERE id = %s", (id,))
        student_data = cursor.fetchone()
        cursor.close()
        return student_data is not None
    
    @classmethod
    def get_one(clr, id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM student WHERE id = %s", (id,))
        student_data = cursor.fetchone()
        cursor.close

        if student_data:
            return Student(id = student_data[0] , firstname = student_data[1], lastname=student_data[2], course_code=student_data[3], year=student_data[4], gender=student_data[5])
            return None

    @classmethod
    def get_paginated(cls, limit=50, offset=0):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT student.id, student.firstname, student.lastname, student.course_code, 
                   student.year, student.gender, course.college_code, student.picture
            FROM student
            LEFT JOIN course ON student.course_code = course.code
            LEFT JOIN college ON course.college_code = college.code
            ORDER BY student.id
            LIMIT %s OFFSET %s
        """, (limit, offset))
        
        students = []
        for student_data in cursor.fetchall():
            student = Student(
                id=student_data[0],
                firstname=student_data[1],
                lastname=student_data[2],
                course_code=student_data[3],
                year=student_data[4],
                gender=student_data[5],
                college=student_data[6],
                picture=student_data[7]
            )
            students.append(student)
        cursor.close()
        return students

    @classmethod
    def get_total_count(cls):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM student")
        count = cursor.fetchone()[0]
        cursor.close()
        return count