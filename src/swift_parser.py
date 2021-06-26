import pandas as pd
import numpy as np
import csv
import sys

# allFields = pd.read_csv(r'/Users/josephfeuer/Desktop/SM.csv') # Set allFields equal to the result of the read_csv function, using the path name of the csv location
allFields = pd.read_csv(
    './resources/SM.csv', sep=';')  # Set allFields equal to the result of the read_csv function, using the path name of the csv location


#################################################################

def main(file, dataFrames):
    text = removeSpaces(file, '#')
    mesgs = parseMultMesg(text, '$')
    mesgEntries = {}
    for i in range(len(mesgs)):
        output_str = str(i) + "\n"
        sys.stdout.write(output_str)  # same as print
        sys.stdout.flush()
        mesgs[i] = findCov(mesgs[i])[0]
        createEntries(mesgs[i], mesgEntries)
        mt = mesgEntries['2'][i][1:4]
        if (mt in dataFrames):
            createEntries(mesgs[i], dataFrames[mt][0])
        else:
            dataFrames.setdefault(mt, []).append(createEntries(mesgs[i], {}))
    # return mesgEntries

    # dataFramesToWrite = []
    # for key in dataFrames:
    #     dataFramesToWrite.append(createTable(dataFrames[key][0]))
    #     #createTable(dataFrames[key]).to_csv('/Users/josephfeuer/Desktop/SwiftResults.csv', index = True, header = True)
    #     #return
    # #return dataFrames
    # return dataFramesToWrite

    return dataFrames


def modAllFields(mesgEntries):
    for key in mesgEntries:
        for i in range(len(mesgEntries[key])):
            fields = createFields(key)
            mod(mesgEntries[key][i], fields)


def confirmSize(dataFrames):
    # fieldsToDel = []
    fieldsToDel = {}
    for key in dataFrames:
        for i in range(len(dataFrames[key])):
            if (len(dataFrames[key][i]) == 1):
                # fieldsToDel.append(key)
                fieldsToDel.setdefault(key, []).append(dataFrames[key][i], {})
    # print(fieldsToDel)
    return fieldsToDel
    '''
    for i in range(len(fieldsToDel)):
        del dataFrames[fieldsToDel[i]]
    return dataFrames
    '''


def main1(file):
    text = removeSpaces(file, '#')
    mesgs = parseMultMesg(text, '$')
    mesgEntries = {}
    for i in range(len(mesgs)):
        mesgs[i] = findCov(mesgs[i])[0]
        createEntries(mesgs[i], mesgEntries)
    return mesgEntries


#################################################################

def removeSpaces(file, replaceChar):
    with open(file, "r") as infile:  # Open file in read mode
        f = infile.read()  # Set f equal to infile.read()
        f = f.replace("\n",
                      replaceChar)  # Call the replace method to replace every new line character with the replaceChar
        return f  # Return f


def parseMultMesg(mesg, delim):
    mesgs = []
    origMesg = mesg  # Set origMesg equal to mesg
    length = len(mesg)
    i = 0
    while (i < length):  # While i is less than length
        searchFor = '}' + delim + '{'  # Set searchFor equal to a string in the formaat of '}delim{'
        endIndex = (mesg.find(searchFor)) + 1  # Set endIndex equal to the index where searchFor appears
        if (mesg[:endIndex] == ''):  # If there is nothing before endIndex within mesg
            mesgs.append(mesg)  # Append mesg to mesgs
            return mesgs  # Return mesgs
        mesgs.append(mesg[:endIndex])  # Append mesg[:endIndex] to mesgss
        mesg = mesg[endIndex:]  # Set mesg equal to everything coming after endIndex
        i = i + 1  # Increment i


#################################################################

def createFields(messageType):
    mt = allFields.loc[:,
         ["MT", "Tag"]]  # Use the loc function to set mt equal to the "MT" and "Tag" columns of allFields
    m103 = mt.loc[mt['MT'] == messageType, [
        'Tag']]  # Use the loc function to set m103 to thee dataframe containing 'MT' where messageType equals mt['MT'] and 'Tag'
    fields = []
    m103D = m103.to_dict()  # set m103D to the dictionary version of the dataframee m103
    data = list(m103D['Tag'].items())  # Set data equal to list of 'Tag' entries
    mArray = np.array(data)  # Set mArray equal to the result of the array method, passing data in as input
    fieldsT = []
    for i in range(len(mArray)):  # Loop through the length of mArray
        fieldsT.append(mArray[i][1])  # Append mArray[i][1] to fieldsT
    return fieldsT  # Return fieldsT


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
    df = pd.DataFrame(data)  # Set df equal to the return value of the DataFrame method, passing data as input
    return df  # Return df


#################################################################

def createEntries(mesg, mesgEntries):
    i = 0
    inputMesg = mesg
    for i in range(4):  # Parse through each of the 4 blocks
        inputMesg = parseMesg(inputMesg,
                              mesgEntries)  # Set inputMesg to the return value of parseMesg; parseMesg takes as input the most recent value of inputMesg and the dictionary to be added to
    return mesgEntries  # After looping through each block, return mesgEntries


def parseMesg(mesg, mesgEntries):
    i = 0
    while (True):
        if (mesg[i].isdigit()):  # If the current character is a digit
            mesg = mesg[i:]  # Set mesg equal to everything after the current index
            stringInfo = findNumberAndContent(mesg, ':', '}',
                                              False)  # Call findNumberAndContent, setting the return value to stringInfo
            if (stringInfo[0] == '2'):  # If the block number is 2
                field2(stringInfo[1], mesgEntries)  # Call field2
            elif (stringInfo[0] == '3'):
                field3(stringInfo[1], mesgEntries)
            elif (stringInfo[0] == '4'):  # If the block number is 4
                fields = createFields(mesgEntries['MT'][0])  # Set fields equal to the result of createFields
                # del mesgEntries['MT']
                mesg = specFormat4(
                    mesg)  # Do formatting on field 4 to ensure that it is in the correct format to be parsed
                return createEntries4(mesg, mesgEntries, fields)  # Return mesgEntries by calling createEntries4
            mesgEntries.setdefault(stringInfo[0], []).append(
                stringInfo[1])  # Add the content of the current block to mesgEntries
            return stringInfo[2]  # Return the rest of the SWIFT message to be parsed
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
        inputMesg = parse4(inputMesg[0], mesgEntries, inputMesg[1], fields)  # Set inputMesg to the result of parse4
        try:
            length = len(inputMesg[0])
        except TypeError:
            if (lastIndex < len(fields)):  # If lastIndex has not reached the end of fields
                for i in range(len(fields) - lastIndex):  # Loop through the remaining fields to look at
                    if (i != 0):
                        mesgEntries.setdefault(fields[lastIndex + i], []).append(None)  # Append None to mesgEntries
            return mesgEntries
    return mesgEntries


def parse4(mesg, mesgEntries, index, fields):
    i = 0
    n = index
    while (i < len(mesg)):  # Loop through the length of mesg
        if (mesg[i] == ':'):  # If the current character is equal to ':'
            mesg = mesg[(i + 1):]  # Set mesg equal to everything after the next character
            stringInfo = findNumberAndContent(mesg, ':', '#',
                                              True)  # Set stringInfo to the result of findNumberAndContent
            while (n < len(fields)):  # Loop through fields
                if (stringInfo[0] != fields[n]):  # If the current field is not equal to fields[n]
                    mesgEntries.setdefault(fields[n], []).append(None)  # Append None to mesgEntries
                else:  # Otherwise
                    mesgEntries.setdefault(stringInfo[0], []).append(
                        stringInfo[1])  # Append the content of the field (stringInfo[1]) to mesgEntries
                    return [stringInfo[2],
                            n + 1]  # Return an array in the format of [restOfString, next index in fields]
                n = n + 1  # Increment n by 1
        else:
            i = i + 1  # Increment i by 1


def findNumberAndContent(text, midChar, endChar, four):
    index1 = text.index(midChar)  # Get index of midChar
    number = text[:index1]  # Set number equal to everything before midChar
    if (number[len(number) - 1] == '#'):
        number = number[:(len(number) - 1)]
    content = text[(index1 + 2):]
    index2 = content.index(endChar)  # Get the index of endChar
    restOfString = content[(index2 + 1):]
    content = text[:(index2 + 3)][(len(number) + 1):]
    if (four == True):  # If four == True
        content = text[(len(number) + 1):]
        index2 = content.index(endChar)
        content = content[:index2]
    return [number, content,
            restOfString]  # Return an array in the format of [number of field, content of field, rest of text to be parsed]


def field2(text, mesgEntries):
    messageType = text[1:4]
    endIndex = text.find('XXXX')
    mesgEntries.setdefault('Direction', []).append(text[:1])
    mesgEntries.setdefault('MT', []).append(messageType)
    mesgEntries.setdefault('Rest of 2', []).append(text[4:endIndex])


def field3(text, mesgEntries):
    begIndex = text.find(':')
    mesgEntries.setdefault('Transaction ID', []).append(text[(begIndex + 1):])


#############

def createTable(data):
    pd.options.display.precision = 18
    df = pd.DataFrame(data)  # Set df equal to the return value of the DataFrame method, passing data as input
    return df  # Return df

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


###########################################################################
###########################################################################
###########################################################################

# Parsing functions that can be applied to dictionary

fieldsP = {'50A': ['50A-Account', '50A-Identifier Code', 0],
           '50K': ['50K-Account', '50k-Line 1', '50K-Line 2', '50k-Line 3', '50K-Line 4', '50K-Line 5', 0],
           '50F': ['50F-Party Identifier', '50F-Line 1', '50F-Line 2', '50F-Line 3', '50F-Line 4', '50F-Line 5',
                   '50F-Line 6', '50F-Line 7', '50F-Line 8', ],
           '51A': ['51A-Account', '51A-Identifier Code', 0],
           '52A': ['52A-Account', '52A-Identifier Code', 0],
           '52D': ['52D-Account', '52D-Line 1', '52D-Line 2', '52D-Line 3', '52D-Line 4', '52D-Line 5', 0],
           '53A': ['53A-Account', '53A-Identifier Code', 1], '53B': ['53B-Party Identifier', '53B-Location'],
           '53D': ['53D-Account', '53D-Line 1', '53D-Line 2', '53D-Line 3', '53D-Line 4', '53D-Line 5', 0],
           '54A': ['54A-Account', '54A-Identifier Code', 1], '54B': ['54B-Party Identifier', '54B-Location'],
           '54D': ['54D-Account', '54D-Line 1', '54D-Line 2', '54D-Line 3', '54D-Line 4', '54D-Line 5', 0],
           '55A': ['55A-Account', '55A-Identifier Code', 1], '55B': ['55B-Party Identifier', '55B-Location'],
           '55D': ['55D-Account', '55D-Line 1', '55D-Line 2', '55D-Line 3', '55D-Line 4', '55D-Line 5', 0],
           '56A': ['56A-National Clearing System Code', '56A-Party Identifier', '56A-Identifier Code'],
           '55B': ['55B-Party Identifier', '55B-Location', 0],
           '57A': ['57A-National Clearing System Code', '57A-Party Identifier', '57A-Identifier Code'],
           '59': ['59-Account', '59-Line 1', '59-Line 2', '59-Line 3', '59-Line 4', '59-Line 5', 0],
           '59A': ['59A-Account', '59A-Identifier Code', 0],
           '59F': ['59F-Party Identifier', '59F-Line 1', '59F-Line 2', '59F-Line 3', '59F-Line 4', '59F-Line 5',
                   '59F-Line 6', '59F-Line 7', '59F-Line 8', ]}


def mod(mesgEntries, fields):
    for i in range(len(mesgEntries)):
        if (fields[i] in fieldsP):
            for n in range(len(mesgEntries[fields[i]])):
                # print(mesgEntries[fields[i]][n])
                if (mesgEntries[fields[i]][n] == None):
                    pass
                elif ((fields[i][2] == 'A') or (fields[i] == '59')):
                    parseA(mesgEntries, n, fields[i])
                elif (fields[i][2] == 'F'):
                    parseF(mesgEntries, n, fields[i])
                elif (fields[i][2] == 'D'):
                    parseF(mesgEntries, n, fields[i])
        else:
            if (fields[i] == '32A'):
                for n in range(len(mesgEntries[fields[i]])):
                    if (mesgEntries[fields[i]][n] == None):
                        pass
                    else:
                        mod32A(mesgEntries, n)
            elif (fields[i] == '33B'):
                for n in range(len(mesgEntries[fields[i]])):
                    if (mesgEntries[fields[i]][n] == None):
                        pass
                    else:
                        mod33B(mesgEntries, n)


def mod32A(mesgEntries, n):
    mesgEntries.setdefault('32A-Date', []).append((mesgEntries['32A'])[n][0:6])
    mesgEntries.setdefault('32A-Currency', []).append((mesgEntries['32A'])[n][6:9])
    mesgEntries.setdefault('32A-Amount', []).append(mesgEntries['32A'][n][9:])


def mod33B(mesgEntries, n):
    if (mesgEntries['33B'][n] == None):
        mesgEntries.setdefault('33B-Currency', []).append(None)
        mesgEntries.setdefault('33B-Amount', []).append(None)
    else:
        mesgEntries.setdefault('33B-Currency', []).append((mesgEntries['33B'])[n][0:3])
        mesgEntries.setdefault('33B-Amount', []).append(mesgEntries['33B'][n][3:])


'''
Works for fields 50A, 51A, 52A, 53A, 54A, 55A, 559
Also works for 55B
'''


def parseA(mesgEntries, n, field):
    onlySlash = 0
    length = len(fieldsP[field])
    if (str(fieldsP[field][len(fieldsP[field]) - 1]).isdigit()):
        slashIndex = fieldsP[field][len(fieldsP[field]) - 1]
    for i in range(length):
        if (i == 0):
            print(mesgEntries[field][n])
            first = (mesgEntries[field])[n].find('/')
            if (first < 0):
                mesgEntries.setdefault(fieldsP[field][i], []).append(None)
                new = mesgEntries[field][n]
                onlySlash = 1
            else:
                new = (mesgEntries[field][n])[(first + 1):]
        elif (i == (length - 2)):
            mesgEntries.setdefault(fieldsP[field][i], []).append(new)
            return mesgEntries
        second = new.find('#')
        if (second < 0):
            mesgEntries.setdefault(fieldsP[field][i + 1], []).append(new)
            for n in range(length - i - 3):
                mesgEntries.setdefault(fieldsP[field][i + n + 1], []).append(None)
            return mesgEntries
        if (onlySlash == 1):
            pass
        else:
            mesgEntries.setdefault(fieldsP[field][i], []).append(new[:second])
        new = new[(second + 1):]


'''
Works for fields 50F, 59F
'''


def parseF(mesgEntries, n, field):
    fields = fieldsP[field]
    result = {}
    for i in range(len(fields)):
        if (i == 0):
            result = getNumField(mesgEntries[field][n], '/', '#', False)
            mesgEntries.setdefault(fieldsP[field][i], []).append(result[0])
            result = result[1]
        else:
            result = getNumField(result, '/', '#', True)
            if (int(result[0]) == i):
                mesgEntries.setdefault(fieldsP[field][i], []).append(result[1])
                result = result[2]
            else:
                mesgEntries.setdefault(fieldsP[field][i], []).append(None)
                result = '#' + result[0] + '/' + result[1] + result[2]
    return mesgEntries


def parseD(mesgEntries, n, field):
    content = mesgEntries[field][n]
    fields = fieldsP[field]
    result = {}
    if (content.find('/') == 0):
        try:
            parseF(mesgEntries, n, field)
        except ValueError:
            return mesgEntries
    else:
        result = getNumField(content, '/', '#', True)
        for i in range(len(fields)):
            if (i == 0):
                mesgEntries.setdefault(fieldsP[field][i], []).append(None)
            else:
                if (int(result[0]) == i):
                    mesgEntries.setdefault(fieldsP[field][i], []).append(result[1])
                    result = result[2]
                else:
                    mesgEntries.setdefault(fieldsP[field][i], []).append(None)
                    result = '#' + result[0] + '/' + result[1] + result[2]
                result = getNumField(result, '/', '#', True)
                try:
                    if (int(result[0]) == 1):
                        pass
                except ValueError:
                    return mesgEntries


# also should work for 57C
def parse56A(mesgEntries, n, field):
    content = mesgEntries[field][n]
    if (content.find('//') != 0):
        mesgEntries.setdefault(fieldsP[field][0], []).append(None)
        if (content[0] == '/'):
            mesgEntries.setdefault(fieldsP[field][1], []).append(content[1:])
            mesgEntries.setdefault(fieldsP[field][2], []).append(None)
        else:
            mesgEntries.setdefault(fieldsP[field][1], []).append(None)
            mesgEntries.setdefault(fieldsP[field][2], []).append(content)
    else:
        content = content[1:]
        result = getNumField(content, '/', '#', False)
        mesgEntries.setdefault(fieldsP[field][0], []).append(result[0])
        print(result[1])
        if (result[1][1] == '/'):
            mesgEntries.setdefault(fieldsP[field][1], []).append(result[1][2:])
            mesgEntries.setdefault(fieldsP[field][2], []).append(None)
        else:
            mesgEntries.setdefault(fieldsP[field][1], []).append(None)
            mesgEntries.setdefault(fieldsP[field][2], []).append(result[1][1:])


def getNumField(mesg, begChar, endChar, numExists):
    begCharIndex = mesg.find(begChar)
    number = ''
    if (numExists == True):
        number = mesg[1:begCharIndex]
    mesg = mesg[(begCharIndex + 1):]
    endCharIndex = mesg.find(endChar)
    if ((endCharIndex < 0) and (numExists == True)):
        return [number, mesg, '']
    elif ((endCharIndex < 0) and (numExists == False)):
        return [mesg, '']
    elif (numExists == True):
        return [number, mesg[:endCharIndex], mesg[endCharIndex:]]
    return [mesg[:endCharIndex], mesg[endCharIndex:]]
