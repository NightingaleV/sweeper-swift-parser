'''
SWIFT Parsing Program
Joseph Feuer
'''

import pandas as pd
import numpy as np

allFields = pd.read_csv(r'/Users/josephfeuer/Desktop/SM.csv') # Set allFields equal to the result of the read_csv function, using the path name of the csv location

'''
createFields takes as input a message type (messageType) that the user wants to generate an array of fields for.
The function will return an array that holds all of the fields associated with the given message type.
'''
def createFields(messageType):
    mt = allFields.loc[:, ["MT", "Tag"]] # Use the loc function to set mt equal to the "MT" and "Tag" columns of allFields
    m103 = mt.loc[mt['MT'] == messageType, ['Tag']] # Use the loc function to set m103 to thee dataframe containing 'MT' where messageType equals mt['MT'] and 'Tag'
    fields = []
    m103D = m103.to_dict() # set m103D to the dictionary version of the dataframee m103
    data = list(m103D['Tag'].items()) # Set data equal to list of 'Tag' entries
    mArray = np.array(data) # Set mArray equal to the result of the array method, passing data in as input
    fieldsT = []
    for i in range(len(mArray)): # Loop through the length of mArray
        fieldsT.append(mArray[i][1]) # Append mArray[i][1] to fieldsT
    return fieldsT # Return fieldsT

##################################################################################################################################

'''
removeSpaces takes as input a file to read (file) and a character that should replace every new line character (replaceChar).
The function returns the contents of file after replacing every new line character with replaceChar.
'''
def removeSpaces(file, replaceChar):
    with open(file, "r") as infile: # Open file in read mode
         f = infile.read() # Set f equal to infile.read()
         f = f.replace("\n", replaceChar) # Call the replace method to replace every new line character with the replaceChar
         return f # Return f

##################################################################################################################################

'''
parseMultMesg takes a string (mesg) as input that signifies a string of many SWIFT messages together.
The second parameter (delim) signifies the character that sepearates SWIFT messages from each other (e.g. '$').
When executed, this function will return an array where each index holds an individual SWIFT message.
'''
def parseMultMesg(mesg, delim):
    mesgs = []
    origMesg = mesg # Set origMesg equal to mesg
    length = len(mesg)
    i = 0
    while (i < length): # While i is less than length
        searchFor = '}' + delim + '{' # Set searchFor equal to a string in the formaat of '}delim{'
        endIndex = (mesg.find(searchFor)) + 1 # Set endIndex equal to the index where searchFor appears
        if (mesg[:endIndex] == ''): # If there is nothing before endIndex within mesg
            mesgs.append(mesg) # Append mesg to mesgs
            return mesgs # Return mesgs
        mesgs.append(mesg[:endIndex]) # Append mesg[:endIndex] to mesgss
        mesg = mesg[endIndex:] # Set mesg equal to everything coming after endIndex
        i = i + 1  # Increment i

##################################################################################################################################

'''
createEntries takes as input a series of SWIFT messages (mesg) and a dictionary (mesgEntries).
The function will return a filled version of mesgEntries, which will hold each index and the content of that index.
'''
def createEntries(mesg, mesgEntries):
    i = 0
    inputMesg = mesg # Set inputMesg equal to mesg
    for i in range(4): # For each of the four blocks
        inputMesg = parseMesg(inputMesg, mesgEntries) # Set inputMesg to the result of parseMesg (returns remaineder of message to be parsed
    return mesgEntries # Return mesgEntries

'''
parseMesg takes as input a SWIFT message (mesg) and a dictionaary (mesgEntries).
Each call to the function will add on block of the SWIFT message to mesgEntries and return the remainder of the SWIFT message to be parsed.
'''
def parseMesg(mesg, mesgEntries):
    fields = ['13C', '20', '23B', '23E', '26T', '32A', '33B', '36', '50A', '50F', '50K', '51A', '52A', '52D', '53A', '53B', '53D', '54A', '54B', '54D', '55A', '55B', '55D', '56A', '56C', '56D', '57A', '57B', '57C', '57D', '59', '59A', '59F', '70', '71A', '71F', '71G', '72', '77B'] # Create a default value for fields
    i = 0
    entryNum = 0
    while (True):
        if (mesg[i].isdigit()): # If the current character is a digit
            entryNum = mesg[i] # Set entryNum equal to the current character
            mesg = mesg[i:] # Set mesg equal to everything after the current character
            if (entryNum == '4'): # If in block 4
                mesg = mesg[2:] # Set mesg equal to everything after index 2
                return createEntries4(mesg, mesgEntries, fields) # Return the result of createEntries4
            else: # Otherwise
                startIndex = mesg.index(':') + 1 # Set startIndex equal to the index after the first apperance of ':'
                content = mesg[int(startIndex):] # Set content equal to everything in mesg after startIndex
                tIndex = content.index('}') # Set tIndex equal to the index of '}'
                content = content[:tIndex] # Reset content equal to everything before tIndex
                if (content[0] == '{'): # If the first character of content is now '{'
                    content = content[1:] # Reset content to everything after index 1
                mesgEntries.setdefault(int(entryNum), []).append(content) # Apppend to mesgEntries in the form of {entryNum: content}
                if (entryNum == '2'): # If entryNum equals 2
                    mt = content[1:4] # Set mt (for message type) equal to the characters in between indeces 1 and 4
                    fields = createFields(mt) # Set fields equal to the result of createFields
                return mesg[(tIndex + 3):] # Return the rest of mesg that has not yet been parsed and added to mesgEntries
        else: # Otherwise
            i = i + 1 # Increase i by 1

'''
createEntries4 takes as input the content of block 4 (content), a dictionary to append to (contentEntries), and an array of fields to references (fields).
The function works in a similar way as createEntries, returning a completed version of contentEntries.
'''
def createEntries4(content, contentEntries, fields):
    i = 0
    inputMesg = [content, 0] # Set inputMesg to an array (first index will be the actual content, second index will be the index currently being looked at)
    while (len(inputMesg[0]) > 1): # While the length of the content is greater than 1
       lastIndex = inputMesg[1] # Set lastIndex equal to the current index indicated by inputMesg
       inputMesg = parse4(inputMesg[0], contentEntries, inputMesg[1], fields) # Set inputMesg equal to the result of parse4
       try:
           length = len(inputMesg[0]) # Try setting length equal to the length of content (inputMesg[0])
       except TypeError: # Catch a TypeError
           if (lastIndex < len(fields)): # If lastIndex is less than the length of fields
               for i in range(len(fields) - lastIndex): # Loop through the difference of length of fields and lastIndex
                   if (i != 0): # If i is not equal to 0
                       contentEntries.setdefault(fields[lastIndex + i], []).append(None) # Append an entry of None to contentEntrues
           return contentEntries # Return contentEntries
    return contentEntries # Return contentEntries

'''
parsse4 takes as input the content of block 4 (content), a dictionary to append to (contentEntries), and the current index being looked at (index).
On each call of the function, contentEntries is appended to and an array in the form of [content, index] is returned to use for future reference.
'''
def parse4(content, contentEntries, index, fields):
    i = 0
    if (index == 0):
        n = index
    else:
        n = index + 1
    while (i < len(content)): # While i is less than the length of content
        if (content[i].isdigit()): # If content[i] is a digit
            content = content[i:] # Set content equal to everything after i
            numEndIndex = content.index(':') # Set numEndIndex equal to the first apperance of ':' in content
            entryNum = content[:numEndIndex] # Set entryNum equal to everything before numEndIndex in content
            content = content[(numEndIndex + 1):] # Set content equal to everything after numEndIndex + 1 in content
            if (int(entryNum[:2]) > 60): # If entryNum is greater than 60
                endIndex = 0
                try:
                    endIndex = content.index(':') # Try to set endIndex equal to the first apperance of ':'
                except ValueError: # Catch a ValueError
                    endIndex = content.index('-') # Set endIndex equal to the first apperance of '-'
                cText = content[:endIndex] # Set cText equal to everything before endIndex in content
            else: # Otherwise
                endIndex = content.index(':') # Set endIndex equal to the first apperance of ':'
                cText = content[:endIndex] # Set cText equal to everything before endIndex in content
            while (n < len(fields)): # While n is less than the length of fields
                if (entryNum != fields[n]): # If entryNum is not equal to fields[n]
                    contentEntries.setdefault(fields[n], []).append(None) # Append None to contentEntriess
                else: # Otherwise
                    contentEntries.setdefault(entryNum, []).append(cText) # Append the actual value of cText to contentEntries
                    result = [content[(endIndex):], n] # Set result equal to [content[(endIndex):], n]
                    return [content[(endIndex):], n] # Return [content[(endIndex):], n]
                n = n + 1 # Increment n by 1
        else: # Otherwise
            i = i + 1 # Increment i by 1

##################################################################################################################################

'''
findCov takes as inpput a message (mesg) that contains a field for COV.
The function returns an array where the first index is equal to the message as if there was no COV and where the second index is equal to the COV.
'''
def findCov(mesg):
    covIndex = mesg.find('{COV:') # Set covIndex equal to the index where '{COV:' first appears within mesg
    first = mesg[:(covIndex)] # Set first equaal to everything before covIndex within mesg
    newS = mesg[covIndex:] # Set newS equal to everything after covIndex within mesg
    covEndIndex = newS.find('}') # Set covEndIndex equal to the index where '}' appepars within newS
    second = newS[(covEndIndex + 1):] # Set second equal to everythin after covEndIndex + 1 within newS
    return [(first + second), newS[:covEndIndex + 1]] # Return an array where the first index is equat to first + second and the second index is equal to the COV message

##################################################################################################################################

'''
createTable takes as input data (data) to convert into a Data Frame, which is essentially a table.
The function returns the Data Frame.
'''
def createTable(data):
    pd.options.display.precision = 18
    df = pd.DataFrame(data) # Set df equal to the return value of the DataFrame method, passing data as input
    return df # Return df

'''
transposeTable takes as input a data frame (table), a dictionary (mesgEntries), and an index (index).
The function returns a dictionary that can then be converted into another data frame.
'''
def transposeTable(table, mesgEntries, index):
    arr1 = []
    arr2 = []
    arr3 = []
    #for i in range(len(fields)): # Loop through the fields
    for i in range(len(table.columns)):
        arr1.append(fields[i]) # Append the name of field to arr1
        arr2.append(mesgEntries[fields[i]][index]) # Append the content of the field to arr2
        arr3.append(mesgEntries[3][index]) # Append the id of the transaction to arr3
    return {'TID': arr3, 'F': arr1, 'Content': arr2} # Return the dictionary

