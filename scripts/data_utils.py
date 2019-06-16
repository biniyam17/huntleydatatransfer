from sanitizer import *
from sql import *
from gBooksUtil import *

# Checks that each cell in a given column exists in the passed in dictionary
# @precondition: dict should have all unique values of the given column
def verify_element_exists(sheet, dict, i):
    rowList = []
    errors = 0
    for row in sheet:
        for cell in row:
            rowList.append(cell.value)
        cell = encoder(rowList[i])
        if cell not in dict:
            errors = errors + 1
            print ("CELL NOT FOUND IN LIST " + cell)
        rowList = []
    print ("Finished verifying all values in given column are present in the"
    "given dictionary. # of errors found : " +  str(errors) )

#unique only
def insert_departments(sheet, cursor, database, dict):
    for dept in dict:
        cursor.execute(department_insert_query, (dept,))
        database.commit()
    print ("Succesfully inserted all departments")

def insert_departments_v2(sheet, cursor, database, i):
    rowList = []
    rows_inserted = 0
    for row in sheet:
        for cell in row:
            rowList.append(cell.value)
        dept = encoder(rowList[i])
        cursor.execute(count_dept_query, (dept,))
        count = cursor.fetchall()[0][0]
        print ("dept: " + str(dept) + " " + str(count))
        if (count == 0):
            rows_inserted = rows_inserted + 1
            cursor.execute(department_insert_query, (dept,))
            database.commit()
        rowList = []
    print ("Succesfully inserted " + str(rows_inserted) + " departments")


#unique only
def insert_professors(sheet, cursor, database, dict):
    for prof in dict:
        cursor.execute(professor_insert_query, (prof,))
    database.commit()
    print ("Succesfully inserted all professors")

def insert_professors_v2(sheet, cursor, database, i):
    rowList = []
    rows_inserted = 0
    for row in sheet:
        for cell in row:
            rowList.append(cell.value)
        if (rowList[i] is None):
            print ("End of column reached. break.")
            break
        prof = encoder(rowList[i])
        cursor.execute(count_prof_query, (prof,))
        count = cursor.fetchall()[0][0]
        print ("prof: " + str(prof) + " " + str(count))
        if (count == 0):
            rows_inserted = rows_inserted + 1
            cursor.execute(professor_insert_query, (prof,))
            database.commit()
        rowList = []
    print ("Succesfully inserted " + str(rows_inserted) + " professors")

#unique only
def insert_books(sheet, cursor, database, dict):
    rowList = []
    rowCount = 0
    for row in sheet:
        for cell in row:
            rowList.append(cell.value)
        isbn = rowList[0]
        title = rowList[1]
        edition = rowList[2]
        if (isbn is None and title is None):
            print ("End of column reached. break.")
            break
        cursor.execute(book_insert_query, (isbn,title,edition,))
        rowList = []
        database.commit()
    print ("Succesfully inserted all books")

#unique only
def insert_courses(sheet, cursor, database, semester_id, i, j, prof_dict):
    rowList = []
    rowCount = 0
    for row in sheet:
        for cell in row:
            rowList.append(cell.value)
        print (rowList)
        print (rowCount)
        rowCount = rowCount + 1
        try:
            course = encoder(rowList[i])
            if (rowList[i] is None):
                print ("End of column reached. break.")
                break
            prof_id = prof_dict.get(encoder(rowList[j]))
            cursor.execute(course_insert_query, (prof_id, semester_id, course))
            rowList = []
            database.commit()
        except Exception as e:
            print ("course is " + course )
            print ("prof is " + encoder(rowList[j]) )
            raise

    print ("Succesfully inserted all courses")

#insert all b/c semester specific
def insert_courses_v2(sheet, cursor, database, i, semester_id):
    rowList = []
    rows_inserted = 0
    for row in sheet:
        for cell in row:
            rowList.append(cell.value)
        print (rowList)
        if (rowList[i] is None):
            print ("End of column reached. break.")
            break
        dept = encoder(rowList[i])
        code = encoder(rowList[i+1])
        prof = encoder(rowList[i+2])
        print ("course code: " + str(code))
        cursor.execute(select_prof_query, (prof,))
        prof_id = cursor.fetchone()[0]
        cursor.execute(select_dept_query, (dept,))
        dept_id = cursor.fetchone()[0]
        cursor.execute(course_insert_query, (prof_id, semester_id, code, dept_id,))
        database.commit()
        rows_inserted = rows_inserted + 1
        rowList = []
    print ("Succesfully inserted " + str(rows_inserted) + " courses")

#unique only
def update_courses(sheet, cursor, database, i, dept_dict):
    rowList = []
    rowCount = 0
    for row in sheet:
        for cell in row:
            rowList.append(cell.value)
        print (rowList)
        print (rowCount)
        rowCount = rowCount + 1
        try:
            if (rowList[i] is None):
                print ("End of column reached. break.")
                break
            dept_id = dept_dict.get(encoder(rowList[i]))
            cursor.execute(update_course_query, (dept_id, rowCount,))
            rowList = []
            database.commit()
        except Exception as e:
            print ("dept id is " + course )
            raise

    print ("Succesfully updated all courses")

def insert_course_books(sheet, cursor, database, book_dict, course_code_to_id_map):
    rowList = []
    rowCount = 0
    for row in sheet:
        for cell in row:
            rowList.append(cell.value)
        rowCount = rowCount + 1
        print (rowCount)
        if (rowList[0] is None and rowList[1] is None):
            print ("End of column reached. break.")
            break
        book_id = book_dict.get(encoder(rowList[1]))
        course_id = course_code_to_id_map.get(encoder(rowList[0]))
        if (course_id is None or book_id is None):
            print ("Could not find corresponding ids.")
            print (str(rowList[0]) + " " + str(rowList[1]))
            print (str(course_id) + " " + str(book_id))
            break
        cursor.execute(course_book_insert_query, (book_id, course_id,))
        rowList = []
        database.commit()
    print ("Succesfully inserted all course departments")

def insert_course_books_v2(sheet, cursor, database, semester_id, row_index):
    rowList = []
    rowCount = row_index - 1
    for row in sheet:
        for cell in row:
            rowList.append(cell.value)
        rowCount = rowCount + 1
        print (rowCount)
        dept = rowList[0]
        course = rowList[1]
        prof = rowList[2]
        isbn13 = rowList[4]
        print (dept)
        print (course)
        print (prof)
        print (isbn13)
        if (rowList[0] is None and rowList[1] is None):
            print ("End of column reached. break.")
            break
        cursor.execute(select_prof_query, (prof,))
        prof_id = cursor.fetchall()[0][0]
        cursor.execute(select_dept_query, (dept,))
        dept_id = cursor.fetchall()[0][0]
        cursor.execute(select_course_query, (prof_id, semester_id, dept_id,))
        course_id = cursor.fetchall()[0][0]
        cursor.execute(select_book_query, (isbn13,))
        book_id = cursor.fetchall()[0][0]
        #check if duplicate exists because of sections in class
        cursor.execute(count_course_query, (book_id, course_id,))
        count = cursor.fetchall()[0][0]
        if (count == 0):
            cursor.execute(course_book_insert_query, (book_id, course_id,))
            database.commit()
        else:
            print ("No insert because duplicate found")
        rowList = []
    print ("Succesfully inserted all course books")

def write_google_books_api_responses(sheet, cursor, database, row_index):
    rowList = []
    rowCount = row_index - 1
    for row in sheet:
        for cell in row:
            rowList.append(cell.value)
        print (rowCount)
        isbn13 = rowList[0]
        existingTitle = rowList[2]
        print (isbn13)
        print (existingTitle)
        response = makeGoogleBooksApiCall(isbn13)
        if not isApiResponseValid(response):
            rowCount = rowCount + 1
            rowList = []
            continue
        isbn10 = parseOtherIsbn(isbn13, response)
        title = parseTitle(response, existingTitle)
        authors = parseAuthors(response)
        print (title)
        print (authors)
        print (isbn10)
        cursor.execute(update_books_query, (isbn10, title, authors, rowCount,))
        database.commit()
        rowCount = rowCount + 1
        rowList = []

def write_google_books_api_responses_v2(sheet, cursor, database, row_index):
    rowList = []
    rowCount = row_index - 1
    rows_inserted = 0
    for row in sheet:
        for cell in row:
            rowList.append(cell.value)
        print (rowCount)
        isbn13 = rowList[0]
        existingAuthor = rowList[1]
        existingTitle = rowList[2]
        edition = rowList[3]
        if (isbn13 is None and existingTitle is None):
            print ("End of column reached. break.")
            break
        cursor.execute(count_book_query, (isbn13,))
        count = cursor.fetchall()[0][0]
        print ("Exists: " + ('no' if count==0 else 'yes'))
        if (count == 0):
            response = makeGoogleBooksApiCall(isbn13)
            if not isApiResponseValid(response):
                rowCount = rowCount + 1
                rowList = []
                rows_inserted = rows_inserted + 1
                cursor.execute(books_insert_query, (isbn13, None, existingTitle, existingAuthor, edition,))
                database.commit()
                continue
            isbn10 = parseOtherIsbn(isbn13, response)
            title = parseTitle(response, existingTitle)
            authors = parseAuthors(response, existingAuthor)
            print (title)
            print (authors)
            print (isbn10)
            rows_inserted = rows_inserted + 1
            cursor.execute(books_insert_query, (isbn13, isbn10, title[:199], authors[:199], edition,))
            database.commit()
        rowCount = rowCount + 1
        rowList = []
    print ("Books inserted : " + str(rows_inserted))

def insert_huntley_data(sheet, cursor, database, row_index):
    rowList = []
    rowCount = row_index - 1
    for row in sheet:
        for cell in row:
            rowList.append(cell.value)
        print (rowCount)
        # isbn13 = rowList[0]
        # if (isbn13 is None):
        #     print ("End of column reached. break.")
        #     break
        # new_shelf_price = doublify(sanitize_price(rowList[4]))
        # used_shelf_price = doublify(sanitize_price(rowList[5]))
        # new_rental_price = doublify(sanitize_price(rowList[6]))
        # used_rental_price = doublify(sanitize_price(rowList[7]))
        # cursor.execute(select_book_query, (isbn13,))
        # book_id = cursor.fetchall()[0][0]
        # print (book_id)
        # print (type(new_shelf_price))
        # print (new_shelf_price)
        values = (rowCount, "89",)
        cursor.execute(huntley_insert_query, values )
        database.commit()
        rowList = []
    print ("Finished uploading huntley prices")

def doublify(number):
    return str(number)

def sanitize_price(input):
    return input
