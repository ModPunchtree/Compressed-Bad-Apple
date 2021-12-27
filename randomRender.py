
# generate 64 random unique macro pixels

# iterate through the raw macro pixels,
# calculate difference for each unique macro pixel,
# set the lowest difference as the index for that macro pixel

# calculate final true error
# save result
# potentially iterate more than once

import random

def generateRandomMacroPixel() -> list:
    macroPixelValues = []
    valueList = [i for i in range(32)]
    for i in range(random.randrange(1, random.randrange(2, 9))):
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

def generateUniqueMacroPixels() -> tuple:
    uniqueMacroPixels = []
    bad = True
    while bad:
        uniqueMacroPixels = [generateRandomMacroPixel() for i in range(62)]
        uniqueMacroPixels.append([[0 for j in range(8)] for i in range(4)])
        uniqueMacroPixels.append([[1 for j in range(8)] for i in range(4)])
        bad = False
        for macroPixel in uniqueMacroPixels:
            if uniqueMacroPixels.count(macroPixel) > 1:
                bad = True
    
    return tuple(uniqueMacroPixels)

def readRawData() -> tuple[list, list]:
    f = open("fullRawMacroPixels.txt", "r")
    uniqueMacroPixels, macroPixelIndexes = f.readlines()
    f.close()
    uniqueMacroPixels = eval(uniqueMacroPixels)
    macroPixelIndexes = eval(macroPixelIndexes)
    return (uniqueMacroPixels, macroPixelIndexes)

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

macroPixelIndexes = [[[0 for i in range(3)] for k in range(8)] for j in range(416)]
rawUniqueMacroPixels, rawMacroPixelIndexes = readRawData()

bestError = 9999999999
iteration = 0
maxIterations = 10000
while iteration < maxIterations:
    print(f"Working on iteration: {iteration}")
    percentage = ("   " + str((iteration * 10000) // maxIterations))[-4: -2] + "." + ("0" + str((iteration * 10000) // maxIterations))[-2: ]
    print(f"Percent completion: {percentage} %")
    
    iteration += 1
    uniqueMacroPixels = generateUniqueMacroPixels()
    
    for frameNumber in range(416):
        #print(f"Working on frame: {frameNumber}")
        #percentage = ("   " + str((frameNumber * 10000) // 416))[-4: -2] + "." + ("0" + str((frameNumber * 10000) // 416))[-2: ]
        #print(f"Percent completion: {percentage} %")
        for macroX in range(8):
            for macroY in range(3):
                differences = [difference(macroPixel, rawUniqueMacroPixels[rawMacroPixelIndexes[frameNumber][macroX][macroY]]) for macroPixel in uniqueMacroPixels]
                macroPixelIndexes[frameNumber][macroX][macroY] = differences.index(min(differences))

    error = realError(macroPixelIndexes, uniqueMacroPixels)
    
    if error < bestError:
        bestError = error
        bestUniqueMacroPixels = [i for i in uniqueMacroPixels]
        bestMacroPixelIndexes = [i for i in macroPixelIndexes]
        
        f = open(f"{len(bestUniqueMacroPixels)}_ERROR_{bestError}_Bad_Apple.txt", "w")
        f.write((str(bestUniqueMacroPixels) + "\n" + str(bestMacroPixelIndexes)).replace(" ", ""))
        f.close()
