from util import *

def is_valid_dept(dept):
    return not emptyStringCheck(dept)

def encoder(input):
    return str(input).strip()

def is_valid_course(course_input):
    return not emptyStringCheck(course_input) and isNumericOrFloat(course_input)

def is_valid_instructor(instructor):
    return not emptyStringCheck(instructor) and not isNumericOrFloat(instructor)

def is_valid_section(section):
    return not emptyStringCheck(course_input) and isNumericOrFloat(course_input)

def is_valid_ISBN(ISBN):
    return (not emptyStringCheck(course_input) and isNumericOrFloat(course_input)
    and (is_ISBN_10(ISBN) or is_ISBN_13(ISBN)))

def is_valid_author(author):
    return not emptyStringCheck(author)

def is_valid_title(title):
    return not emptyStringCheck(title)

def is_valid_edition(edition):
    return not emptyStringCheck(edition)
