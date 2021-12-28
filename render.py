
import time

MacroPixels = 64
Error = 11789
f = open(f"{MacroPixels}_ERROR_{Error}_Bad_Apple.txt", "r")
UniqueMacroPixels, MacroPixelIndexes = f.readlines()
f.close()

bestUniqueMacroPixels = eval(UniqueMacroPixels)
bestMacroPixelIndexes = eval(MacroPixelIndexes)

frames = []
for frameNumber in range(416):
    frame = ""
    for macroY in range(3):
        printLines = ["" for i in range(8)]
        for macroX in range(8):
            for Y in range(8):
                for X in range(4):
                    if bestUniqueMacroPixels[bestMacroPixelIndexes[frameNumber][macroX][2 - macroY]][X][7 - Y] == 0:
                        #printLines[Y] += "  "
                        printLines[Y] += "⬛"
                    else:
                        #printLines[Y] += "##"
                        printLines[Y] += "⬜"
        frame += "\n" + "\n".join(printLines)
    frames.append(frame[1: ] + "\n")

for i in range(10):
    print(i)
    print(i)
    #time.sleep(1)

for frameNumber in range(416):
    print("\n\n\n" + frames[frameNumber][: -1])
    time.sleep(0.5)
    