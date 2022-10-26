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

#-------------------------------------------------------------------------

# Make bitmaps from the bin files and store them in the input folder:
# os.system('./Bitmapizer -bitmapize')


# Define input and output directories and create subfolders for each colour depth:
PATH_INPUT = Path('input')
PATH_OUTPUT = Path('output')

PATH_INPUT.mkdir(exist_ok=True)

def loop_through_function(file_path, filename, path_output, bits: int):
    # The quality of the picture in pixels, 100 is original quality.
    for quality_percent in range(10, 101, 10):
        im = Image.open(file_path / filename)

        # Removed crop since my sample image does not need it
        # croppedIm = imf.cropImage(im, SQUARE)
        # greyIm = imf.makeGrayscale(croppedIm)
        grey_im    = imf.make_grayscale(im, bits)
        reduced_im = imf.reduce_quality_of_image(grey_im, (100 - quality_percent))

        name = "_".join([Path(filename).stem, f'{bits}bit', f'{quality_percent}ppt']) + '.bmp'
        new_path_output = path_output / f"{quality_percent}ppt"
        ff.make_directory(new_path_output)
        reduced_im.save(new_path_output / name)

# This now seems to create 1bit and 8bit as expected.
# But pillow does not support 2bit or 4bit so those are missing.
for bits in [1, 8]:
    output_path = (PATH_OUTPUT / f'{bits}bit')
    output_path.mkdir(exist_ok=True)
    for file in PATH_INPUT.glob('*.bmp'):
        print(f'loop_through_directory ->On file: {file}')
        loop_through_function(PATH_INPUT, file.name, output_path, bits)


# os.system('./Bitmapizer -convert')