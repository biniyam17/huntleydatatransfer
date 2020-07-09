from sql_5c_public import *
from sql_huntley import *

school_map = {
"Claremont" : 1,
"Pomona" : 2,
"Pitzer" : 3,
"Scripps" : 4,
"Harvey Mudd" : 5,
}

def transfer_users_to_users(db1, db2, cursor1, cursor2):
    cursor2.execute(select_all_users)
    db2.commit()
    for user in cursor2:
        email = user[2]
        password = user[3]
        school_id = school_map.get(user[5])
        cursor1.execute(insert_users, (school_id,email,password,))
        db1.commit()
    db1.close()
    db2.close()

def transfer_users_to_students(db1, db2, cursor1, cursor2):
    cursor2.execute(select_all_users)
    db2.commit()
    user_id = 0
    for user in cursor2:
        user_id = user_id + 1
        if (user[2] == 'care@cmc.edu'):
            continue
        fname = user[1].split()[0]
        lname = user[1].split()[1]
        grad_year = user[6]
        fb = user[7]
        phone = user[8]
        cursor1.execute(insert_students, (user_id,fname,lname,fb,phone,grad_year,))
        db1.commit()
    db1.close()
    db2.close()

def transfer_renters_to_students_existing(db1, db2, cursor1, cursor2):
    cursor2.execute(select_all_renters)
    for renter in cursor2:
        id = renter[0]
        fname = renter[1]
        lname = renter[2]
        email = renter[3]
        cursor1.execute(select_user_by_email, (email,))
        result = cursor1.fetchall()
        if (result == []): #does not exists
            grad = convert_email_to_grad_year(email)
            print (grad)
            cursor1.execute(insert_users_with_default_password, (1,email,))
            db1.commit()
            cursor1.execute(select_user_by_email, (email,))
            user_id = cursor1.fetchall()[0][0]
            cursor1.execute(insert_students2, (user_id, id, fname,lname,grad,))
            db1.commit()
        else: #Exists
            print ( "FOUND A MATCH" )
            print ( email )
            #update existing student record with id
            # cursor1.execute(update_students, (id,fname,lname))
            # db1.commit()

def convert_email_to_grad_year(email):
    list = []
    for s in email:
        if (s.isdigit()):
            list.append(s)
    return ("".join(list))

def transfer_listings_to_books(db1, db2, cursor1, cursor2):
    cursor2.execute(select_all_listings)
    record_exists = 0
    new_records = 0
    for listing in cursor2:
        upload_id = listing[0]
        title = listing[1]
        author = listing[2]
        isbn = listing[3]
        isbn13 = listing[4]
        cursor1.execute(select_book_by_isbn, (isbn,isbn13,))
        matches = cursor1.fetchall()[0][0]
        if (matches == 1):
            record_exists = record_exists + 1
            continue
        elif (matches == 0):
            new_records = new_records + 1
            list[upload_id] = False
            # cursor1.execute(books_full_insert_query, (isbn13,isbn,title,author,None,))
            # db1.commit()
        else:
            print ("matches: " + str(matches))
    print (str(new_records) + " records inserted")
    print (str(record_exists) + " records already existed")
    print (list)

#transfer_listings_to_books function missed edge case where we update
#the complementary isbn in Huntley DB if we match only via one isbn only
#this function addresses that use case
def transfer_remaining_listings_to_books(db1, db2, cursor1, cursor2):
    cursor2.execute(select_all_listings) #old 5c database
    zero_count = 0
    over_one_count = 0
    good_matches = 0
    for listing in cursor2:
        upload_id = listing[0]
        title = listing[1]
        author = listing[2]
        isbn = listing[3]
        isbn13 = listing[4]

        if (isbn is None and isbn13 is None):
            cursor1.execute(book_select_via_title, (title,author,))
        if (isbn is None and isbn13 is not None):
            cursor1.execute(book_select_via_isbns1, (isbn13,))
        if (isbn13 is None and isbn is not None):
            cursor1.execute(book_select_via_isbns2, (isbn,))
        if (isbn13 is not None and isbn is not None):
            cursor1.execute(book_select_via_isbns3, (isbn,isbn13,))

        sub_result = cursor1.fetchall()
        results = len(sub_result)
        if (results is 0):
            zero_count = zero_count + 1
            # cursor1.execute(books_full_insert_query, (isbn13,isbn,title,author,None,))
            # db1.commit()
        if (results > 1):
            over_one_count = over_one_count + 1
        if (results == 1):
            good_matches = good_matches + 1
    print (zero_count)
    print (over_one_count)
    print (good_matches)

def transfer_listings_to_listings(db1, db2, cursor1, cursor2):
    cursor2.execute(select_all_listings) #old 5c database
    cursor3 = db1.cursor(buffered=True) #huntley
    cursor4 = db2.cursor(buffered=True) #old 5c database
    for listing in cursor2:
        upload_id = listing[0]
        title = listing[1]
        author = listing[2]
        isbn = listing[3]
        isbn13 = listing[4]
        cond = listing[5]
        add_info = listing[6]
        price = listing[7]
        user_id = listing[8]
        availability = listing[9]
        upload_date = listing[10]
        removal_date = listing[11]
        removal_reason = listing[12]

        #huntley db for book_id
        if (isbn is None and isbn13 is None):
            cursor1.execute(book_select_via_title, (title,author,))
        if (isbn is None and isbn13 is not None):
            cursor1.execute(book_select_via_isbns1, (isbn13,))
        if (isbn13 is None and isbn is not None):
            cursor1.execute(book_select_via_isbns2, (isbn,))
        if (isbn13 is not None and isbn is not None):
            cursor1.execute(book_select_via_isbns3, (isbn,isbn13,))
        book_id = cursor1.fetchall()[0][0]
        #old 5c db for user_email
        cursor4.execute(select_user_by_id, (user_id,)) #old 5c database
        user_email = cursor4.fetchall()[0][0]
        #huntley for user_id
        cursor1.execute(select_user_by_email_huntley, (user_email,)) #huntley
        huntley_user_id = cursor1.fetchall()[0][0]
        #insert listing in huntley
        try:
            cursor1.execute(insert_listing_query, (upload_id,book_id,huntley_user_id,cond, add_info, upload_date, removal_date,))
            db1.commit()
        except Exception as e:
            print (e)

        # #create listing for rent record
        if (user_id != 2):
            try:
                cursor1.execute(insert_listing_for_sale_detail_query, (upload_id,availability,removal_reason,price,))
                db1.commit()
            except Exception as e:
                print (e)
                raise
        else:
            try:
                cursor1.execute(insert_listing_for_rent_detail_query, (upload_id,availability,removal_reason,))
                db1.commit()
            except Exception as e:
                print (e)
                raise

def transfer_rented_listings(db1, db2, cursor1, cursor2):
    cursor2.execute(select_all_rented_listings) #old 5c database
    # cursor3 = db1.cursor(buffered=True) #huntley
    # cursor4 = db2.cursor(buffered=True) #old 5c database
    count = 0
    for rl in cursor2:
        id = rl[0]
        rent_date = rl[1]
        return_date = rl[2]
        cond_change = rl[3]
        upload_id = rl[4]
        id_number = rl[5]
        semester_id = rl[6]
        yellow_flag = rl[7]

        cursor1.execute(select_from_students, (id_number,))
        result = cursor1.fetchall()
        student_id = result[0][0]

        try:
            cursor1.execute(insert_into_rented_listings, (upload_id,student_id,semester_id,return_date, return_date, cond_change, yellow_flag,))
            db1.commit()
        except Exception as e:
            print (e)
            raise

def parse_account_notes(db1, db2, cursor1, cursor2):
    # cursor2.execute(select_account_notes) #old 5c database
    # count = 1
    # for note in cursor2:
    #     if (count == 1):
    #         count = count + 1
    #         continue
    #     if (count > 42):
    #         break
    #     renter_id = note[2]
    #     created_at = note[4]
    #     cursor1.execute(select_from_students, (renter_id,))
    #     result = cursor1.fetchall()
    #     student_id = result[0][0]
    #     cursor1.execute(insert_into_account_notes, (student_id,created_at))
    #     db1.commit()
    #     count = count + 1

        # print (note[0])
        # print (str(renter_id) + "===>" + str(student_id))

    # cursor3 = db1.cursor() #huntley
    # cursor1.execute(select_account_notes_huntley)
    # for note in cursor1:
    #     student_id = note[1]
    #     cursor3.execute(multi_join_rented_listings_to_books,(student_id,))
    #     rows = cursor3.fetchall()
    #     for row in rows:
    #         print (row)
    #     break
    # cursor1.execute(insert_into_account_flag_change_notes, (count, 4, ,4,3))
