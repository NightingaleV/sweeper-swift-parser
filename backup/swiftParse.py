
# Method below takes a string (mesg) and a dictionary (mesgEntries) and adds the contents and entry number to mesgEntries
def parseMesg(mesg, mesgEntries):
    i = 0
    entryNum = 0
    while (mesg[i] != '$'):
        if (mesg[i].isdigit()):
            entryNum = mesg[i]
            mesg = mesg[i:]
            startIndex = mesg.index(':')
            startIndex = startIndex + 1
            content = mesg[int(startIndex):]
            tIndex = content.index('}')
            content = content[:tIndex]
            if (content[0] == '{'):
                content = content[1:]
            mesgEntries[int(entryNum)] = content
            return mesg[(tIndex + 3):]
        else:
            i = i + 1

def parseMesgRec(mesg, mesgEntries):
    i = 0
    n = 0
    entryNum = 0
    for n in range(4):
        if (mesg[i].isdigit()):
            entryNum = mesg[i]
            mesg = mesg[i:]
            startIndex = mesg.index(':')
            startIndex = startIndex + 1
            content = mesg[int(startIndex):]
            tIndex = content.index('}')
            content = content[:tIndex]
            if (content[0] == '{'):
                content = content[1:]
            mesgEntries[int(entryNum)] = content
            #return mesg[(tIndex + 3):]
            #parseMesgRec(mesg[(tIndex + 3):], mesgEntries)
        else:
            i = i + 1
        #n = n + 1
    return mesgEntries

# Method below takes a string (mesg) and a dictionary (mesgEntries) and calls the parseMesg function to add all entries into the dictionary
def createEntries(mesg, mesgEntries):
    two = parseMesg(mesg, mesgEntries)
    three = parseMesg(two, mesgEntries)
    four = parseMesg(three, mesgEntries)
    five = parseMesg(four, mesgEntries)
    return mesgEntries

def parse4(content, contentEntries):
    i = 0
    while (content[i] != '$'):
        if (content[i].isdigit()):
           content = content[i:]
           numEndIndex = content.index(':')
           entryNum = content[:numEndIndex]
           #print(entryNum)
           #print(content)
           content = content[(numEndIndex + 1):]
           #print(content)
           if (int(entryNum[:2]) > 60):
               endIndex = content.index('-')
           else:
               endIndex = content.index(':')
           cText = content[:endIndex]
           #print(cText)
           contentEntries[entryNum] = cText
           #print(contentEntries)
           return content[(endIndex):]
        else:
            i = i + 1

def createEntries4(content, contentEntries):
    two = parse4(content, contentEntries)
    three = parse4(two, contentEntries)
    four = parse4(three, contentEntries)
    five = parse4(four, contentEntries)
    six = parse4(five, contentEntries)
    seven = parse4(six, contentEntries)
    eight = parse4(seven, contentEntries)
    nine = parse4(eight, contentEntries)
    ten = parse4(nine, contentEntries)
    eleven = parse4(ten, contentEntries)
    twelve = parse4(eleven, contentEntries)
    return contentEntries
    

def getSender(indexOne):
    # indexOneMod is identical to indexOne, except that the first character is excluded
    indexOneMod = indexOne[1:]
    i = 0
    # Iterate through indexOneMod to find where the sender name starts
    while (indexOneMod[i].isalpha() == False):
        i = i + 1
    return indexOneMod[i:]
    


