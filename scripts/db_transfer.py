#dependencies
import mysql.connector

from config import *
from sql_5c_public import *
from data_utils_5c_public import *

#Database Actions
#huntley
db1 = mysql.connector.connect(host='localhost',port=port,db=database, user=user, passwd=password)
cursor1=db1.cursor()
#5c_public
db2 = mysql.connector.connect(host='localhost',port=port,db=database2, user=user, passwd=password)
cursor2 = db2.cursor(buffered=True)

# class Connection:
#     def __init__(self):
#         self.database1 = database1
#         self.db2 = database2
#         self.cursor1 = cursor1
#         self.cursor2 = cursor2
#
#     def db1(query, values = None):
#         if (values is None):
#             cursor2.execute(query)
#         else:
#             cursor2.execute(query, values)

# transfer_users_to_users(db1, db2, cursor1, cursor2)
# transfer_users_to_students(db1, db2, cursor1, cursor2)
# transfer_renters_to_students_existing(db1, db2, cursor1, cursor2)
# convert_email_to_grad_year("asdf234")
# transfer_listings_to_books(db1, db2, cursor1, cursor2)
# transfer_listings_to_listings(db1, db2, cursor1, cursor2)
# transfer_rented_listings(db1, db2, cursor1, cursor2)
# parse_account_notes(db1, db2, cursor1, cursor2)

db1.close()
db2.close()
