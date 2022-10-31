from PIL import Image
from typing import List

def to_digits(im: Image.Image) -> List[Image.Image]:
    """Hardcoded for our 8-digit analogue meters for now."""
    width = im.width // 8
    images = []
    for i in range(8):
        box = (width * i, 0, width * (i+1), im.height)
        images.append(im.crop(box))
    return images

if __name__ == "__main__":
    from pathlib import Path
    import os
    import create_overview_doc

    PATH_INPUT = Path('input')
    PATH_OUTPUT = Path('output')

    # Clean up the output.
    for f in PATH_OUTPUT.glob('*.png'):
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

    im = Image.open(PATH_INPUT / 'sample.bmp')
    im.save(PATH_OUTPUT / f'original.png')
    images = to_digits(im)

    for i, im in enumerate(images):
        im.save(PATH_OUTPUT / f'digit_{i}.png')

    create_overview_doc.create_doc()