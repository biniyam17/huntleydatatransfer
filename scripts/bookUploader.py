#dependencies
import openpyxl
import mysql.connector
import re

# from ../util import write_list, emptyStringCheck, isNumericOrFloat, requestComplete, locateNextEntry, makeInputNumeric
from config import port, database, user, password
from sanitizer import *
from sql import *
#global variables
isbnRegEx = re.compile(r"[^0-9X]")

startpoint = 'B' + str(2)
endpoint = 'I' + str(280)

#Workbook Actions
doc = openpyxl.load_workbook('../excel/CMC_Fall_2018_bookstore_list.xlsx', read_only = True, data_only = True)
print (doc.sheetnames)
doc = doc.active
sheet = doc[startpoint:endpoint]
rowList = []
rowCount=0

#Database Actions
database = mysql.connector.connect(host='localhost',port=port,db=database, user=user, passwd=password)
cursor=database.cursor()


for row in sheet:
    for cell in row:
        rowList.append(cell.value)

    #Dept
    if not (is_valid_dept(rowList[0])):
        print ("not valid")
    cursor.execute(dept_check_query)
    result = cursor.fetchone()
    print (result[0])
    cursor.execute(dept_insert_query)
    database.commit()
    # if (cursor.execute(dept_check_query,(rowList[0])) == 0):
    #     cursor.execute(dept_insert_query, (rowList[0]) )
    # else:
    #     cursor.execute(dept_select_query, (rowList[0]) )

    if rowCount == 1:
        print ("break")
        break

    rowCount += 1
    print ('* Row ' + str(rowCount))
