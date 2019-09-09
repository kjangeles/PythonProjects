import random
from random import randint


#each space will be stored as a node
#node will be assigned row, column, and section when created
class Node:
    def __init__(self, row = None, column = None, sec = None):
        self.gValue = 0 #generated value 
        self.pValue = 0 #player viewed value
        self.row = row  #row address
        self.column = column  #column address
        self.section = sec    #section assignment (based on [row][column] address)
        self.locked = False   #space is locked if revealed at beginning of play
        self.solved = False   #node is solved if pValue == gValue


#populate puzzle matrix with nodes
puzzleMatrix = []
# i is for row
for i in range(0,9):
    rowList = []
    # j is for column, column locations are stored in row
    for j in range(0,9):
        # section assignment
        if (i in range(0, 3) and j in range(0, 3)):
            sec = 0
        elif (i in range(0, 3) and j in range(3, 6)):
            sec = 1
        elif (i in range(0, 3) and j in range(6, 9)):
            sec = 2
        elif (i in range(3, 6) and j in range(0, 3)):
            sec = 3
        elif (i in range(3, 6) and j in range(3, 6)):
            sec = 4
        elif (i in range(3, 6) and j in range(6, 9)):
            sec = 5
        elif (i in range(6, 9) and j in range(0, 3)):
            sec = 6
        elif (i in range(6, 9) and j in range(3, 6)):
            sec = 7
        else:
            sec = 8
        node = Node(i, j, sec)
        rowList.append(node)
    puzzleMatrix.append(rowList)

#randomly generates 7 sections
# selects a section, finds a space within section, assigns valid value (one without conflict)
# if the script encounters a space that cannot hold any value without conflict
# the section is cleared and re-filled
# if the section is cleared 10 times, it will move to an adjacent section,
#   clear and refill the adj section, then move back to original section
# Works
def method1(section, puzMat):
    f = 0
    retry = 0                           #if clearSec 10 times, move to redo adjacent section
    rowRange = rLimit(section, puzMat)  #row and column bounds set for section
    colRange = cLimit(section, puzMat)
    secValues = [1, 2, 3, 4, 5, 6, 7, 8, 9]     #values not occupying section
    while (f < 9):
        r = randint(rowRange[0], rowRange[1])   #choose random space in section
        c = randint(colRange[0], colRange[1])
        if (puzMat[r][c].gValue == 0):          #proceed if space has not been assigned a value
            inR = True          #conflict checks
            inC = True
            inS = False
            reject = [1, 2, 3, 4, 5, 6, 7, 8, 9]    #if a number is conflicted out, remove from possible selection
            while (inR == True or inC == True or inS == False):
                try:                                #if 'reject' is empty, section needs to be cleared for retry
                    v = random.choice(reject)
                except:
                    f = -1
                    break
                vIndex = reject.index(v)
                del reject[vIndex]          #

                #find conflicts in column, row, or section
                i = 0
                while (i < 9):
                    if (puzMat[i][c].gValue == v):
                        inC = True
                        break
                    elif (puzMat[r][i].gValue == v):
                        inR = True
                        break
                    else:
                        inC = False
                        inR = False
                        i += 1
                inS = v in secValues
            # if a value found for space, continue placing, loop until all spaces filled in section
            if (f >= 0):
                puzMat[r][c].gValue = v
                try:
                    vIndex = secValues.index(v)
                    del secValues[vIndex]
                except:
                    pass
                f += 1

            # conflict with all values in a space, reset section
            else:
                f = 0
                puzMat = clearSec(puzMat, rowRange, colRange)
                secValues = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                retry += 1
                
                # if fill failed 10 times, move to adjacent section
                if (retry == 10):
                    if (section == 0):
                        mov = 1
                    elif (section == 1):
                        mov = 2
                    elif (section == 2):
                        mov = 5
                    elif (section == 3):
                        mov = 4
                    elif (section == 4):
                        mov = 5
                    elif (section == 5):
                        mov = 8
                    elif (section == 6):
                        mov = 3
                    elif (section == 7):
                        mov = 6
                    elif (section == 8):
                        mov = 7
                    rowRange2 = rLimit(mov, puzMat)
                    colRange2 = cLimit(mov, puzMat)
                    puzMat = clearSec(puzMat, rowRange2, colRange2)
                    method1(mov, puzMat)
                    retry = 0

# function to clear a section
# used if space in a section has no valid options
# gives script another chance to fill the section
#   in a way that is compatable with all values
#part of method1
def clearSec(puzMat, rowRange, colRange):
    i = rowRange[0]
    j = colRange[0]
    while (i <= rowRange[1]):
        while (j <= colRange[1]):
            puzMat[i][j].gValue = 0
            j += 1
        j = colRange[0]
        i += 1
    return puzMat

# method to fill last 2 sections
# Finds all valid values for each space in remaining 2 sections
# asigns priority to space with least amount of options
# fills that space with accepted value
# moves to other section and fills appropriate space with value
# repeat until all spaces filled 
# ALMOST WORKING, haven't found where error occurs, but errors in the following ways:
#   see finalPlace function comment on lines 225 and 226; infinite loop
#   "completes" puzzle, but fails to assign values to some spaces

# Does occasionally make a complete puzzle that would be useable
# I'm going to continue testing and try to figure it out.
def method2(section1, section2, puzMat):
    #row and column bounds set for section
    rowRange1 = rLimit(section1, puzMat)  # section 4 - row no.3,4,5
    rowRange2 = rLimit(section2, puzMat)  # section 7 -  row no. 6,5,8
    colRange = cLimit(section1, puzMat)   # section 1 - col no. 3,4,5
    i = rowRange1[0]

    #dictionary, translates priorityList to space address in puzzle matrix
    spaceDict = {0 : puzMat[i][colRange[0]], 1 : puzMat[i][colRange[0]+1], 2: puzMat[i][colRange[1]], 3 : puzMat[i+1][colRange[0]], 4 : puzMat[i+1][colRange[0+1]+1], 5: puzMat[i+1][colRange[1]], 
    6 : puzMat[i+2][colRange[0]], 7 : puzMat[i+2][colRange[0]+1], 8: puzMat[i+2][colRange[1]], 9 : puzMat[i+3][colRange[0]], 10 : puzMat[i+3][colRange[0+1]+1], 11: puzMat[i+3][colRange[1]], 
    12 : puzMat[i+4][colRange[0]], 13 : puzMat[i+4][colRange[0]+1], 14: puzMat[i+4][colRange[1]], 15 : puzMat[i+5][colRange[0]], 16 : puzMat[i+5][colRange[0+1]+1], 17: puzMat[i+5][colRange[1]]}
    
    #record acceptable values for each space
    #re-checks after each new placement
    f = 0
    while (f < 9):
        i = rowRange1[0]
        priorityLists = []
        while (i <= rowRange2[1]):
            j = colRange[0]
            while (j <= colRange[1]):
                values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                priorityLists.append(conCheck(puzMat[i][j], values, puzMat))
                j += 1
            i += 1
        #assigns prioirty to the space with fewest acceptable values
        #usually priority spaces will have 1 value, but accounts for when such a space doesn't exist
        index = 99
        for x in priorityLists:
            length = len(x)
            if (length == 1):
                index = priorityLists.index(x)
                break
        if (index == 99):
            for x in priorityLists:
                length = len(x)
                if (length > 0):
                    index = priorityLists.index(x)
                    break
        
        #space and value found, assigned
        spaceDict[index].gValue = priorityLists[index][0]

        #goes to other section and places last instance of value
        if (index < 9):
            finalPlace(spaceDict[index].gValue, puzMat, rowRange2, colRange)
        else:
            finalPlace(spaceDict[index].gValue, puzMat, rowRange1, colRange)

        f += 1
        
#Places last instance of specific value
#i.e. 8 sections have this value, place the last one in final section
#part of method 2
#might need tweeked, might be part of the error
def finalPlace(value, puzMat, rowRange, colRange):
    #select space
    rowLoc = 0
    colLoc = 0
    r = rowRange[0]
    #ERROR: on occasion, r will exceed bounderies, and rowLoc & colLock still == 0
    #gets stuck looping lines 225 and 226
    while (rowLoc == 0 or colLoc == 0):
        while (r <= rowRange[1]):
            c = colRange[0]
            while (c <= colRange[1]):
                #check for conflict with value
                inR = False
                inC = False

                if (colLoc == 0):
                    i = 0
                    while (inC == False and i < 9):
                        while (i < 9):
                            if (puzMat[i][c].gValue == value):
                                inC = True
                                break
                            else:
                                i += 1

                    if (i == 9 and inC == False):
                        colLoc = c
       
                #move row check to outer loop?
                if (rowLoc == 0):
                    i = 0
                    while (inR == False and i < 9):
                        while (i < 9):
                            if (puzMat[r][i].gValue == value):
                                inR = True
                                break
                            else:
                                i += 1

                    if (i == 9 and inR == False):
                        rowLoc = r
                if (rowLoc != 0 and colLoc != 0):
                    break
                c += 1
            r += 1
    puzMat[rowLoc][colLoc].gValue = value

#check for conflicts at space
#return list of values that are acceptable
#part of method 2
def conCheck(Node, values, puzMat):
    j = 0
    pList = []
    if (Node.gValue == 0):
        while (j < 9):
            if (puzMat[Node.row][j].gValue == 0):
                j += 1
            else:
                pList.append(puzMat[Node.row][j].gValue)
                j += 1

        j = 0
        while (j < 9):
            if (puzMat[j][Node.column].gValue == 0):
                j += 1
            else:
                pList.append(puzMat[j][Node.column].gValue)
                j += 1

        for i in pList:
            try:
                iIndex = values.index(i)
                del values[iIndex]
            except:
                pass
    else:
        return []
    return values

#finds row limit for method 2
def rLimit(section, puzMat):
    rows = []
    for i in puzMat:
        for j in i:
            if j.section == section:
                rows.append(j.row)
    limits = [min(rows), max(rows)]
    return limits          
#finds column limit for method 2
def cLimit(section, puzMat):
    cols = []
    for i in puzMat:
        for j in i:
            if j.section == section:
                cols.append(j.column)
    limits = [min(cols), max(cols)]
    return limits 

#main {
seq = [0, 1, 2]
x = len(seq)
while (x > 0):
    a = random.choice(seq)
    aIndex = seq.index(a)
    del seq[aIndex]
    method1(a, puzzleMatrix)
    x -= 1


seq = [3, 6]
x = len(seq)
while (x > 0):
    a = random.choice(seq)
    aIndex = seq.index(a)
    del seq[aIndex]
    method1(a, puzzleMatrix)
    x -= 1


seq1 = [5, 8]

x = len(seq1)
while (x > 0):
    a = random.choice(seq1)
    aIndex = seq1.index(a)
    del seq1[aIndex]
    method1(a, puzzleMatrix)
    x -= 1

method2(4, 7, puzzleMatrix)
# }

#print for testing purpose
for i in puzzleMatrix:
    for j in i:
        print(j.gValue, end = ' ')
    print()
print()

