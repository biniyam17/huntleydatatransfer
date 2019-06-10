dept_insert_query = """INSERT INTO school_departments (school_id,department_code)
            VALUES (1,%s)"""
dept_check_query = """SELECT COUNT(1) FROM school_departments WHERE school_id = 1 AND code = %s"""

professor_insert_query = """INSERT INTO professors (school_id,last_name)
            VALUES (1,%s)"""
professor_check_query = """SELECT COUNT(1) FROM professors WHERE school_id = 1 AND last_name = %s"""

# cursor.execute(query,values)
