
# differences
# occurences

# input fullRawMacroPixels

# calculate occurences
# calculate differences

# write results to file

import random

def readRawData() -> tuple[list, list]:
    f = open("fullRawMacroPixels.txt", "r")
    uniqueMacroPixels, macroPixelIndexes = f.readlines()
    f.close()
    uniqueMacroPixels = eval(uniqueMacroPixels)
    macroPixelIndexes = eval(macroPixelIndexes)
    return (uniqueMacroPixels, macroPixelIndexes)

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

def calculateDifferences(uniqueMacroPixels, macroPixelIndexes, occurrences) -> list:
    differences = []
    for indexOne, macroPixelOne in enumerate(uniqueMacroPixels):
        print(f"Calculating differences for macro pixel: {indexOne}")
        for indexTwo, macroPixelTwo in enumerate(uniqueMacroPixels[indexOne + 1: ]):
            if indexTwo != 1:
                delta = difference(macroPixelOne, macroPixelTwo, occurrences, len(differences) - 1)
                differences.append([indexOne + 2, indexTwo + indexOne + 1, delta])
    return differences

def difference(macroPixelOne: list, macroPixelTwo: list, occurrences: list, index: int) -> int:
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
                differentNeighbours = 17
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
                delta += differentNeighbours
    
    delta += abs(sum1 - sum2)
    
    # horrizontal checkerboard check
    change = 0
    currentValue = macroPixelOne[0][0]
    for microY in range(8):
        for microX in range(4):
            if macroPixelOne[microX][microY] != currentValue:
                currentValue = macroPixelOne[microX][microY]
                change += 1
    
    # vertical checkerboard check
    change2 = 0
    currentValue = macroPixelOne[0][0]
    for microX in range(4):
        for microY in range(8):
            if macroPixelOne[microX][microY] != currentValue:
                currentValue = macroPixelOne[microX][microY]
                change2 += 1
    
    if change < change2:
        delta += (31 - change)
    else:
        delta += (31 - change2)
    
    numberOfOne = occurrences[uniqueMacroPixels.index(macroPixelOne)]
    numberOfTwo = occurrences[uniqueMacroPixels.index(macroPixelTwo)]
    delta *= (numberOfTwo * (numberOfOne >= numberOfTwo) + numberOfOne * (numberOfOne < numberOfTwo))
    
    delta += (10000000 - index) // 100000
    
    return delta

uniqueMacroPixels, macroPixelIndexes = readRawData()
occurrences = calculateOccurrences(uniqueMacroPixels, macroPixelIndexes)
differences = calculateDifferences(uniqueMacroPixels, macroPixelIndexes, occurrences)

f = open(f"precalculatedDifferences.txt", "w")
f.write((str(differences) + "\n" + str(occurrences)).replace(" ", ""))
f.close()
