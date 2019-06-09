# @author           Biniyam Asnake
# @date             January 2018
#
# @description      excelBookUploader.py converts excel rows into entries in a
#                   mySql database. Leverages the googleBooksApi to ensure row
#                    accuracy and fill in missing data.

# @how-to-install-dependencies
#   Set up environment
#   sudo easy_install pip
#   pip install openpyxl (--user optional)
#   (sudo optional) pip install mysql-connector
#   install any other dependences using sudo easy_install nameHere

#dependencies
import openpyxl
import mysql.connector
import re

from util import write_list, emptyStringCheck, isNumericOrFloat, requestComplete, locateNextEntry, makeInputNumeric
from gBooksUtil import *
from config import port, database, user, password, key

#global variables
isbnRegEx = re.compile(r"[^0-9X]")
invalidIsbns = 0
invalidIsbnList = []
unsuccesfulParseOtherIsbnList = []
quantityTypeFieldErrorList = []

#breakpoint stops script every given number of rows
breakpoint = raw_input("Choose breakpoint (number required)? ")

#if enter is put in then no breakpoint essentially
if emptyStringCheck(breakpoint):
    breakpoint = 1000
else:
    breakpoint = makeInputNumeric(breakpoint)

startpoint = raw_input("Choose starting row (number required)? ")
startpoint = makeInputNumeric(startpoint)

endpoint = raw_input("Choose ending row (number required)? ")
endpoint = makeInputNumeric(endpoint)

gBooksApiFlag = raw_input("Press enter to keep the google books api off ")

#by pressing enter, the api flag is automatically off
if (emptyStringCheck(gBooksApiFlag)):
    gBooksApiFlag = False
else:
    gBooksApiFlag = True

#A -> F : title -> additional info
#Always start at A2 because of header row
startpoint = 'A' + str(startpoint)
endpoint = 'F' + str(endpoint)

#---------------------------------------------------------------------------------------------------------------

print 'Script running'
if (gBooksApiFlag):
    print 'API on'
else:
    print 'API off'

#Workbook Actions
doc = openpyxl.load_workbook('../records/bookdonationsSpring2018Edited.xlsx')
print doc.sheetnames
doc = doc.active
sheet = doc[startpoint:endpoint]
rowList = []
rowCount=0

#Database Actions
database = mysql.connector.connect(host='localhost',port=port,db=database, user=user, passwd=password)
cursor=database.cursor()
query="""INSERT INTO listing (title,author,isbn,isbn13,cond,additional_information,upload_date,user_id,availability) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

# cursor.execute("SELECT * FROM listing")
# results = cursor.fetchall()
# cnt = 0
# for row in results:
#     for col in row:
# 	print col
# 	print ' '
#     #print row[3]
#     cnt = cnt +1
#     if (cnt == 10):
# 	break

print "------------------------------------------------------------------------------------------------"

#Iterates through every row in the sheet
for row in sheet:
    for cell in row:
        rowList.append(cell.value)
    rowCount += 1
    print '* Row ' + str(rowCount)

    #Sanitize title, author, quantity, additional information, condition fields

    #Title
    if (not emptyStringCheck(rowList[0])):
        if (isNumericOrFloat(rowList[0])):
            title= str(rowList[0]).encode('utf-8').strip()
        else:
            title= str(rowList[0].encode('utf-8')).strip()
    else:
        title = ''

    #Author
    if (not emptyStringCheck(rowList[1])):
        author= str(rowList[1].encode('utf-8')).strip()
    else:
        author = ''

    #Condition
    try:
        if (not emptyStringCheck(rowList[4])):
            condition= str(rowList[4].encode('utf-8'))
        else:
            condition = '3'
    except AttributeError:
        print " AttributeError for Condition"
        condition = 3
    else:
        condition = condition.strip()
        if (condition == 'Good'):
            condition = 3
        elif (condition == 'Decent'):
            condition = 4
        elif (condition == 'Decent-Good'):
            condition = 3
        elif (condition == 'Poor'):
            condition = 5
        else:
            condition = 3

    #Additional Information
    if (not emptyStringCheck(rowList[5])):
        additional= str(rowList[5].encode('utf-8')).strip()
    else:
        additional = ''

    #Quantity
    #
    #@global quantityTypeFieldErrorList lists the rows with quantity errors
    if (not emptyStringCheck(rowList[2])):
        if (isNumericOrFloat(rowList[2])):
            quantity= str(rowList[2]).encode('utf-8').strip()
        else:
            print ' QuantityError not a valid numeric value'
            quantity = '1'
            quantityTypeFieldErrorList.append(rowCount)
    else:
        quantity = '1'
        quantityTypeFieldErrorList.append(rowCount)

    #Isbn
    if (not emptyStringCheck(rowList[3])):
        try:
            #deletes any dashes from the isbn
            isbn = rowList[3].strip()
            isbn = re.sub(isbnRegEx,"",isbn)
            # print 'isbn is ' + str(isbn)
        except TypeError:
            print 'TypeError for isbn on row ' + str(rowCount)
            isbn = ''
        else:
            if (isNumericOrFloat(isbn)):
                isbn= str(isbn).encode('utf-8')
            else:
                isbn= str(isbn.encode('utf-8'))
    else:
        isbn = ''

    # print 'next isbn is ' + str(isbn)
    #Make call to Google Books API
    #@return isbn and isbn13 have appropriate values, may include 'N/A'
    # @return update title and author with valid api response records
    #
    # @global   invalidIsbns    counts the number of invalid isbns from the excel sheet
    # @global   unsuccesfulParseOtherIsbnList
    #                           lists the rows that had valid api responses but couldn't
    #                           parse for the other isbn
    # @global   invalidIsbnList lists the rows with invalid isbns
    # print('before api flag is ' + str(gBooksApiFlag))

    if ( len(isbn) == 13 or len(isbn) == 10):

        # print('api flag is ' + str(gBooksApiFlag))
        #Checks user flag to run api or not
        if (gBooksApiFlag == True):
            apiResponse = makeGoogleBooksApiCall(isbn)
            # print('api response is ' + str(apiResponse))
        else:
            apiResponse = False

        #case - invalid api response or we don't make the api call
        if (apiResponse is False):
            if (len(isbn)==13):
                isbn13= isbn
                isbn = "N/A"
            elif (len(isbn)==10):
                isbn13 = "N/A"
            else:
                isbn = "N/A"
                isbn13 = "N/A"

        #case - valid api response
        else:
            if (len(isbn)==13):
                isbn13= isbn
                print 'isbn13 is ' + str(isbn13)
                isbn = parseOtherIsbn(isbn13, apiResponse)
                print 'isbn10 is ' + str(isbn)
                if (isbn == 'N/A'):
                     unsuccesfulParseOtherIsbnList.append(rowCount)
            #case assumes len(isbn) == 10 because check already exists in outer outer loop
            else:
                print 'isbn10 is ' + str(isbn)
                isbn13= parseOtherIsbn(isbn, apiResponse)
                print 'isbn13 is ' + str(isbn13)
                if (isbn == 'N/A'):
                     unsuccesfulParseOtherIsbnList.append(rowCount)

            #update title and author with api records
            title = parseTitle(apiResponse, title)
            author = parseAuthors(apiResponse, author)
    else:
        invalidIsbns = invalidIsbns +1
        invalidIsbnList.append(rowCount)
        isbn = "N/A"
        isbn13 = "N/A"

    #values for database entry
    values = (title,author,isbn,isbn13,condition,additional,"2018-08-03",'2','Y')

    #insert into database
    #TODO:uncomment below
    cursor.execute(query,values)

    #execute query quantity number of times
    try:
        quantity = int(float(quantity))

        while (quantity > 1):
            # TODO:uncomment below
            cursor.execute(query,values)
            quantity = quantity - 1
    except ValueError:
        print " ValueError for quantity while attempting multiple insert"
        quantityTypeFieldErrorList.append(rowCount)

    database.commit()

    print " data commited"

    #empty array for new row
    rowList =[]

    #Stops the script every 'breakpoint' number of rows
    if (rowCount % breakpoint == 0):
        input = raw_input("Press enter to continue ")
        if (not emptyStringCheck(input)):
            break;


#Summary
print "------------------------------------------------------------------------------------------------"
cursor.close()
print "cursor closed"
database.close()
print "finished uploading"
print "------------------------------------------------------------------------------------------------"
print 'Summary'
print 'Number of total entries made: ' + str(rowCount)
print 'Number of incorrect isbns given based on length: ' + str(invalidIsbns)
write_list('List of rows with incorrect isbns lengths given: ', invalidIsbnList)
write_list('List of rows with non numberic quantities: ', quantityTypeFieldErrorList)

if (gBooksApiFlag == True):
    print 'GOOGLE API STATS'
    print '************************'
    print 'Number of valid API responses: ' + str((rowCount-invalidApiResponses))
    print 'Number of parseOtherIsbn function calls : ' + str(isbnCallCount)
    print 'Number of successful parseOtherIsbn function calls: ' + str(findsOtherIsbn)
    write_list('List of rows with valid Apis but unsuccesful parseOtherIsbn calls: ', unsuccesfulParseOtherIsbnList)
    print '************************'

print 'All rows completed? ' + str(requestComplete(startpoint, endpoint, rowCount))
print 'Next entry should be at row # ' + str(locateNextEntry(startpoint, endpoint, rowCount))
print "------------------------------------------------------------------------------------------------"
