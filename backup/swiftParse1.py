import pandas as pd

#-------------------------------------------
def parse4(content, contentEntries):
    i = 0
    while (content[i] != '$'):
        if (content[i].isdigit()):
           content = content[i:]
           numEndIndex = content.index(':')
           entryNum = content[:numEndIndex]
           content = content[(numEndIndex + 1):]
           #print(content)
           '''
           #----------------------------
           if (entryNum  == '32A'):
               print('-----------')
               return getMoneyAndDate(content, contentEntries)
           #----------------------------
           '''
           if (int(entryNum[:2]) > 60):
               endIndex = content.index('-')
           else:
               endIndex = content.index(':')
           cText = content[:endIndex]
           contentEntries[entryNum] = [cText]
           return content[(endIndex):]
        else:
            i = i + 1

def parseMesg(mesg, mesgEntries):
    i = 0
    entryNum = 0
    while (mesg[i] != '$'):
        if (mesg[i].isdigit()):
            entryNum = mesg[i]
            mesg = mesg[i:]
            if (entryNum == '4'):
                mesg = mesg[2:]
                return createEntries4(mesg, mesgEntries)
            elif (entryNum == '2'):
                mesgEntries['Direction'] = [mesg[2]]
                mesgEntries['Message Type'] = [mesg[3:6]]
                #print(mesgEntries)
                startIndex = mesg.index(':') + 1
                content = mesg[int(startIndex):]
                tIndex = content.index('}')
                content = content[:tIndex]
                if (content[0] == '{'):
                    content = content[1:]
                mesgEntries[int(entryNum)] = [content]
                return mesg[(tIndex + 3):]
            else:
                startIndex = mesg.index(':') + 1
                content = mesg[int(startIndex):]
                tIndex = content.index('}')
                content = content[:tIndex]
                if (content[0] == '{'):
                    content = content[1:]
                #mesgEntries[int(entryNum)] = content
                mesgEntries[int(entryNum)] = [content]
                return mesg[(tIndex + 3):]
        else:
            i = i + 1

def createEntries(mesg, mesgEntries):
    i = 0
    inputMesg = mesg
    for i in range(4):
        inputMesg = parseMesg(inputMesg, mesgEntries)
    return mesgEntries

def getDirectionAndType(block2):
    print(block2[0])
    print(block2[1:4])


def getMoneyAndDate(mesg, mesgEntries):
    i = 0
    loop = True
    while (loop):
        if (mesg[i].isdigit() == False):
            year = mesg[:i]
            amount = mesg[i:]
            print(year)
            print(amount)
            return
        i = i + 1

def createEntries4(content, contentEntries):
    i = 0
    inputMesg = content
    for i in range(11):
        inputMesg = parse4(inputMesg, contentEntries)
    return contentEntries

#--------------------------------------------------------------------

def createDF(data):
    df = pd.DataFrame(data, index = [0])
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)

def mod(mesgEntries):
    mod1(mesgEntries)
    mod2(mesgEntries)
    mod32A(mesgEntries)
    mod33B(mesgEntries)

def mod1(mesgEntries):
    endIndex = mesgEntries[1].index('X')
    mesgEntries[1] = mesgEntries[1][:endIndex]

def mod2(mesgEntries):
    endIndex = mesgEntries[2].index('X')
    mesgEntries[2] = mesgEntries[2][4:]
    mesgEntries[2] = mesgEntries[2][:(endIndex - 4)]
    
def mod32A(mesgEntries):
    mesgEntries['Date A'] = (mesgEntries['32A'])[0:6]
    mesgEntries['Currency A'] = (mesgEntries['32A'])[6:9]
    mesgEntries['Amount A'] = (mesgEntries['32A'])[9:]
    mesgEntries.pop('32A')

def mod33B(mesgEntries):
    mesgEntries['Currency B'] = (mesgEntries['33B'])[0:3]
    mesgEntries['Amount B'] = (mesgEntries['33B'])[3:]
    mesgEntries.pop('33B')

'''
def mod50K(mesgEntries):

'''

