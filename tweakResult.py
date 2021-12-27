
# import raw data as best data

# calculate occurrences

# randomise least useful pixel
# calculate new error
# if error < best error
# set as new best
# save file
# calculate occurrences

import random

def readRawData() -> tuple[list, list]:
    f = open("fullRawMacroPixels.txt", "r")
    uniqueMacroPixels, macroPixelIndexes = f.readlines()
    f.close()
    uniqueMacroPixels = eval(uniqueMacroPixels)
    macroPixelIndexes = eval(macroPixelIndexes)
    return uniqueMacroPixels, macroPixelIndexes

def calculateOccurrences(uniqueMacroPixels: list, macroPixelIndexes: list) -> list:
    occurrences = []
    number = 0
    for macroPixelIndex in range(len(uniqueMacroPixels)):
        for frameNumber in range(416):
            for macroX in range(8):
                for macroY in range(3):
                    if macroPixelIndexes[frameNumber][macroX][macroY] == macroPixelIndex:
                        number += 1
        occurrences.append(number)
    return occurrences

def generateRandomMacroPixel() -> list:
    macroPixelValues = []
    valueList = [i for i in range(32)]
    for i in range(random.randrange(0, random.randrange(2, 9))):
        macroPixelValues.append(random.choice(valueList))
        valueList.pop(valueList.index(macroPixelValues[-1]))
    macroPixelValues.append(64)
    result = ""
    x = random.randrange(0, 2)
    macroPixelValues.sort()
    while len(result) < 64:
        if len(result) > macroPixelValues[0]:
            x = int(x == 0)
            macroPixelValues.pop(0)
        result += str(x)
    
    if random.randrange(0, 2) == 1:
        macroPixel = [[int(result[i * 8 + j]) for j in range(8)] for i in range(4)]
    else:
        macroPixel = [[int(result[i + j * 4]) for j in range(8)] for i in range(4)]
        
    return macroPixel

def realError(macroPixelIndexes: list, uniqueMacroPixels: list) -> int:
    rawUniqueMacroPixels, rawMacroPixelIndexes = readRawData()
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
                    error += 1
    
    return error

def difference(macroPixelOne: list, macroPixelTwo: list) -> int:
    if random.randrange(0, 2) == 1:
        macroPixelOne, macroPixelTwo = macroPixelTwo, macroPixelOne
    delta = 0
    sum1 = 0
    sum2 = 0
    for microX in range(4):
        sum1 += sum(macroPixelOne[microX])
        sum2 += sum(macroPixelTwo[microX])
        for microY in range(8):
            if macroPixelOne[microX][microY] != macroPixelTwo[microX][microY]:
                delta += 1
    
    delta += abs(sum1 - sum2)
  
    return delta

bestError = 12818
f = open(f"64_ERROR_{bestError}_Bad_Apple.txt", "r")
bestUniqueMacroPixels, bestMacroPixelIndexes = f.readlines()
bestUniqueMacroPixels = eval(bestUniqueMacroPixels)
bestMacroPixelIndexes = eval(bestMacroPixelIndexes)
f.close()

random.shuffle(bestUniqueMacroPixels)
occurrences = calculateOccurrences(bestUniqueMacroPixels, bestMacroPixelIndexes)
for index in range(len(bestUniqueMacroPixels)):
    bestUniqueMacroPixels[occurrences.index(min(occurrences[index: ]))], bestUniqueMacroPixels[index] = bestUniqueMacroPixels[index], bestUniqueMacroPixels[occurrences.index(min(occurrences[index: ]))]
    occurrences[occurrences.index(min(occurrences[index: ]))], occurrences[index] = occurrences[index], occurrences[occurrences.index(min(occurrences[index: ]))]

rawUniqueMacroPixels, rawMacroPixelIndexes = readRawData()
randomisedIndex = 10
nonRandomisedUniqueMacroPixels = []
for i in bestUniqueMacroPixels:
    temp = []
    for j in i:
        temp2 = []
        for k in j:
            temp2.append(k)
        temp.append(temp2)
    nonRandomisedUniqueMacroPixels.append(temp)

bestUniqueMacroPixels[randomisedIndex] = generateRandomMacroPixel()

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

iteration = 1
while True:
    print(f"\nCurrently on iteration: {iteration}")
    print(f"Randomising index: {randomisedIndex}")
    print(f"Best Error = {bestError}")
    iteration += 1
    for frameNumber in range(416):
        #print(f"Working on frame: {frameNumber}")
        #percentage = ("   " + str((frameNumber * 10000) // 416))[-4: -2] + "." + ("0" + str((frameNumber * 10000) // 416))[-2: ]
        #print(f"Percent completion: {percentage} %")
        for macroX in range(8):
            for macroY in range(3):
                differences[frameNumber][macroX][macroY][randomisedIndex] = difference(bestUniqueMacroPixels[randomisedIndex], rawUniqueMacroPixels[rawMacroPixelIndexes[frameNumber][macroX][macroY]])
                bestMacroPixelIndexes[frameNumber][macroX][macroY] = differences[frameNumber][macroX][macroY].index(min(differences[frameNumber][macroX][macroY]))

    error = realError(bestMacroPixelIndexes, bestUniqueMacroPixels)
    print(f"Calculated Error = {error}")

    if error < bestError:
        bestError = error
        
        f = open(f"{len(bestUniqueMacroPixels)}_ERROR_{bestError}_Bad_Apple.txt", "w")
        f.write((str(bestUniqueMacroPixels) + "\n" + str(bestMacroPixelIndexes)).replace(" ", ""))
        f.close()
        
        occurrences = calculateOccurrences(bestUniqueMacroPixels, bestMacroPixelIndexes)
        for index in range(len(bestUniqueMacroPixels)):
            bestUniqueMacroPixels[occurrences.index(min(occurrences[index: ]))], bestUniqueMacroPixels[index] = bestUniqueMacroPixels[index], bestUniqueMacroPixels[occurrences.index(min(occurrences[index: ]))]
            occurrences[occurrences.index(min(occurrences[index: ]))], occurrences[index] = occurrences[index], occurrences[occurrences.index(min(occurrences[index: ]))]
        
        randomisedIndex = 0
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
            
        bestUniqueMacroPixels[randomisedIndex] = generateRandomMacroPixel()
        
        
    else:
        if iteration >= 100:
            break
            iteration = 0
            randomisedIndex += 1
            if randomisedIndex >= 64:
                randomisedIndex = 0
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
        bestUniqueMacroPixels[randomisedIndex] = generateRandomMacroPixel()
