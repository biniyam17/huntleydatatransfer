# @author           Biniyam Asnake
# @date             January 2018
#
# @description      gBooksUtil.py is a catalog of functions written specifically
#                   to make google book api calls, verify responses, and parse
#                   through valid responses

#dependencies
import urllib
import json
import re

from config import key

#global variables and counters to track script success
isbnRegEx = re.compile(r"[^0-9X]")
isbnCallCount = 0
findsOtherIsbn = 0
invalidApiResponses = 0

#---------------------------------------------------------------------------------------------------------------

# isApiResponseValid
#
# This function determines if the api response is valid.
#
# @param    dictionary  response
# @return   boolen      True or False
#
# @global   invalidApiResponses   tracks the number of invalid Api responses

def isApiResponseValid(response):
    global invalidApiResponses
    totalItems = response["totalItems"]

    if (response["totalItems"] > 0):
        return True
    else:
        print " No Response"
        invalidApiResponses = invalidApiResponses + 1
        return False

# makeGoogleBooksApiCall
#
# This function calls the google books api and returns the response if valid. If
# not valid, returns False.
#
# @param    isbn
# @return   False or dictionary

def makeGoogleBooksApiCall(isbn):

    #serviceurl is the base url waiting for isbn input of either 10 or 13 digits
    serviceurl = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'

    fields='&fields=items/volumeInfo(title,authors,industryIdentifiers),totalItems'

    url = serviceurl + isbn + key +fields

    #get a handle by urlopen
    uh = urllib.urlopen(url)

    #read the returned file. Do not need to decode because it's not in UTF-8
    data = uh.read()

    print( 'Retrieved', len(data), 'characters')

    #takes a json string and converts it to a dictionary structure
    response = json.loads(data)

    if (isApiResponseValid(response)):
        return response
    else:
        return False

# parseOtherIsbn
#
# This function takes a valid google books api response and returns a
# complimentary isbn for the one given.
#
# @param    integer     original isbn
# @param    dictionary  response
# @return   integer     complementary isbn or 'N/A'
#
# @global   isbnCallCount   tracks the number of parseOtherIsbn function calls
# @global   findsOtherIsbn  tracks the number of succesful parseOtherIsbn function calls

def parseOtherIsbn(isbn, response):
    global isbnCallCount
    global findsOtherIsbn

    isbnCallCount = isbnCallCount + 1

    try:
        newIsbn = response["items"][0]["volumeInfo"]["industryIdentifiers"][0]["identifier"].encode('utf-8')
        # print newIsbn
    except IndexError:
        print " Index Error at [industryIdentifiers][0][identifier] for book with isbn: " + isbn
        return "N/A"
    except KeyError:
        print " Key Error: at [industryIdentifiers][0][identifier] for book with isbn: " + isbn
        return "N/A"

    newIsbn = re.sub(isbnRegEx,"",newIsbn)

    if (len(isbn)==10):
        if (len(newIsbn)==13):
            findsOtherIsbn = findsOtherIsbn +1
            return newIsbn
        else:
            try:
                newIsbn = response["items"][0]["volumeInfo"]["industryIdentifiers"][1]["identifier"].encode('utf-8')
                findsOtherIsbn = findsOtherIsbn +1
                return re.sub(isbnRegEx,"",newIsbn)
            except IndexError:
                print " Index Error at [industryIdentifiers][1][identifier] for book with isbn: " + isbn
                return "N/A"
            except KeyError:
                print " Key Error: at [industryIdentifiers][1][identifier] for book with isbn: " + isbn
                return "N/A"
    else:
        if (len(newIsbn)==10):
            findsOtherIsbn = findsOtherIsbn +1
            return newIsbn
        else:
            try:
                newIsbn = response["items"][0]["volumeInfo"]["industryIdentifiers"][1]["identifier"].encode('utf-8')
                findsOtherIsbn = findsOtherIsbn +1
                return re.sub(isbnRegEx,"",newIsbn)
            except IndexError:
                print " Index Error at [industryIdentifiers][1][identifier] for book with isbn: " + isbn
                return "N/A"
            except KeyError:
                print " Key Error: at [industryIdentifiers][1][identifier] for book with isbn: " + isbn
                return "N/A"

# parseTitle
#
# This function parses the response for a title. Returns the title if found or
# existing title if not found.
#
# @param    dictionary  response
# @param    string      existing title
# @return   string      title (existing or from response)

def parseTitle(response, existingTitle):
    try:
        title = response["items"][0]["volumeInfo"]["title"].encode('utf-8')
        # print title
        return title
    except IndexError:
        print " Index Error at [items][0][volumeInfo][title] for book with title: " + existingTitle
        return existingTitle
    except KeyError:
        print " Key Error: at [items][0][volumeInfo][title] for book with title: " + existingTitle
        return existingTitle

# parseAuthors
#
# This function parses the response for any author(s). Returns the auhors if found
# or existing author(s) if not found.
#
# @param    dictionary  response
# @param    string      existing author
# @return   string      author(s) (existing or from response)

def parseAuthors(response, existingAuthor):
    try:
        author = response["items"][0]["volumeInfo"]["authors"][0].encode('utf-8')
    except IndexError:
        print " Index Error at at [items][0][volumeInfo][authors] for book with title: " + existingAuthor
        return existingAuthor
    except KeyError:
        print " Key Error: at [items][0][volumeInfo][authors] for book with title: " + existingAuthor
        return existingAuthor

    #check for additionalAuthors
    allAuthors = author
    index =1

    while (index > 0):
        try:
            author = response["items"][0]["volumeInfo"]["authors"][index].encode('utf-8')
            index = index +1
            allAuthors = allAuthors + ', ' + author
        except IndexError:
            index = -1

    return allAuthors
