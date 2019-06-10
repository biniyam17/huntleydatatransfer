#dependencies
import openpyxl
import mysql.connector
import re

# from ../util import write_list, emptyStringCheck, isNumericOrFloat, requestComplete, locateNextEntry, makeInputNumeric

#global variables
isbnRegEx = re.compile(r"[^0-9X]")

startpoint = 'B' + str(2)
endpoint = 'I' + str(280)

#Workbook Actions
doc = openpyxl.load_workbook('../excel/CMC_Fall_2018_bookstore_list.xlsx')
print (doc.sheetnames)
doc = doc.active
sheet = doc[startpoint:endpoint]
rowList = []
rowCount=0

for row in sheet:
    for cell in row:
        rowList.append(cell.value)

    rowCount += 1
    print ('* Row ' + str(rowCount))
