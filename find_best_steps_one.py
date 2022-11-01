from PIL import Image, ImageOps, ImageMath, ImageFilter, ImageGrab
import os
import img as img
from pathlib import Path
from img import Filter
import create_overview_doc

# All the quality reducing variants in a list.
# quality_funcs = [Filter(img.reduce_quality_of_image, f'{quality_percent}ppt', reduce_percentage=(100 - quality_percent)) for quality_percent in range(1, 20, 1)]
quality_funcs = [Filter(img.reduce_quality_of_image, f'{quality_percent}ppt', reduce_percentage=(100 - quality_percent)) for quality_percent in [5, 10]]
# All the to_grayscale variants in a list.
greyscale_funs = [Filter(img.make_grayscale, f'{bits}bits', bits=bits) for bits in [1,8]]
invert_funcs = [Filter(ImageOps.invert, f'invert')]

# blur did not work well
blur_funcs = [
    Filter(lambda im: im.filter(ImageFilter.BLUR), 'blur'),
    Filter(lambda im: im, '')
    ]

minfilter_funcs = [
    Filter(lambda im: im.filter(ImageFilter.MinFilter(1)), 'minfilter_1'),
    Filter(lambda im: im.filter(ImageFilter.MedianFilter()), 'meadian_filter'),
    Filter(lambda im: im.filter(ImageFilter.MaxFilter(1)), 'maxfilter_1'),
    Filter(lambda im: im.filter(ImageFilter.ModeFilter(1)), 'modefilter_1'),
    Filter(lambda im: im, '')
    ]

thresholds = [Filter(lambda im: im.point(lambda p: p < limit and 255), f'threshold_{limit}') for limit in range(0, 150, 10)]

if __name__ == "__main__":
    # This file will try a lot of combinations on the sample.bmp image
    # and generate a report showing the results.

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

    options = [
        [Filter(img.make_grayscale, f'{8}bits', bits=8)],
        quality_funcs,
        # greyscale_funs,
        # blur_funcs,
        invert_funcs,
        # minfilter_funcs,
        thresholds,
        [Filter(img.make_grayscale, f'{1}bits', bits=1)],
    ]

    im = Image.open(PATH_INPUT / 'sample.bmp')
    images = img.execute_reordered_combinations_on_one_image(options, im)

    for steps, im in images:
        # Store the final image, name the file according to the steps taken.
        im.save(PATH_OUTPUT / ('_'.join(f.name for f in steps) + '.png'))

    create_overview_doc.create_doc()