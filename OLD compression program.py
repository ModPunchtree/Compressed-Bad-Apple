
from PIL import Image
import random
import time

def grabFrame(frameNumber: int) -> tuple:
    frameNumber = str(frameNumber)
    while len(frameNumber) < 3:
        frameNumber = "0" + frameNumber
    frame = Image.open(f"Pics/frame_{frameNumber}_delay-0.5s.gif")
    pixels = frame.load()
    frame.close()
    result = [[0 for j in range(24)] for i in range(32)]
    for height in range(24):
        for width in range(32):
            result[width][23 - height] = pixels[width, height]
    return tuple(result)

def getFrameMacroPixels(frameNumber: int) -> tuple:
    data = grabFrame(frameNumber)
    
    result = [[[[0 for k in range(8)] for j in range(4)] for i in range(3)] for l in range(8)]
    
    for macroX in range(8):
        for macroY in range(3):
            for microX in range(4):
                for microY in range(8):
                    X = macroX * 4 + microX
                    Y = macroY * 8 + microY
                    result[macroX][macroY][microX][microY] = data[X][Y]
    
    return tuple(result)

def updateUniqueMacroPixels(rawMacroData: tuple) -> None:
    global uniqueMacroPixels
    for macroX in range(8):
        for macroY in range(3):
            if rawMacroData[macroX][macroY] not in uniqueMacroPixels:
                uniqueMacroPixels.append(rawMacroData[macroX][macroY])

def difference(macroPixelOne: tuple, macroPixelTwo: tuple, index: int) -> int:
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
    
    numberOfOne = occurrence[uniqueMacroPixels.index(macroPixelOne)]
    numberOfTwo = occurrence[uniqueMacroPixels.index(macroPixelTwo)]
    delta *= (numberOfTwo * (numberOfOne >= numberOfTwo) + numberOfOne * (numberOfOne < numberOfTwo))
    
    delta += (10000000 - index) // 10000
    
    return delta

def calculateDifferences() -> list:
    differences = []
    for indexOne, macroPixelOne in enumerate(uniqueMacroPixels[2:]):
        print(f"Calculating differences for macro pixel: {indexOne}")
        for indexTwo, macroPixelTwo in enumerate(uniqueMacroPixels[indexOne + 1: ]):
            if indexTwo != 1:
                delta = difference(macroPixelOne, macroPixelTwo, len(differences) - 1)
                differences.append([indexOne + 2, indexTwo + indexOne + 1, delta])
    return differences

def getMacroPixelIndexes(rawMacroData: tuple) -> list:
    macroPixelIndexes = [[0 for j in range(3)] for i in range(8)]
    for macroX in range(8):
        for macroY in range(3):
            macroPixelIndexes[macroX][macroY] = uniqueMacroPixels.index(rawMacroData[macroX][macroY])
    return macroPixelIndexes

def merge(macroPixelIndexOne: int, macroPixelIndexTwo: int, macroPixelIndexes: list) -> tuple:
    global uniqueMacroPixels
    
    numberOfOne = occurrence[macroPixelIndexOne]
    numberOfTwo = occurrence[macroPixelIndexTwo]
    
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
    occurrence[keptIndex] = numberOfOne + numberOfTwo
    
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
    occurrence.pop(poppedIndex)
    
    return macroPixelIndexes, poppedIndex

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

def getOccurrence(macroPixelIndexes: list) -> None:
    global occurrence
    number = 0
    for macroPixelIndex in range(len(uniqueMacroPixels)):
        for frameNumber in range(416):
            for macroX in range(8):
                for macroY in range(3):
                    if macroPixelIndexes[frameNumber][macroX][macroY] == macroPixelIndex:
                        number += 1
        occurrence.append(number)

def realError(macroPixelIndexes: list) -> int:
    error = 0
    for frameNumber in range(416):
        rawMacroData = getFrameMacroPixels(frameNumber)
        for macroY in range(3):
            for macroX in range(8):
                for microY in range(8):
                    for microX in range(4):
                        if rawMacroData[macroX][macroY][microX][microY] != uniqueMacroPixels[macroPixelIndexes[frameNumber][macroX][2 - macroY]][microX][microY]:
                            differentNeighbours = 17
                            if (microX - 1 >= 0) and (microY - 1 >= 0):
                                if rawMacroData[macroX][macroY][microX][microY] == uniqueMacroPixels[macroPixelIndexes[frameNumber][macroX][2 - macroY]][microX - 1][microY - 1]:
                                    differentNeighbours -= 2
                            else:
                                differentNeighbours -= 1
                            if (microX - 1 >= 0):
                                if rawMacroData[macroX][macroY][microX][microY] == uniqueMacroPixels[macroPixelIndexes[frameNumber][macroX][2 - macroY]][microX - 1][microY]:
                                    differentNeighbours -= 2
                            else:
                                differentNeighbours -= 1
                            if (microX - 1 >= 0) and (microY + 1 < 8):
                                if rawMacroData[macroX][macroY][microX][microY] == uniqueMacroPixels[macroPixelIndexes[frameNumber][macroX][2 - macroY]][microX - 1][microY + 1]:
                                    differentNeighbours -= 2
                            else:
                                differentNeighbours -= 1
                            if (microY - 1 >= 0):
                                if rawMacroData[macroX][macroY][microX][microY] == uniqueMacroPixels[macroPixelIndexes[frameNumber][macroX][2 - macroY]][microX][microY - 1]:
                                    differentNeighbours -= 2
                            else:
                                differentNeighbours -= 1
                            if (microY + 1 < 8):
                                if rawMacroData[macroX][macroY][microX][microY] == uniqueMacroPixels[macroPixelIndexes[frameNumber][macroX][2 - macroY]][microX][microY + 1]:
                                    differentNeighbours -= 2
                            else:
                                differentNeighbours -= 1
                            if (microX + 1 < 4) and (microY - 1 >= 0):
                                if rawMacroData[macroX][macroY][microX][microY] == uniqueMacroPixels[macroPixelIndexes[frameNumber][macroX][2 - macroY]][microX + 1][microY - 1]:
                                    differentNeighbours -= 2
                            else:
                                differentNeighbours -= 1
                            if (microX + 1 < 4):
                                if rawMacroData[macroX][macroY][microX][microY] == uniqueMacroPixels[macroPixelIndexes[frameNumber][macroX][2 - macroY]][microX + 1][microY]:
                                    differentNeighbours -= 2
                            else:
                                differentNeighbours -= 1
                            if (microX + 1 < 4) and (microY + 1 < 8):
                                if rawMacroData[macroX][macroY][microX][microY] == uniqueMacroPixels[macroPixelIndexes[frameNumber][macroX][2 - macroY]][microX + 1][microY + 1]:
                                    differentNeighbours -= 2
                            else:
                                differentNeighbours -= 1
                            error += differentNeighbours
    return error

bestUniqueMacroPixels = []
bestMacroPixelIndexes = []
bestError = 99999999999
iteration = 0
maxIterations = 1
while iteration < maxIterations:
    iteration += 1
    print(f"Iteration: {iteration}")
    percentage = ("000" + str((iteration * 10000) // maxIterations))[-6: -2] + "." + ("0" + str((iteration * 10000) // maxIterations))[-2: ]
    print(f"Percent completion: {percentage} %")
    
    global occurrence
    occurrence = []
    
    global uniqueMacroPixels
    uniqueMacroPixels = [[[0 for j in range(8)] for i in range(4)], [[1 for l in range(8)] for k in range(4)]]

    macroPixelIndexes = [[[0 for j in range(3)] for i in range(8)] for l in range(416)] # list[frame][x][y]
    for frameNumber in range(416): # should be 416
        rawMacroData = getFrameMacroPixels(frameNumber)
        updateUniqueMacroPixels(rawMacroData)
        macroPixelIndexes[frameNumber] = getMacroPixelIndexes(rawMacroData)
    
    getOccurrence(macroPixelIndexes)

    totalError = 0
    differences = calculateDifferences()
    random.shuffle(differences)
    def getLastItem(x):
        return x[2]
    differences.sort(key=getLastItem)
    goal = len(uniqueMacroPixels) - 64
    while len(uniqueMacroPixels) > 64:
        print(f"Number of Unique Macro Pixels Left: {len(uniqueMacroPixels)}")
        print(f"Error so far: {totalError}")
        percentage = ("000" + str(((goal - len(uniqueMacroPixels) + 64) * 10000) // goal))[-6: -2] + "." + ("0" + str(((goal - len(uniqueMacroPixels) + 64) * 10000) // goal))[-2: ]
        print(f"Percent completion: {percentage} %")

        totalError += differences[0][2]
        macroPixelIndexes, poppedIndex = merge(differences[0][0], differences[0][1], macroPixelIndexes)
        differences = reduceDifferences(differences, poppedIndex)
        
        if len(uniqueMacroPixels) in [64, 128, 256]:
            error = realError(macroPixelIndexes)
            f = open(f"{len(uniqueMacroPixels)}_ERROR_{error}_Bad_Apple.txt", "w")
            f.write(str(uniqueMacroPixels) + "\n" + str(macroPixelIndexes))
            f.close()

    #print(f"Final number of uniqueMacroPixels: {len(uniqueMacroPixels)}")
    error = realError(macroPixelIndexes)
    print(f"Real Error: {error}")
    
    if error < bestError:
        bestError = error
        bestUniqueMacroPixels = [uniqueMacroPixels[i] for i in range(len(uniqueMacroPixels))]
        bestMacroPixelIndexes = [macroPixelIndexes[i] for i in range(len(macroPixelIndexes))]
        
    print(f"Best Error: {bestError}")

# save to .txt file
#f = open(f"ERROR_{bestError}_Bad_Apple.txt", "w")
#f.write(str(bestUniqueMacroPixels) + "\n" + str(bestMacroPixelIndexes))
#f.close()
"""
# render
frames = []
for frameNumber in range(416):
    frame = ""
    for macroY in range(3):
        printLines = ["" for i in range(8)]
        for macroX in range(8):
            for Y in range(8):
                for X in range(4):
                    if bestUniqueMacroPixels[bestMacroPixelIndexes[frameNumber][macroX][2 - macroY]][X][7 - Y] == 0:
                        printLines[Y] += "⬛"
                    else:
                        printLines[Y] += "⬜"
        frame += "\n" + "\n".join(printLines)
    frames.append(frame[1: ] + "\n")

input("DONE\nPress Enter to view the best iteration: ")

for frameNumber in range(416):
    print("\n\n\n" + frames[frameNumber][: -1])
    time.sleep(0.5)
"""
