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


# for row in sheet:
#     for cell in row:
#         rowList.append(cell.value)

    #Dept
    # if not (is_valid_dept(rowList[0])):
    #     print ("not valid")

dept_list = {
"ARBC" : 1,
"ARBC" : 2,
"ECON" : 3,
"FHS" : 4,
"FREN" : 5,
"FWS" : 6,
"GOVT" : 7,
"HIST" : 8,
"KORE" : 9,
"LEAD" : 10,
"LIT" : 11,
"MATH" : 12,
"PHIL" : 13,
"PONT" : 14,
"PORT" : 15,
"PPE" : 16,
"PSYC" : 17,
"RLST" : 18,
"SPAN" : 19,
    }

prof_list = {
"Aitel" : 1,
"Altamirano" : 2,
"Antecol" : 3,
"Appel" : 4,
"Ascher" : 5,
"Batta" : 6,
"Bessette" : 7,
"Birkenbeuel" : 8,
"Bjerk" : 9,
"Bjornlie" : 10,
"Bowman" : 11,
"Brown" : 12,
"Busch" : 13,
"Charlop" : 14,
"Cody" : 15,
"Conger" : 16,
"Cook" : 17,
"Crockett" : 18,
"Day" : 19,
"Espinosa" : 20,
"Evans" : 21,
"Farrell" : 22,
"Favretto" : 23,
"Filson" : 24,
"Finley" : 25,
"Frangieh" : 26,
"Fukshansky" : 27,
"Ganguly" : 28,
"Gann" : 29,
"Gelman" : 30,
"Gilbert" : 31,
"Gonzales" : 32,
"Hamburg" : 33,
"Harris" : 34,
"Helland" : 35,
"Hernandez" : 36,
"Hughson" : 37,
"Ibragimov" : 38,
"Jones" : 39,
"Kanaya" : 40,
"Kao" : 41,
"Keil" : 42,
"Kim" : 43,
"Kind" : 44,
"Krauss" : 45,
"Kreines" : 46,
"Lobis" : 47,
"Magilke" : 48,
"Martin" : 49,
"Martinez" : 50,
"Mestaz" : 51,
"Miller" : 52,
"Morrison" : 53,
"Nadon" : 54,
"Nelson" : 55,
"Nichols" : 56,
"Olfati" : 57,
"Ozbeklik" : 58,
"Petropoulos" : 59,
"Pitney" : 60,
"Rajczi" : 61,
"Raviv" : 62,
"Rentz" : 63,
"Rose" : 64,
"Rosett" : 65,
"Rossum" : 66,
"Sarzynski" : 67,
"Schroeder" : 68,
"Shelton" : 69,
"Sinha" : 70,
"Skinner" : 71,
"Staff" : 72,
"Taylor" : 73,
"Thompson" : 74,
"Tocoian" : 75,
"Umanath" : 76,
"Valencia" : 77,
"Valenza" : 78,
"Velji" : 79,
"Venit-Shelton" : 80,
"Von Hallberg" : 81,
"Warner" : 82,
"Wyman" : 83,
"Yu" : 84,
}

for element in dept_list:
    print (element)
    cursor.execute(dept_insert_query, (element,))
    # result = cursor.fetchone()
    # print (result[0])
    # cursor.execute(dept_insert_query)
    database.commit()
for element in prof_list:
    print (element)
    cursor.execute(professor_insert_query, (element,))
    database.commit()

    # if (cursor.execute(dept_check_query,(rowList[0])) == 0):
    #     cursor.execute(dept_insert_query, (rowList[0]) )
    # else:
    #     cursor.execute(dept_select_query, (rowList[0]) )

    # if rowCount == 1:
    #     print ("break")
    #     break
    #
    # rowCount += 1
    # print ('* Row ' + str(rowCount))
