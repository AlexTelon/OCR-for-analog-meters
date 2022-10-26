from PIL import Image
import math
from pathlib import Path

def make_grayscale(im: Image) -> Image:
    return im.convert('L')

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