from PIL import Image, ImageOps, ImageMath, ImageFilter, ImageGrab
import os
import img as img
from pathlib import Path
from itertools import product
from img import Filter
import create_overview_doc
import to_digits

if __name__ == "__main__":
    # Define input and output directories and create subfolders for each colour depth:
    PATH_INPUT = Path('input')
    PATH_OUTPUT = Path('output')
    PATH_INPUT.mkdir(exist_ok=True)

    # Clean up the output.
    for f in PATH_OUTPUT.glob('*.png'):
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

    # First we used find_best_steps_one.py to manually find some series of
    # transforms that resulted in a nice output for the sample.bmp image.
    # Now we choose one of the best performing series and use that on a 
    # lot of example images.

    # sample.bmp does not need to be croped so that step is added here
    # as a first step. After which we run a bunch of steps that I have
    # manually choosen.

    # The square that the program will cut out and use
    # The first two numbers represent upper left corner of the square
    # The last two numbers represent lower right corner of the square
    upper_left = (170, 250)
    lower_right = (747, 340)
    SQUARE = (*upper_left, *lower_right)

    # Here I have choosen something I belive in and want to run that on all images.
    steps = [
        Filter(lambda im: img.crop_image(im, SQUARE), 'crop'),
        Filter(ImageOps.invert, f'invert'),
        Filter(img.make_grayscale, f'{8}bits', bits=8),
        # Filter(img.make_grayscale, f'{1}bits', bits=1),
        Filter(lambda im: im.filter(ImageFilter.MedianFilter(3)), 'meadian_filter'),
        [Filter(img.reduce_quality_of_image, f'{quality_percent}ppt', reduce_percentage=(100 - quality_percent)) for quality_percent in [60]][0],
        Filter(lambda im: im.filter(ImageFilter.MedianFilter(3)), 'meadian_filter'),
        [Filter(img.reduce_quality_of_image, f'{quality_percent}ppt', reduce_percentage=(100 - quality_percent)) for quality_percent in [30]][0],
        # TODO wut is this and 255 stuff?
        Filter(lambda im: im.point(lambda p: p < 100 and 255), 'threshold_'),
        Filter(ImageOps.invert, f'invert'),
        Filter(img.make_grayscale, f'{1}bits', bits=1),
    ]

    for i, filename in enumerate(PATH_INPUT.glob('*.bmp')):
        if filename.name == 'sample.bmp': continue

        im = img.execute_steps_on_one_image(steps, im=Image.open(filename))

        digit_images = to_digits.to_digits(im)

        # picture22_00048221 -> correct digit
        _, correct_digits = filename.stem.split('_')
        for j, im in enumerate(digit_images):
            # if j in [5]: # the 6th digits is usually the one with most noice.
            # Store the final image, name the file according to the steps taken.
            # name_parts = [filename.stem] + [f.name for f in steps] + [f"digit=[{correct_digits[j]}]"]

            # Store image witha name containing information about the digit.
            name_parts = [filename.stem] + [f"pos={j}", f"digit={correct_digits[j]}"]
            im.save(PATH_OUTPUT / ('_'.join(name_parts) + '.png'))

        # if i > 10:
        #     break

    create_overview_doc.create_doc()