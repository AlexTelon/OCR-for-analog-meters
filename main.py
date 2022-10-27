from PIL import Image, ImageOps, ImageMath, ImageFilter
import os
import ImgFunctions as imf
import FileFunctions as ff
from pathlib import Path
from typing import List, Callable
from functools import partial
from itertools import combinations, product, permutations

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

# clean up the output 
for f in PATH_OUTPUT.glob('*.bmp'):
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))

# def loop_through_function(im: Image.Image, steps: List[Callable[[Image.Image], Image.Image]]) -> Image.Image:
#     for step in steps:
#         im = step(im)
#     return im

#     # Looking at how to do manual tresholds in pillow.
#     # multibands = im.split()
#     # red      = multibands[0].point(lambda intensity: intensity)
#     # green    = multibands[1].point(lambda intensity: intensity)
#     # blue     = multibands[2].point(lambda intensity: intensity)
#     # # red = ImageMath.eval("", a = red)
#     # im = Image.merge("RGB", (red, green, blue))

#     # Removed crop since my sample image does not need it
#     # croppedIm = imf.cropImage(im, SQUARE)
#     # greyIm = imf.makeGrayscale(croppedIm)
#     # im = imf.reduce_quality_of_image(im, (100 - quality_percent))
#     # im = imf.make_grayscale(im, bits)

#     # Try to despeckle the image
#     # im = im.filter(ImageFilter.BLUR)
#     # im = im.filter(ImageFilter.MinFilter(3))
#     # im = im.filter(ImageFilter.MinFilter)

#     # Invert image
#     # im = ImageOps.invert(im)

#     # name = "_".join([Path(filename).stem, f'{bits}bit', f'{quality_percent}ppt']) + '.bmp'
#     # new_path_output = path_output / f"{quality_percent}ppt"
#     # ff.make_directory(new_path_output)
#     # im.save(new_path_output / name)

class Filter:
    def __init__(self, func, name, **kwargs):
        self.func = func
        self.name = name
        self.kwargs = kwargs

    def __call__(self, im: Image.Image) -> Image.Image:
        return self.func(im, **self.kwargs)

    # def __str__(self):
    #     return f"{self.name}"

# All the quality reducing variants in a list.
quality_funcs = [Filter(imf.reduce_quality_of_image, f'{quality_percent}ppt', reduce_percentage=(100 - quality_percent)) for quality_percent in range(10, 101, 10)]
# All the to_grayscale variants in a list.
greyscale_funs = [Filter(imf.make_grayscale, f'{bits}bits', bits=bits) for bits in [1,8]]
invert_funcs = [Filter(ImageOps.invert, f'invert')]


steps = []
for steps in product(quality_funcs, greyscale_funs, invert_funcs):
    for comb in permutations(steps):
        im = Image.open(PATH_INPUT / 'sample.bmp')

        # Run all steps.
        for func in comb:
            im = func(im)

        # Store the final image, name the file according to the steps taken.
        im.save(PATH_OUTPUT / ('_'.join(f.name for f in comb) + '.bmp'))

# This now seems to create 1bit and 8bit as expected.
# But pillow does not support 2bit or 4bit so those are missing.
# for bits in [1, 8]:
#     output_path = (PATH_OUTPUT / f'{bits}bit')
#     output_path.mkdir(exist_ok=True)
#     for file in PATH_INPUT.glob('*.bmp'):
#         print(f'loop_through_directory ->On file: {file}')
#         loop_through_function(PATH_INPUT, file.name, output_path, bits)


# os.system('./Bitmapizer -convert')