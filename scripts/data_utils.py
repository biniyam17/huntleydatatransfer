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

#unique only
def insert_professors(sheet, cursor, database, dict):
    for prof in dict:
        cursor.execute(professor_insert_query, (prof,))
    database.commit()
    print ("Succesfully inserted all professors")

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
        cursor.execute(update_books_from_api_query, (isbn10, title, authors, rowCount,))
        database.commit()
        rowCount = rowCount + 1
        rowList = []
