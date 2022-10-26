from PIL import Image
import os
import ImgFunctions as imf
import FileFunctions as ff
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
output_path_8bit = (PATH_OUTPUT / '8bit')

def loop_through_function(file_path, filename, path_output):
    for i in range(0, AMMOUNT_OF_STEPS+1):
        # the quality of the picture in pixels, 100 is orgininal quality
        quality_percent = 100 - (i * PERCENT_TO_REDUCE)

        new_path_output = path_output / f"{quality_percent}ppt"
        ff.make_directory(new_path_output)
        im = Image.open(file_path / filename)

        # Removed crop since my sample image does not need it
        # croppedIm = imf.cropImage(im, SQUARE)
        # greyIm = imf.makeGrayscale(croppedIm)

        grey_im    = imf.make_grayscale(im)
        reduced_im = imf.reduce_quality_of_image(grey_im, i*PERCENT_TO_REDUCE)

        name = "_".join([Path(filename).stem, '8bit', f'{quality_percent}ppt'])
        imf.save_iamge_as_bmp(reduced_im, name, new_path_output)

for file in PATH_INPUT.glob('*.bmp'):
    print(f'loop_through_directory ->On file: {file}')
    loop_through_function(PATH_INPUT, file.name, output_path_8bit)

# os.system('./Bitmapizer -convert')