import pandas as pd
import numpy as np

allFields = pd.read_csv(r'/Users/josephfeuer/Desktop/SM.csv') # Set allFields equal to the result of the read_csv function, using the path name of the csv location

#################################################################

def main(file, dataFrames):
    text = removeSpaces(file, '#')
    mesgs = parseMultMesg(text, '$')
    mesgEntries = {}
    for i in range(len(mesgs)):
        mesgs[i] = findCov(mesgs[i])[0]
        createEntries(mesgs[i], mesgEntries)
        mt = mesgEntries['2'][i][1:4]
        if (mt in dataFrames):
            createEntries(mesgs[i], dataFrames[mt][0])
        else:
            dataFrames.setdefault(mt, []).append(createEntries(mesgs[i], {}))
    return dataFrames


#################################################################

def removeSpaces(file, replaceChar):
    with open(file, "r") as infile: # Open file in read mode
         f = infile.read() # Set f equal to infile.read()
         f = f.replace("\n", replaceChar) # Call the replace method to replace every new line character with the replaceChar
         return f # Return f

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

#################################################################

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

#################################################################

def findCov(mesg):
    covIndex = mesg.find('{119:')
    if (covIndex < 0):
        return [mesg, None]
    first = mesg[:(covIndex)]
    newS = mesg[covIndex:]
    covEndIndex = newS.find('}')
    second = newS[(covEndIndex + 1):]
    return [(first + second), newS[:covEndIndex + 1]]

#################################################################

def createTable(data):
    pd.options.display.precision = 18
    df = pd.DataFrame(data) # Set df equal to the return value of the DataFrame method, passing data as input
    return df # Return df


#################################################################

def createEntries(mesg, mesgEntries):
    i = 0
    inputMesg = mesg
    for i in range(4): # Parse through each of the 4 blocks
        inputMesg = parseMesg(inputMesg, mesgEntries) # Set inputMesg to the return value of parseMesg; parseMesg takes as input the most recent value of inputMesg and the dictionary to be added to
    return mesgEntries # After looping through each block, return mesgEntries

def parseMesg(mesg, mesgEntries):
    i = 0
    while (True):
        if (mesg[i].isdigit()): # If the current character is a digit
            mesg = mesg[i:] # Set mesg equal to everything after the current index
            stringInfo = findNumberAndContent(mesg, ':', '}', False) # Call findNumberAndContent, setting the return value to stringInfo
            if (stringInfo[0] == '2'): # If the block number is 2
                field2(stringInfo[1], mesgEntries) # Call field2
            elif (stringInfo[0] == '4'): # If the block number is 4
                fields = createFields(mesgEntries['MT'][0]) # Set fields equal to the result of createFields
                del mesgEntries['MT']
                mesg = specFormat4(mesg) # Do formatting on field 4 to ensure that it is in the correct format to be parsed
                return createEntries4(mesg, mesgEntries, fields) # Return mesgEntries by calling createEntries4
            mesgEntries.setdefault(stringInfo[0], []).append(stringInfo[1]) # Add the content of the current block to mesgEntries
            return stringInfo[2] # Return the rest of the SWIFT message to be parsed
        else:
            i = i + 1

def specFormat4(mesg):
    if (mesg.find('}{4:#') >= 0):
        mesg = mesg[5:]
    elif (mesg.find('4:#') >= 0):
        mesg = mesg[3:]
    return mesg

def createEntries4(mesg, mesgEntries, fields):
    i = 0
    inputMesg = [mesg, 0]
    while (len(inputMesg[0]) > 1):
       lastIndex = inputMesg[1]
       inputMesg = parse4(inputMesg[0], mesgEntries, inputMesg[1], fields) # Set inputMesg to the result of parse4
       try:
           length = len(inputMesg[0])
       except TypeError:
           if (lastIndex < len(fields)): # If lastIndex has not reached the end of fields
               for i in range(len(fields) - lastIndex): # Loop through the remaining fields to look at
                   if (i != 0):
                       mesgEntries.setdefault(fields[lastIndex + i], []).append(None) # Append None to mesgEntries
           return mesgEntries
    return mesgEntries

def parse4(mesg, mesgEntries, index, fields):
    i = 0
    n = index
    while (i < len(mesg)): # Loop through the length of mesg
        if (mesg[i] == ':'): # If the current character is equal to ':'
            mesg = mesg[(i+1):] # Set mesg equal to everything after the next character
            stringInfo = findNumberAndContent(mesg, ':', '#', True) # Set stringInfo to the result of findNumberAndContent
            while (n < len(fields)): # Loop through fields
                if (stringInfo[0] != fields[n]): # If the current field is not equal to fields[n]
                    mesgEntries.setdefault(fields[n], []).append(None) # Append None to mesgEntries
                else: # Otherwise
                    mesgEntries.setdefault(stringInfo[0], []).append(stringInfo[1]) # Append the content of the field (stringInfo[1]) to mesgEntries
                    return [stringInfo[2], n+1] # Return an array in the format of [restOfString, next index in fields]
                n = n + 1 # Increment n by 1
        else:
            i = i + 1 # Increment i by 1

def findNumberAndContent(text, midChar, endChar, four):
    index1 = text.index(midChar) # Get index of midChar
    number = text[:index1]  # Set number equal to everything before midChar
    if (number[len(number)-1] == '#'):
        number = number[:(len(number)-1)]
    content = text[(index1+2):]
    index2 = content.index(endChar) # Get the index of endChar
    restOfString = content[(index2+1):]
    content = text[:(index2+3)][(len(number)+1):]
    if (four == True): # If four == True
        content = text[(len(number)+1):]
        index2 = content.index(endChar)
        content = content[:index2]
    return [number, content, restOfString] # Return an array in the format of [number of field, content of field, rest of text to be parsed]

def field2(text, mesgEntries):
    messageType = text[1:4]
    mesgEntries.setdefault('MT', []).append(messageType)
