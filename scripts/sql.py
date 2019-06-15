department_insert_query = ("INSERT INTO school_departments (school_id,code)"
            "VALUES (1,%s)")
professor_insert_query = ("INSERT INTO professors (school_id,last_name)"
             "VALUES (1,%s)")
course_insert_query = ("INSERT INTO courses (professor_id, school_semester_id, code)"
            "VALUES (%s, %s, %s)")
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
update_course_query = (
"UPDATE courses SET school_department_id = %s WHERE course_id = %s"
)
update_books_from_api_query = (
"UPDATE books SET isbn10 = %s, title = %s, author = %s WHERE book_id = %s"
)

select_dept_query = (
"SELECT COUNT(code) FROM school_departments WHERE code = %s"
)
select_prof_query = (
"SELECT COUNT(last_name) FROM professors WHERE last_name = %s"
)

select_prof_query2 = (
"SELECT professor_id FROM professors WHERE last_name = %s"
)
