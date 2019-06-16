department_insert_query = (
    "INSERT INTO school_departments (school_id,code)"
    "VALUES (1,%s)"
)
professor_insert_query = (
    "INSERT INTO professors (school_id,last_name)"
    "VALUES (1,%s)"
 )
course_insert_query = (
    "INSERT INTO courses (professor_id, school_semester_id, code, school_department_id)"
    "VALUES (%s, %s, %s, %s)"
)
course_book_insert_query = (
    "INSERT INTO course_books (book_id, course_id)"
    "VALUES (%s, %s)"
)
book_simple_insert_query = (
    "INSERT INTO books (isbn13)"
    "VALUES (%s)"
)
book_insert_query = (
    "INSERT INTO books (isbn13, title, edition)"
    "VALUES (%s,%s,%s)"
)
huntley_insert_query = (
    "INSERT INTO book_huntley_prices (book_id, new_shelf_price)"
    "VALUES (%s, %s)"
)
books_insert_query = (
    "INSERT INTO books (isbn13, isbn10, title, author, edition)"
    "VALUES (%s, %s, %s, %s, %s)"
)
update_course_query = (
    "UPDATE courses SET school_department_id = %s WHERE course_id = %s"
)
update_books_query = (
    "UPDATE books SET isbn10 = %s, title = %s, author = %s WHERE book_id = %s"
)
count_dept_query = (
    "SELECT COUNT(code) FROM school_departments WHERE code = %s"
)
count_prof_query = (
    "SELECT COUNT(last_name) FROM professors WHERE last_name = %s"
)
count_book_query = (
    "SELECT COUNT(isbn13) FROM books WHERE isbn13 = %s"
)
count_course_query = (
    "SELECT COUNT(course_id) FROM course_books WHERE book_id = %s AND course_id = %s"
)
select_prof_query = (
    "SELECT professor_id FROM professors WHERE last_name = %s"
)
select_dept_query = (
    "SELECT school_department_id FROM school_departments WHERE code = %s"
)
select_course_query = (
    "SELECT course_id FROM courses WHERE professor_id = %s AND school_semester_id = %s AND school_department_id = %s"
)
select_book_query = (
    "SELECT book_id FROM books WHERE isbn13 = %s LIMIT 1"
)
