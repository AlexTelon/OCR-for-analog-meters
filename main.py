from PIL import Image
import os
import ImgFunctions as imf
import FileFunctions as ff
import NameMaker as nm
from pathlib import Path

#                       Settings for the program
#-------------------------------------------------------------------------

# Not needed with my current sample image. too lazy to edit it to the original size right now.
# The square that the program will cut out and use
# The first two numbers represent upper left corner of the square
# The last two numbers represent lower right corner of the square
# SQUARE = (130, 300, 270, 370)

# The ammount of pixels that are reduced for each step
PERCENT_TO_REDUCE = 10

# The ammount steps with reduction that are taken
AMMOUNT_OF_STEPS = 9

#-------------------------------------------------------------------------

# Make bitmaps from the bin files and store them in the input folder:
# os.system('./Bitmapizer -bitmapize')


# Define input and output directories and create subfolders for each colour depth:
PATH_INPUT = Path('input')
PATH_OUTPUT = Path('output')

PATH_INPUT.mkdir(exist_ok=True)
(PATH_OUTPUT / '8bit').mkdir(exist_ok=True)
(PATH_OUTPUT / '4bit').mkdir(exist_ok=True)
(PATH_OUTPUT / '2bit').mkdir(exist_ok=True)
(PATH_OUTPUT / '1bit').mkdir(exist_ok=True)
outputPath8Bit = (PATH_OUTPUT / '8bit')

# Function should be used with the loopTroughDirectory function in FileFunctions
def loopTroughFunction(filePath, fileName, pathOutput):

    for i in range(0,AMMOUNT_OF_STEPS+1):
        #print('loopTroughFunction -> Loop: '+str(i))
        #print('loopTroughFunction -> Filename: '+ filePath)

        # the quality of the picture in pixels, 100 is orgininal quality
        qualityPercent = 100 - (i * PERCENT_TO_REDUCE)

        newPathOutput = pathOutput / f"{qualityPercent}ppt"

        ff.makeDirectory(newPathOutput)

        im = Image.open(filePath / fileName)

        # Removed crop since my sample image does not need it
        # croppedIm = imf.cropImage(im, SQUARE)
        # greyIm = imf.makeGrayscale(croppedIm)

        greyIm = imf.makeGrayscale(im)

        reducedIm = imf.reduceQualityOfImage(greyIm, i*PERCENT_TO_REDUCE)
        
        colorDepth = '8bit'
        newName = nm.getProcessedFileName(fileName, qualityPercent, colorDepth)

        imf.saveImageAsBMP(reducedIm, newName, newPathOutput)

ff.loopTroughDirectory(PATH_INPUT, outputPath8Bit, loopTroughFunction)

# os.system('./Bitmapizer -convert')