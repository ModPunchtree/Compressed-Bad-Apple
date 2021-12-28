
# import pil

# read best data

# for frameNumber in range 416
    # read raw image
    # pixel = image.load()
    # for pixel in frameNumber from best data
        # edit each pixel[x, y]
    # save image (overwrite)

from PIL import Image

bestError = 12753
f = open(f"64_ERROR_{bestError}_Bad_Apple.txt", "r")
bestUniqueMacroPixels, bestMacroPixelIndexes = f.readlines()
bestUniqueMacroPixels = eval(bestUniqueMacroPixels)
bestMacroPixelIndexes = eval(bestMacroPixelIndexes)
f.close()

for frameNumber in range(416):
    frameNumber2 = str(frameNumber)
    while len(frameNumber2) < 3:
        frameNumber2 = "0" + frameNumber2
    frame = Image.open(f"Pics/frame_{frameNumber}_delay-0.5s.gif")
    pixels = frame.load()
    for macroX in range(8):
        for macroY in range(3):
            for microX in range(4):
                for microY in range(8):
                    X = macroX * 4 + microX
                    Y = macroY * 8 + microY
                    pixels[X, Y]
    
    frame.close()
