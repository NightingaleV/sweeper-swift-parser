import pandas as pd

fields = ['13C', '20', '23B', '23E', '26T', '32A', '33B', '36', '50A', '50F', '50K', '51A', '52A', '52D', '53A', '53B', '53D', '54A', '54B', '54D', '55A', '55B', '55D', '56A', '56C', '56D', '57A', '57B', '57C', '57D', '59', '59A', '59F', '70', '71A', '71F', '71G', '72', '77B']

mesgEntries = {}

for i in range(len(fields)):
    mesgEntries.setdefault(fields[i], [])

def main(text):
    mesgs = parseMultMesg(text, '$')
    contentEntries = {}
    createEntries(mesgs[0], contentEntries)
    createEntries(mesgs[1], contentEntries)
    createEntries(mesgs[2], contentEntries)
    createEntries(mesgs[3], contentEntries)
    return contentEntries


'''
parseMultMesg takes a string (mesg) as input that signifies a string of many SWIFT messages together.
The delim parameter signifies the character that sepearates SWIFT messages from each other (e.g. '$').
When executed, this function will return an array where each index holds an individual SWIFT message.
'''
def parseMultMesg(mesg, delim):
    mesgs = []
    origMesg = mesg
    length = len(mesg)
    i = 0
    while (i < length):
        searchFor = '}' + delim + '{'
        endIndex = (mesg.find(searchFor)) + 1
        if (mesg[:endIndex] == ''):
            mesgs.append(mesg)
            return mesgs
        mesgs.append(mesg[:endIndex])
        mesg = mesg[endIndex:]
        i = i + 1

#------------------------------------------------

'''
createEntries takes as input a SWIFT message (mesg) and a dictionary (mesgEntries).
The function will return a filled version of mesgEntries, which will hold each index and the content of that index
'''
def createEntries(mesg, mesgEntries):
    i = 0
    inputMesg = mesg
    for i in range(4):
        inputMesg = parseMesg(inputMesg, mesgEntries)
    return mesgEntries

'''

'''
def parseMesg(mesg, mesgEntries):
    i = 0
    entryNum = 0
    while (True):
        if (mesg[i].isdigit()):
            entryNum = mesg[i]
            mesg = mesg[i:]
            if (entryNum == '4'):
                mesg = mesg[2:]
                return createEntries4M(mesg, mesgEntries)
            else:
                startIndex = mesg.index(':') + 1
                content = mesg[int(startIndex):]
                tIndex = content.index('}')
                content = content[:tIndex]
                if (content[0] == '{'):
                    content = content[1:]
                mesgEntries.setdefault(int(entryNum), []).append(content)
                return mesg[(tIndex + 3):]
        else:
            i = i + 1

def createEntries4M(content, contentEntries):
    i = 0
    inputMesg = [content, 0]
    while (len(inputMesg[0]) > 1):
       lastIndex = inputMesg[1]
       inputMesg = parse4M(inputMesg[0], contentEntries, inputMesg[1])
       try:
           length = len(inputMesg[0])
       except TypeError:
           print(lastIndex)
           if (lastIndex < len(fields)):
               for i in range(len(fields) - lastIndex):
                   if (i != 0):
                       contentEntries.setdefault(fields[lastIndex + i], []).append(None)
           return contentEntries
    '''
    if (inputMesg[1] < len(fields)):
        for i in range(len(fields) - inputMesg[1]):
            if (i != 0):
                contentEntries.setdefault(fields[inputMesg[1] + i], []).append(None)
    '''
    return contentEntries

def parse4M(content, contentEntries, index):
    i = 0
    if (index == 0):
        n = index
    else:
        n = index + 1
    while (i < len(content)):
        if (content[i].isdigit()):
            content = content[i:]
            numEndIndex = content.index(':')
            entryNum = content[:numEndIndex]
            content = content[(numEndIndex + 1):]
            if (int(entryNum[:2]) > 60):
                endIndex = 0
                try:
                    endIndex = content.index(':')
                except ValueError:
                    endIndex = content.index('-')
                cText = content[:endIndex]
            else:
                endIndex = content.index(':')
                cText = content[:endIndex]
            while (n < len(fields)):
                if (entryNum != fields[n]):
                    contentEntries.setdefault(fields[n], []).append(None)
                else:
                    contentEntries.setdefault(entryNum, []).append(cText)
                    result = [content[(endIndex):], n]
                    return [content[(endIndex):], n]
                n = n + 1
        else:
            i = i + 1


#-------------

def mod(mesgEntries):
    for i in range(len(mesgEntries)):
        if (i < 3):
            for n in range(len(mesgEntries[i+1])):
                if (i == 0):
                    mesgEntries[i+1][n] = mod1(mesgEntries[i+1][n])
                elif  (i == 1):
                    mesgEntries.setdefault('Direction', []).append(mesgEntries[i+1][n][0])
                    mesgEntries.setdefault('Message Type', []).append(mesgEntries[i+1][n][1:4])
                    mesgEntries[i+1][n] = mod2(mesgEntries[i+1][n])
                elif (i == 2):
                    mesgEntries[i+1][n] = mesgEntries[i+1][n][4:]
        '''
        else:
            for n in range(len(fields)):
                if (fields[n] == '32A'):
                    print(fields[n])
                    print('test')
                    #mod32A(mesgEntries)
        '''

def mod1(content):
    endIndex = content.index('X')
    return content[:endIndex]
    

def mod2(content):
    endIndex = content.index('X')
    content = content[4:]
    content = content[:(endIndex - 4)]
    return content
    
def mod32A(mesgEntries):
    mesgEntries.setdefault('Date A', []).append((mesgEntries['32A'])[0:6])
    mesgEntries.setdefault('Currency A', []).append((mesgEntries['32A'])[6:9])
    mesgEntries.setdefault('Amount A', []).append(mesgEntries['32A'][9:])

def mod33B(mesgEntries):
    mesgEntries['Currency B'] = (mesgEntries['33B'])[0:3]
    mesgEntries['Amount B'] = (mesgEntries['33B'])[3:]
    mesgEntries.pop('33B')


#-------------

def createTable(data):
    pd.options.display.precision = 18
    df = pd.DataFrame(data)
    return df

def transpose(table, mesgEntries, index):
    arr1 = []
    arr2 = []
    arr3 = []
    for key, value in table.iteritems():
        arr1.append(key)
        arr2.append(value[index])
        #arr3.append(mesgEntries[3][index][4:])
        arr3.append(mesgEntries[3][index][4:18])
    return {'TID': arr3, 'Field Name': arr1, 'Content': arr2}

def createDF(data):
    df = pd.DataFrame(data, index = [0])
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)

