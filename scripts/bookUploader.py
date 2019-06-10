#dependencies
import openpyxl
import mysql.connector
import re

# from ../util import write_list, emptyStringCheck, isNumericOrFloat, requestComplete, locateNextEntry, makeInputNumeric
from config import port, database, user, password

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

#Database Actions
database = mysql.connector.connect(host='localhost',port=port,db=database, user=user, passwd=password)
cursor=database.cursor()
query="""INSERT INTO listing (title,author,isbn,isbn13,cond,additional_information,upload_date,user_id,availability) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""


for row in sheet:
    for cell in row:
        rowList.append(cell.value)

    rowCount += 1
    print ('* Row ' + str(rowCount))
