
# number of pixels = 0 

# bestError = 12671
# get best data 

# create backup of best data

# get raw data 

# calculate differences

# create backup of differences

# iteration = 0
# while true:
  # numberOfPixels += 1
  # toggleIndex = [0 for i in range(numberOfPixels + 1)]
  # while true:
    # tweak = false
    # stop = false
    # pixels = [ ]
    # for i in toggleIndex[1: ]:
      # pixels.append([i % 4, i // 4])
    # pixels = list(set(pixels)) //double check
    # for pixel in pixels:
      # bestUniqueMacroPixels[toggleIndex[0]][pixel[0]][pixel[1]] = int(bestUniqueMacroPixels[toggleIndex[0]][pixel[0]][pixel[1]] == 0)
    # for all raw macro pixels:
      # calculate difference
      # set min to bestMacroPixelIndexes
    # error = realError()
    # iteration += 1
    # if error < bestError:
      # bestError = error
      # save file
      # create backup of new data
      # calculate new differences
      # tweak = true
      # iteration = 0
    # else:
      # restore data from backup
      # restore differences from backup
    # if tweak:
      # toggleIndex = [0 for i in range(numberOfPixels + 1)]
      # numberOfPixels = 0
      # break
    # else: {
    # for i in range(len(toggleIndex)):
      # j = len(toggleIndex) - 1 - i
      # if (j == 0) and (toggleIndex[0] < 63):
        # toggleIndex[0] += 1
        # break
      # elif j == 0:
        # if not(tweak):
          # stop = true
          # break
        # else:
          # toggleIndex[0] = 0
      # if (toggleIndex[j] < 31) and (j != 0):
        # toggleIndex[j] += 1
        # break
      # else:
        # toggleIndex[j] = 0
# }
    # if stop:
      # break
    # print(f"""Number of Pixels: {NumberOfPixels}
# Currently on index: {toggleIndex[0]}
# Pixel Indexes: {toggleIndex[1: ]}
# Best Error: {bestError}
# Current Error: {error}
# Iterations since last improvement: {iteration}""")

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
    #sum1 = 0
    #sum2 = 0
    for microX in range(4):
        #sum1 += sum(macroPixelOne[microX])
        #sum2 += sum(macroPixelTwo[microX])
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
    
    #delta += abs(sum1 - sum2)
  
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

numberOfPixels = 0 

bestError = 12092
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

global rawUniqueMacroPixels
global rawMacroPixelIndexes
rawUniqueMacroPixels, rawMacroPixelIndexes = readRawData()

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

while True:
    numberOfPixels += 1
    toggleIndex = [0 for i in range(numberOfPixels + 1)]
    while True:
        tweak = False
        stop = False
        pixels = []
        for i in toggleIndex[1: ]:
            pixels.append((i % 4, i // 4))
        pixels = list(set(pixels))
        for pixel in pixels:
            bestUniqueMacroPixels[toggleIndex[0]][pixel[0]][pixel[1]] = int(bestUniqueMacroPixels[toggleIndex[0]][pixel[0]][pixel[1]] == 0)

        for frameNumber in range(416):
            for macroX in range(8):
                    for macroY in range(3):
                        differences[frameNumber][macroX][macroY][toggleIndex[0]] = difference(bestUniqueMacroPixels[toggleIndex[0]], rawUniqueMacroPixels[rawMacroPixelIndexes[frameNumber][macroX][macroY]])
                        bestMacroPixelIndexes[frameNumber][macroX][macroY] = differences[frameNumber][macroX][macroY].index(min(differences[frameNumber][macroX][macroY]))

        error = realError(bestMacroPixelIndexes, bestUniqueMacroPixels)

        iteration += 1
        if error < bestError:
            bestError = error
            
            f = open(f"{len(bestUniqueMacroPixels)}_ERROR_{bestError}_Bad_Apple.txt", "w")
            f.write((str(bestUniqueMacroPixels) + "\n" + str(bestMacroPixelIndexes)).replace(" ", ""))
            f.close()
        
            print("\n\n\nFOUND IMPROVEMENT\n\n\n")
            
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
                
            tweak = True
            iteration = 0
        
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

        if tweak:
            toggleIndex = [0 for i in range(numberOfPixels + 1)]
            numberOfPixels = 0
            break
        else:
            for i in range(len(toggleIndex)):
                j = len(toggleIndex) - 1 - i
                if (j == 0) and (toggleIndex[0] < 63):
                    toggleIndex[0] += 1
                    break
                elif j == 0:
                    if not(tweak):
                        stop = True
                        break
                    else:
                        toggleIndex[0] = 0
                elif toggleIndex[j] < 31:
                    toggleIndex[j] += 1
                    break
                else:
                    toggleIndex[j] = 0

        if stop:
            break
        print(f"""Number of Pixels: {numberOfPixels}
Currently on index: {toggleIndex[0]}
Pixel Indexes: {toggleIndex[1: ]}
Best Error: {bestError}
Current Error: {error}
Iterations since last improvement: {iteration}""")
