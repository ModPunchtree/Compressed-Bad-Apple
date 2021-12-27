
import random

def readPrecalculatedDifferences() -> tuple[list, list]:
    f = open(f"precalculatedDifferences.txt", "r")
    differences, occurrences = f.readlines()
    f.close()
    differences = eval(differences)
    occurrences = eval(occurrences)
    return differences, occurrences

def readRawData() -> tuple[list, list]:
    f = open("fullRawMacroPixels.txt", "r")
    uniqueMacroPixels, macroPixelIndexes = f.readlines()
    f.close()
    uniqueMacroPixels = eval(uniqueMacroPixels)
    macroPixelIndexes = eval(macroPixelIndexes)
    return (uniqueMacroPixels, macroPixelIndexes)

def merge(macroPixelIndexOne: int, macroPixelIndexTwo: int, macroPixelIndexes: list, occurrences: list) -> tuple[list, int, list]:
    global uniqueMacroPixels
    
    numberOfOne = occurrences[macroPixelIndexOne]
    numberOfTwo = occurrences[macroPixelIndexTwo]
    
    # generate average macro pixel
    #averageMacroPixel = [[0 for j in range(8)] for i in range(4)]
    #for microX in range(4):
    #    for microY in range(8):
    #        if random.randrange(0, numberOfOne + numberOfTwo) < numberOfOne:
    #            averageMacroPixel[microX][microY] = uniqueMacroPixels[macroPixelIndexOne][microX][microY]
    #        else:
    #            averageMacroPixel[microX][microY] = uniqueMacroPixels[macroPixelIndexTwo][microX][microY]
    
    if numberOfOne > numberOfTwo:
        poppedIndex = macroPixelIndexTwo
        keptIndex = macroPixelIndexOne
    else:
        poppedIndex = macroPixelIndexOne
        keptIndex = macroPixelIndexTwo
    
    #uniqueMacroPixels[keptIndex] = averageMacroPixel
    occurrences[keptIndex] = numberOfOne + numberOfTwo
    
    for frameNumber in range(416):
        for macroX in range(8):
            for macroY in range(3):
                if macroPixelIndexes[frameNumber][macroX][macroY] == poppedIndex:
                    if keptIndex > poppedIndex:
                        macroPixelIndexes[frameNumber][macroX][macroY] = keptIndex - 1
                    else:
                        macroPixelIndexes[frameNumber][macroX][macroY] = keptIndex
                elif macroPixelIndexes[frameNumber][macroX][macroY] > poppedIndex:
                    macroPixelIndexes[frameNumber][macroX][macroY] -= 1
                    
    uniqueMacroPixels.pop(poppedIndex)
    occurrences.pop(poppedIndex)
    
    return macroPixelIndexes, poppedIndex, occurrences

def reduceDifferences(differences: list, poppedIndex: int) -> list:
    indexOffset = 0
    for index in range(len(differences)):
        index += indexOffset
        if poppedIndex in differences[index][: -1]:
            differences.pop(index)
            indexOffset -= 1
        else:
            differences[index][0] -= (differences[index][0] > poppedIndex)
            differences[index][1] -= (differences[index][1] > poppedIndex)
        
    return differences

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
                    differentNeighbours = 17
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
                    error += differentNeighbours
    
    return error

uniqueMacroPixels, macroPixelIndexes = readRawData()
print("Reading raw data ...")
differences, occurrences = readPrecalculatedDifferences()

bestUniqueMacroPixels = []
bestMacroPixelIndexes = []
bestError = 9999999999
iteration = 0
maxIterations = 20
while iteration < maxIterations:
    iteration += 1
    print(f"Iteration: {iteration}")
    percentage = ("000" + str((iteration * 10000) // maxIterations))[-4: -2] + "." + ("0" + str((iteration * 10000) // maxIterations))[-2: ]
    print(f"Percent completion: {percentage} %")
    
    random.shuffle(differences)
    def getLastItem(x):
        return x[2]
    differences.sort(key=getLastItem)
    goal = len(uniqueMacroPixels) - 64
    while len(uniqueMacroPixels) > 64:
        print(f"Number of Unique Macro Pixels Left: {len(uniqueMacroPixels)}")
        percentage = ("000" + str(((goal - len(uniqueMacroPixels) + 64) * 10000) // goal))[-4: -2] + "." + ("0" + str(((goal - len(uniqueMacroPixels) + 64) * 10000) // goal))[-2: ]
        print(f"Percent completion: {percentage} %")
        macroPixelIndexes, poppedIndex, occurrences = merge(differences[0][0], differences[0][1], macroPixelIndexes, occurrences)
        differences = reduceDifferences(differences, poppedIndex)
        
        if len(uniqueMacroPixels) in [64, 128, 256]:
            error = realError(macroPixelIndexes, uniqueMacroPixels)
            f = open(f"{len(uniqueMacroPixels)}_ERROR_{error}_Bad_Apple.txt", "w")
            f.write((str(uniqueMacroPixels) + "\n" + str(macroPixelIndexes)).replace(" ", ""))
            f.close()
            
    error = realError(macroPixelIndexes, uniqueMacroPixels)
    print(f"Real Error: {error}")
    
    if error < bestError:
        bestError = error
        bestUniqueMacroPixels = [uniqueMacroPixels[i] for i in range(len(uniqueMacroPixels))]
        bestMacroPixelIndexes = [macroPixelIndexes[i] for i in range(len(macroPixelIndexes))]
        
    print(f"Best Error: {bestError}")
    
    if iteration < maxIterations:
        uniqueMacroPixels, macroPixelIndexes = readRawData()
        print("Reading raw data ...")
        differences, occurrences = readPrecalculatedDifferences()
