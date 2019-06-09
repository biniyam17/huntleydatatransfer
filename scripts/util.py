# @author           Biniyam Asnake
# @date             July 2018
#
# @description      util.py is a catalog of helper functions for
#                   excelBookUploader.py


#---------------------------------------------------------------------------------------------------------------

# write_list
#
# This function formats printing in the Summary section.
#
# @param    string      first part of print
# @param    list        list of items to be printed
# @prints   string      statement + (list of items or Empty List)

def write_list(statement, lst):
    print statement
    if (len(lst) == 0):
        print 'Empty List'
    else:
        for item in lst:
            print str(item) + ' '

# emptyStringCheck
#
# This function checks if the passed input is empty.
#
# @param    string
# @returns  boolean     True or False

def emptyStringCheck(input):
    if (input is None):
        return True
    else:
        if (type(input) is float ):
            return (False if (len(str(input)) > 0) else True)
        else:
            return (False if (len(input) > 0) else True)

# isNumericOrFloat
#
# This function returns if the passed input is an int or float.
#
# @param    string
# @returns  boolean     True or False

def isNumericOrFloat(input):
    if ((type(input) is int) or (type(input) is float)):
        return True
    else:
        return False

# requestComplete
#
# This function returns whether or not all of the requested rows were inputted
# into the database
#
# @param    string
# @param    string
# @param    integer
# @returns  boolean     True or False

def requestComplete(startpoint, endpoint, entriesMade):
    startpoint = startpoint[1:]
    endpoint = endpoint[1:]

    try:
        start = int(startpoint)
        end = int(endpoint)
    except ValueError:
        print " ValueError in requestComplete"
    else:
        expectedEntries = end - start + 1
        return expectedEntries == entriesMade

# locateNextEntry
#
# This function returns the integer value of the next row entry, based on how
# many entries were made.
#
# @param    string
# @param    string
# @param    integer
# @returns  boolean     True or False

def locateNextEntry(startpoint, endpoint, entriesMade):
    startpoint = startpoint[1:]
    endpoint = endpoint[1:]

    try:
        start = int(startpoint)
    except ValueError:
        print " ValueError in locateNextEntry"
    else:
        return start + entriesMade

# makeInputNumeric
#
# This function returns the numberic version of the input. If it fails, it quits the program.
# It quits because this function has to ensure the passed inputs are numeric or else
# the script can't run.
#
# @param    string
# @returns  integer     or quits script

def makeInputNumeric(input):
    try:
        return int(input)
    except ValueError:
        quit()
