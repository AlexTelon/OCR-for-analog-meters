from PIL import Image, ImageOps, ImageMath, ImageFilter, ImageGrab
import os
import ImgFunctions as imf
from pathlib import Path
from typing import List, Callable
from itertools import combinations, product, permutations

class Filter:
    def __init__(self, func, name, **kwargs):
        self.func = func
        self.name = name
        self.kwargs = kwargs

    def __call__(self, im: Image.Image) -> Image.Image:
        return self.func(im, **self.kwargs)

# All the quality reducing variants in a list.
# quality_funcs = [Filter(imf.reduce_quality_of_image, f'{quality_percent}ppt', reduce_percentage=(100 - quality_percent)) for quality_percent in range(1, 20, 1)]
quality_funcs = [Filter(imf.reduce_quality_of_image, f'{quality_percent}ppt', reduce_percentage=(100 - quality_percent)) for quality_percent in [5, 10]]
# All the to_grayscale variants in a list.
greyscale_funs = [Filter(imf.make_grayscale, f'{bits}bits', bits=bits) for bits in [1,8]]
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


def execute_steps_on_one_image(steps: List[Callable[[Image.Image], Image.Image]], im: Image.Image):
    # Run all steps.
    for func in steps:
        im = func(im)

    # Store the final image, name the file according to the steps taken.
    im.save(PATH_OUTPUT / ('_'.join(f.name for f in steps) + '.png'))


def execute_reordered_combinations_on_one_image(options: List[List[Callable[[Image.Image], Image.Image]]], im: Image.Image):
    for steps in product(*options):
        # Run all combinations on one image
        for comb in permutations(steps):
            execute_steps_on_one_image(comb, im)


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


    options = [
        quality_funcs,
        greyscale_funs,
        # blur_funcs,
        invert_funcs,
        minfilter_funcs,
    ]

    im = Image.open(PATH_INPUT / 'sample.bmp')
    execute_reordered_combinations_on_one_image(options, im)
    exit()

    # The square that the program will cut out and use
    # The first two numbers represent upper left corner of the square
    # The last two numbers represent lower right corner of the square
    # SQUARE = (130, 300, 270, 370)
    SQUARE = (170, 250, 747, 340)

    if False:
        options = [
            # [Filter(lambda im: imf.crop_image(im, SQUARE), 'crop')],
            invert_funcs,
            [Filter(imf.make_grayscale, f'{1}bits', bits=1)],
            [Filter(lambda im: im.filter(ImageFilter.MedianFilter(i)), f'meadian_filter_{i}') for i in [3,5]],
            [Filter(imf.reduce_quality_of_image, f'{quality_percent}ppt', reduce_percentage=(100 - quality_percent)) for quality_percent in range(10, 101, 10)],
            [Filter(lambda im: im.filter(ImageFilter.MedianFilter(i)), f'meadian_filter_{i}') for i in [3,5]],
            [Filter(imf.reduce_quality_of_image, f'{quality_percent}ppt', reduce_percentage=(100 - quality_percent)) for quality_percent in range(10, 101, 10)],
        ]
        for steps in product(*options):
            execute_steps_on_one_image(steps)
        exit()

    # Here I have choosen something I belive in and want to run that on all images.
    steps = [
        Filter(lambda im: imf.crop_image(im, SQUARE), 'crop'),
        invert_funcs[0],
        Filter(imf.make_grayscale, f'{1}bits', bits=1),
        # blur_funcs,
        Filter(lambda im: im.filter(ImageFilter.MedianFilter(3)), 'meadian_filter'),
        [Filter(imf.reduce_quality_of_image, f'{quality_percent}ppt', reduce_percentage=(100 - quality_percent)) for quality_percent in [60]][0],
        Filter(lambda im: im.filter(ImageFilter.MedianFilter(3)), 'meadian_filter'),
        [Filter(imf.reduce_quality_of_image, f'{quality_percent}ppt', reduce_percentage=(100 - quality_percent)) for quality_percent in [30]][0],
    ]

    for i, filename in enumerate(PATH_INPUT.glob('*.bmp')):
        if filename.name == 'sample.bmp': continue
        im = Image.open(filename)

        # Run all steps.
        for func in steps:
            im = func(im)

        # Store the final image, name the file according to the steps taken.
        im.save(PATH_OUTPUT / (filename.stem + '_'.join(f.name for f in steps) + '.png'))
        if i > 10:
            break
