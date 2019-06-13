department_insert_query = ("INSERT INTO school_departments (school_id,code)"
            "VALUES (1,%s)")
professor_insert_query = ("INSERT INTO professors (school_id,last_name)"
             "VALUES (1,%s)")
course_insert_query = ("INSERT INTO courses (professor_id, school_semester_id, code)"
            "VALUES (%s, %s, %s)")
course_dept_insert_query = (
"INSERT INTO course_departments (course_id, school_department_id)"
"VALUES (%s, %s)")
course_book_insert_query = (
"INSERT INTO course_books (book_id, course_id)"
"VALUES (%s, %s)")
book_simple_insert_query = (
"INSERT INTO books (isbn13)"
"VALUES (%s)"
)
book_insert_query = (
"INSERT INTO books (isbn13, title, edition)"
"VALUES (%s,%s,%s)"
)
