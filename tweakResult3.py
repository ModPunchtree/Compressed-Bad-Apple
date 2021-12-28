
# import raw data

# bestError = 155559
# import best data

# create backup of best data

# iteration = 0

# while true
    # choose random unique macro pixel
    # for pixel in macro pixel:
        # check if it has neighbours of opposite type
        # save index if true to list
    # random.choice(list) - toggle this pixel
    
    # for all raw macro pixels:
        # calculate difference
        # set min to bestMacroPixelIndexes
    
    # calculate real error
    
    # if real error < best error:
        # bestError = error
        # save file
        # iteration = 0
    # else:
        # iteration += 1
        # restore bestUniqueMacroPixels

import random

def readRawData() -> tuple:
    f = open("fullRawMacroPixels.txt", "r")
    uniqueMacroPixels, macroPixelIndexes = f.readlines()
    f.close()
    uniqueMacroPixels = eval(uniqueMacroPixels)
    macroPixelIndexes = eval(macroPixelIndexes)
    return uniqueMacroPixels, macroPixelIndexes

def difference(macroPixelOne: list, macroPixelTwo: list) -> int:
    #if random.randrange(0, 2) == 1:
    #    macroPixelOne, macroPixelTwo = macroPixelTwo, macroPixelOne
    delta = 0
    sum1 = 0
    sum2 = 0
    for microX in range(4):
        sum1 += sum(macroPixelOne[microX])
        sum2 += sum(macroPixelTwo[microX])
        for microY in range(8):
            if macroPixelOne[microX][microY] != macroPixelTwo[microX][microY]:
                """differentNeighbours = 17
                if (microX - 1 >= 0) and (microY - 1 >= 0):
                    if macroPixelOne[microX][microY] == macroPixelTwo[microX - 1][microY - 1]:
                        differentNeighbours -= 2
                else:
                    differentNeighbours -= 1
                if (microX - 1 >= 0):
                    if macroPixelOne[microX][microY] == macroPixelTwo[microX - 1][microY]:
                        differentNeighbours -= 2
                else:
                    differentNeighbours -= 1
                if (microX - 1 >= 0) and (microY + 1 < 8):
                    if macroPixelOne[microX][microY] == macroPixelTwo[microX - 1][microY + 1]:
                        differentNeighbours -= 2
                else:
                    differentNeighbours -= 1
                if (microY - 1 >= 0):
                    if macroPixelOne[microX][microY] == macroPixelTwo[microX][microY - 1]:
                        differentNeighbours -= 2
                else:
                    differentNeighbours -= 1
                if (microY + 1 < 8):
                    if macroPixelOne[microX][microY] == macroPixelTwo[microX][microY + 1]:
                        differentNeighbours -= 2
                else:
                    differentNeighbours -= 1
                if (microX + 1 < 4) and (microY - 1 >= 0):
                    if macroPixelOne[microX][microY] == macroPixelTwo[microX + 1][microY - 1]:
                        differentNeighbours -= 2
                else:
                    differentNeighbours -= 1
                if (microX + 1 < 4):
                    if macroPixelOne[microX][microY] == macroPixelTwo[microX + 1][microY]:
                        differentNeighbours -= 2
                else:
                    differentNeighbours -= 1
                if (microX + 1 < 4) and (microY + 1 < 8):
                    if macroPixelOne[microX][microY] == macroPixelTwo[microX + 1][microY + 1]:
                        differentNeighbours -= 2
                else:
                    differentNeighbours -= 1
                delta += differentNeighbours"""
                delta += 1
    
    delta += abs(sum1 - sum2)
  
    return delta

def realError(macroPixelIndexes: list, uniqueMacroPixels: list) -> int:
    #rawUniqueMacroPixels, rawMacroPixelIndexes = readRawData()
    error = 0
    for frameNumber in range(416):
        rawData = [[0 for j in range(24)] for i in range(32)]
        data = [[0 for j in range(24)] for i in range(32)]
        for macroY in range(3):
            for microY in range(8):
                for macroX in range(8):
                    for microX in range(4):
                        X = macroX * 4 + microX
                        Y = macroY * 8 + microY
                        rawData[X][Y] = rawUniqueMacroPixels[rawMacroPixelIndexes[frameNumber][macroX][macroY]][microX][microY]
                        data[X][Y] = uniqueMacroPixels[macroPixelIndexes[frameNumber][macroX][macroY]][microX][microY]
        
        for X in range(32):
            for Y in range(24):
                if rawData[X][Y] != data[X][Y]:
                    """differentNeighbours = 17
                    if (X - 1 >= 0) and (Y - 1 >= 0):
                        if rawData[X][Y] == data[X - 1][Y - 1]:
                            differentNeighbours -= 2
                    else:
                        differentNeighbours -= 1
                    if (X - 1 >= 0):
                        if rawData[X][Y] == data[X - 1][Y]:
                            differentNeighbours -= 2
                    else:
                        differentNeighbours -= 1
                    if (X - 1 >= 0) and (Y + 1 < 24):
                        if rawData[X][Y] == data[X - 1][Y + 1]:
                            differentNeighbours -= 2
                    else:
                        differentNeighbours -= 1
                    if (Y - 1 >= 0):
                        if rawData[X][Y] == data[X][Y - 1]:
                            differentNeighbours -= 2
                    else:
                        differentNeighbours -= 1
                    if (Y + 1 < 24):
                        if rawData[X][Y] == data[X][Y + 1]:
                            differentNeighbours -= 2
                    else:
                        differentNeighbours -= 1
                    if (X + 1 < 32) and (Y - 1 >= 0):
                        if rawData[X][Y] == data[X + 1][Y - 1]:
                            differentNeighbours -= 2
                    else:
                        differentNeighbours -= 1
                    if (X + 1 < 32):
                        if rawData[X][Y] == data[X + 1][Y]:
                            differentNeighbours -= 2
                    else:
                        differentNeighbours -= 1
                    if (X + 1 < 32) and (Y + 1 < 24):
                        if rawData[X][Y] == data[X + 1][Y + 1]:
                            differentNeighbours -= 2
                    else:
                        differentNeighbours -= 1
                    error += differentNeighbours"""
                    error += 1
    
    return error

global rawUniqueMacroPixels
global rawMacroPixelIndexes
rawUniqueMacroPixels, rawMacroPixelIndexes = readRawData()

bestError = 12671
f = open(f"64_ERROR_{bestError}_Bad_Apple.txt", "r")
bestUniqueMacroPixels, bestMacroPixelIndexes = f.readlines()
bestUniqueMacroPixels = eval(bestUniqueMacroPixels)
bestMacroPixelIndexes = eval(bestMacroPixelIndexes)
f.close()

nonRandomisedUniqueMacroPixels = []
for i in bestUniqueMacroPixels:
    temp = []
    for j in i:
        temp2 = []
        for k in j:
            temp2.append(k)
        temp.append(temp2)
    nonRandomisedUniqueMacroPixels.append(temp)

differences = [[[[difference(bestUniqueMacroPixels[macroPixelIndex], rawUniqueMacroPixels[rawMacroPixelIndexes[frameNumber][macroX][macroY]]) for macroPixelIndex in range(64)] for macroY in range(3)] for macroX in range(8)] for frameNumber in range(416)]
#differences[frameNumber][macroX][macroY][macroPixelIndex]
originalDifferences = []
for i in differences:
    temp = []
    for j in i:
        temp2 = []
        for k in j:
            temp3 = []
            for l in k:
                temp3.append(l)
            temp2.append(temp3)
        temp.append(temp2)
    originalDifferences.append(temp)

iteration = 0
macroPixelIndex = 0
toggleOptionsIndex = 0
toggleOptionsIndex2 = 1
toggleOptionsIndex3 = 2
tweak = False

while True:
    print(f"\n\nCurrently on iteration: {iteration}")
    print(f"Tweaking index: {macroPixelIndex}")
    print(f"toggleOptionsIndex = {toggleOptionsIndex}")
    print(f"toggleOptionsIndex2 = {toggleOptionsIndex2 + toggleOptionsIndex}")
    print(f"toggleOptionsIndex3 = {toggleOptionsIndex3 + toggleOptionsIndex2 + toggleOptionsIndex}")
    print(f"Best Error = {bestError}")
    
    toggleOptions = []
    for microY in range(8):
        for microX in range(4):
            toggleOptions.append([microX, microY])
    """for microX in range(4):
        for microY in range(8):
            value = bestUniqueMacroPixels[macroPixelIndex][microX][microY]
            if microX - 1 >= 0:
                if bestUniqueMacroPixels[macroPixelIndex][microX - 1][microY] != value:
                    toggleOptions.append([microX, microY])
            if microY - 1 >= 0:
                if bestUniqueMacroPixels[macroPixelIndex][microX][microY - 1] != value:
                    toggleOptions.append([microX, microY])
            if microX + 1 < 4:
                if bestUniqueMacroPixels[macroPixelIndex][microX + 1][microY] != value:
                    toggleOptions.append([microX, microY])
            if microY + 1 < 8:
                if bestUniqueMacroPixels[macroPixelIndex][microX][microY + 1] != value:
                    toggleOptions.append([microX, microY])"""
    
    """pixel = [toggleOptionsIndex % 4, toggleOptionsIndex // 4]
    if toggleOptionsIndex >= 31:
        toggleOptionsIndex = 0
        macroPixelIndex += 1
        if macroPixelIndex >= 64:
            macroPixelIndex = 0
    else:
        toggleOptionsIndex += 1"""
    
    good = True
    if len(toggleOptions) >= 2:
        if toggleOptionsIndex < len(toggleOptions) - 1:
            pixel = toggleOptions[toggleOptionsIndex]
            if toggleOptionsIndex + toggleOptionsIndex2 < len(toggleOptions) - 1:
                pixel2 = toggleOptions[toggleOptionsIndex + toggleOptionsIndex2]
                if toggleOptionsIndex + toggleOptionsIndex2 + toggleOptionsIndex3 < len(toggleOptions) - 1:
                    pixel3 = toggleOptions[toggleOptionsIndex + toggleOptionsIndex2 + toggleOptionsIndex3]
                else:
                    pixel3 = toggleOptions[0]
            else:
                pixel2 = toggleOptions[0]
                pixel3 = toggleOptions[1]
        else:
            pixel = toggleOptions[0]
            pixel2 = toggleOptions[toggleOptionsIndex2]
            pixel3 = toggleOptions[toggleOptionsIndex3]
        if toggleOptionsIndex + toggleOptionsIndex2 + toggleOptionsIndex3 < len(toggleOptions) - 3:
            toggleOptionsIndex3 += 1
        else:
            toggleOptionsIndex3 = 2
            if toggleOptionsIndex + toggleOptionsIndex2 < len(toggleOptions) - 2:
                toggleOptionsIndex2 += 1
            else:
                toggleOptionsIndex2 = 1
                toggleOptionsIndex += 1
                if toggleOptionsIndex >= len(toggleOptions) - 1:
                    toggleOptionsIndex = 0
                    macroPixelIndex += 1
                    if macroPixelIndex >= 64:
                        if not(tweak):
                            break
                        else:
                            tweak = False
                        macroPixelIndex = 0
                else:
                    pass#toggleOptionsIndex += 1
                
        """if toggleOptionsIndex >= len(toggleOptions) - 1:
            toggleOptionsIndex = 0
            macroPixelIndex += 1
            if macroPixelIndex >= 64:
                macroPixelIndex = 0
        else:
            toggleOptionsIndex += 1"""
    else:
        good = False
        #pixel = [random.randrange(0, 4), random.randrange(0, 8)]
        toggleOptionsIndex = 0
        toggleOptionsIndex2 = 1
        macroPixelIndex += 1
        if macroPixelIndex >= 64:
            if not(tweak):
                break
            else:
                tweak = False
            macroPixelIndex = 0
    
    if good:
        bestUniqueMacroPixels[macroPixelIndex][pixel[0]][pixel[1]] = int(bestUniqueMacroPixels[macroPixelIndex][pixel[0]][pixel[1]] == 0)
        bestUniqueMacroPixels[macroPixelIndex][pixel2[0]][pixel2[1]] = int(bestUniqueMacroPixels[macroPixelIndex][pixel2[0]][pixel2[1]] == 0)
        bestUniqueMacroPixels[macroPixelIndex][pixel3[0]][pixel3[1]] = int(bestUniqueMacroPixels[macroPixelIndex][pixel3[0]][pixel3[1]] == 0)
    
    for frameNumber in range(416):
        for macroX in range(8):
                for macroY in range(3):
                    differences[frameNumber][macroX][macroY][macroPixelIndex] = difference(bestUniqueMacroPixels[macroPixelIndex], rawUniqueMacroPixels[rawMacroPixelIndexes[frameNumber][macroX][macroY]])
                    bestMacroPixelIndexes[frameNumber][macroX][macroY] = differences[frameNumber][macroX][macroY].index(min(differences[frameNumber][macroX][macroY]))
    
    error = realError(bestMacroPixelIndexes, bestUniqueMacroPixels)
    print(f"Calculated Error = {error}")
    
    if error < bestError:
        bestError = error
        tweak = True
        
        f = open(f"{len(bestUniqueMacroPixels)}_ERROR_{bestError}_Bad_Apple.txt", "w")
        f.write((str(bestUniqueMacroPixels) + "\n" + str(bestMacroPixelIndexes)).replace(" ", ""))
        f.close()
        
        print("\n\n\nFOUND IMPROVEMENT\n\n\n")
        
        iteration = 0
        nonRandomisedUniqueMacroPixels = []
        for i in bestUniqueMacroPixels:
            temp = []
            for j in i:
                temp2 = []
                for k in j:
                    temp2.append(k)
                temp.append(temp2)
            nonRandomisedUniqueMacroPixels.append(temp)
            
        originalDifferences = []
        for i in differences:
            temp = []
            for j in i:
                temp2 = []
                for k in j:
                    temp3 = []
                    for l in k:
                        temp3.append(l)
                    temp2.append(temp3)
                temp.append(temp2)
            originalDifferences.append(temp)
        
        #macroPixelIndex = 0
        
    else:
        bestUniqueMacroPixels = []
        for i in nonRandomisedUniqueMacroPixels:
            temp = []
            for j in i:
                temp2 = []
                for k in j:
                    temp2.append(k)
                temp.append(temp2)
            bestUniqueMacroPixels.append(temp)
        
        differences = []
        for i in originalDifferences:
            temp = []
            for j in i:
                temp2 = []
                for k in j:
                    temp3 = []
                    for l in k:
                        temp3.append(l)
                    temp2.append(temp3)
                temp.append(temp2)
            differences.append(temp)
            
        iteration += 1

print("\n\n\nFinished\n\n\n")
