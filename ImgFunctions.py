from PIL.Image import Image
import math
from pathlib import Path
from typing import List, Callable, Iterable, Tuple
from itertools import combinations, product, permutations

class Filter:
    def __init__(self, func, name, **kwargs):
        self.func = func
        self.name = name
        self.kwargs = kwargs

    def __call__(self, im: Image) -> Image:
        return self.func(im, **self.kwargs)


def execute_steps_on_one_image(steps: List[Callable[[Image], Image]], im: Image):
    # Run all steps.
    for func in steps:
        im = func(im)
    return im


def execute_reordered_combinations_on_one_image(options: List[List[Callable[[Image], Image]]], im: Image) -> Iterable[Tuple[List[Filter], Image]]:
    for steps in product(*options):
        # Run all combinations on one image
        for comb in permutations(steps):
            yield (comb, execute_steps_on_one_image(comb, im))


def make_grayscale(im: Image, bits: int) -> Image:
    if bits not in [1, 8]:
        raise NotImplementedError(f"make_grayscale does not support {bits} bits")
    return im.convert('L' if bits == 8 else '1')

def crop_image(im: Image, box) -> Image:
    return im.crop(box)

def save_iamge_as_bmp(im: Image, fileName: str, path: Path) -> None:
    im.save(path / (fileName+'.bmp'))

def reduce_quality_of_image(im: Image, reduce_percentage: float) -> Image:
    if reduce_percentage < 0:
        return im
    width, height = im.size

    #The real percent, in decimal form, to reduce width and height with to get the proper percent reduction
    real_percent = math.sqrt(1 - (reduce_percentage / 100))

    newWidth = int(round(width * real_percent))
    newHeight = int(round(height * real_percent))
    
    newSize = (newWidth, newHeight)
    reducedIm = im.resize(newSize)
    return reducedIm