department_insert_query = (
    "INSERT INTO school_departments (school_id,code,created_at)"
    "VALUES (1,%s,%s)"
)
professor_insert_query = (
    "INSERT INTO professors (school_id,last_name,created_at)"
    "VALUES (1,%s,%s)"
 )
course_insert_query = (
    "INSERT INTO courses (professor_id, school_semester_id, code, school_department_id,created_at)"
    "VALUES (%s, %s, %s, %s,%s)"
)
course_book_insert_query = (
    "INSERT INTO course_books (book_id, course_id,created_at)"
    "VALUES (%s, %s,%s)"
)
book_simple_insert_query = (
    "INSERT INTO books (isbn13)"
    "VALUES (%s)"
)
book_insert_query = (
    "INSERT INTO books (isbn13, title, authors, edition, created_at)"
    "VALUES (%s,%s,%s,%s,%s)"
)
huntley_insert_query = (
    "INSERT INTO book_huntley_prices (book_id, new_shelf_price)"
    "VALUES (%s, %s)"
)
books_full_insert_query = (
    "INSERT INTO books (isbn13, isbn10, title, authors, edition)"
    "VALUES (%s, %s, %s, %s, %s)"
)
update_course_query = (
    "UPDATE courses SET school_department_id = %s WHERE course_id = %s"
)
update_books_query = (
    "UPDATE books SET isbn10 = %s, title = %s, authors = %s WHERE book_id = %s"
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
    "SELECT COUNT(course_id) FROM courses WHERE professor_id = %s AND code = %s AND school_semester_id = %s AND school_department_id = %s"
)
count_course_book_query = (
    "SELECT COUNT(course_id) FROM course_books WHERE book_id = %s AND course_id = %s"
)
select_prof_query = (
    "SELECT professor_id FROM professors WHERE last_name = %s"
)
select_dept_query = (
    "SELECT school_department_id FROM school_departments WHERE code = %s"
)
select_course_query = (
    "SELECT course_id FROM courses WHERE professor_id = %s AND school_semester_id = %s AND school_department_id = %s AND code = %s"
)
select_book_query = (
    "SELECT book_id FROM books WHERE isbn13 = %s LIMIT 1"
)

insert_users = (
"INSERT INTO users (school_id,email,password)"
"VALUES (%s,%s,%s)"
)
insert_users_with_default_password = (
"INSERT INTO users (school_id,email,password)"
"VALUES (%s,%s,'1135treatave')"
)
select_user_by_email = (
"SELECT * FROM users WHERE email = %s"
)
insert_students = (
"INSERT INTO students (user_id,first_name,last_name,fb_link,phone_number,grad_year)"
"VALUES (%s,%s,%s,%s,%s,%s)"
)
insert_students2 = (
"INSERT INTO students (user_id, id_number, first_name,last_name, grad_year)"
"VALUES (%s,%s,%s,%s,%s)"
)

select_all_students = (
"SELECT * FROM students"
)

update_students = (
"UPDATE students SET id_number = %s WHERE first_name = %s AND last_name = %s"
)

select_book_by_isbn = (
"SELECT COUNT(*) FROM books WHERE isbn10 = %s OR isbn13 = %s"
)

select_book_id_from_books = (
"SELECT book_id FROM books WHERE isbn10 = %s OR isbn13 = %s"
)

book_select_via_title = (
"SELECT book_id FROM books WHERE title = %s AND authors = %s"
)

book_select_via_isbns1 = (
"SELECT book_id FROM books WHERE isbn13 = %s"
)
book_select_via_isbns2 = (
"SELECT book_id FROM books WHERE isbn10 = %s"
)
book_select_via_isbns3 = (
"SELECT book_id FROM books WHERE isbn10 = %s AND isbn13 = %s"
)
select_user_by_email_huntley = (
"SELECT user_id FROM users WHERE email = %s"
)

insert_listing_query = (
"INSERT INTO listings (listing_id, book_id, user_id, `condition`, `additional_information`,`created_at`, `deleted_at`)"
"VALUES (%s, %s, %s, %s, %s, %s, %s)"
)

insert_listing_for_sale_detail_query = (
"INSERT INTO listing_for_sale_details (listing_id, `availability`, `removal_reason`, `price`)"
"VALUES (%s, %s, %s, %s)"
)
insert_listing_for_rent_detail_query = (
"INSERT INTO listing_for_rent_details (listing_id, `availability`, `removal_reason`)"
"VALUES (%s, %s, %s)"
)

select_from_students = (
    "SELECT * FROM students WHERE id_number = %s"
)

insert_into_rented_listings = (
"INSERT INTO rented_listings ( `listing_id`, `student_id`, `school_semester_id`,`rent_date`,`return_date`,`condition_change`, `yellow_flag`)"
" VALUES (%s, %s, %s, %s, %s, %s, %s)"
)

insert_into_account_notes = (
"INSERT INTO account_notes (`student_id`,`created_at`)"
" VALUES (%s, %s)"
)

multi_join_rented_listings_to_books = (
"SELECT * FROM rented_listings INNER JOIN listings ON rented_listings.listing_id = listings.listing_id INNER JOIN books ON books.book_id = listings.book_id WHERE student_id = %s"
)

select_account_notes_huntley = (
"SELECT * FROM account_notes"
)

insert_into_account_flag_change_notes = (
"INSERT INTO `account_flag_changes_notes` (`account_note_id`, `admin_id`, `rented_listing_id`, `reason_id`, `flag_change_id`)"
"VALUES (%s, %s, %s, %s, %s)"
)
