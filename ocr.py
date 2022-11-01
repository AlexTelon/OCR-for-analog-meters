from PIL import Image, ImageOps
from pathlib import Path
from collections import defaultdict
import create_overview_doc
from glob import glob

def create_digit_images(path_output):
    # TODO this assuems that output contains those 2000 images that main.py can generate atm.
    # Should refator the current main code to a new file that generates those on demand.

    directory = Path('output')
    files = directory.glob('*.png')

    # ensure that directory contains the type of files we expect
    assert directory/'picture4_00048174_pos=7_digit=4.png' in files, "sanity check failed!"

    path_output = Path('digits_images')
    path_output.mkdir(exist_ok=True)
    
    # Create output directories for each digit 0..9
    for i in range(0, 10):
        (path_output / f"{i}").mkdir(exist_ok=True)

    images = defaultdict(list)
    for i, filename in enumerate(files):
        _, _, pos, digit = filename.stem.split('_')
        digit = int(digit.strip('digit='))
        
        im = Image.open(filename)
        images[digit].append(im.crop(im.getbbox()))
        # images[digit].append(im)
        im.save(path_output / f"{digit}" / f"{filename.name}")

# def get_digit_images():
#     files = glob('output/**/*.png')

#     images = defaultdict(list)
#     for i, filename in enumerate(files):
#         _, _, pos, digit = filename.stem.split('_')
#         digit = int(digit.strip('digit='))
        
#         im = Image.open(filename)
        
#         box = Image.getbbox(im)
#         images[digit].append(im.crop(box))

def print_pixels(im: Image.Image):
    for row in get_rows(im):
        row = ['.#'[x==255] for x in row]
        print(''.join(row))

def get_rows(im: Image.Image):
    width, height = im.size
    data = list(im.getdata())

    rows = [data[y*width:(y+1)*width] for y in range(height)]
    return rows

if __name__ == "__main__":
    # PATH_OUTPUT = Path('digits_images')
    # create_digit_images(PATH_OUTPUT)
    # create_overview_doc.create_doc(f"{PATH_OUTPUT}/**/*.png")

    files = list(Path('digits_images').glob('**/*.png'))

    digit_images = defaultdict(list)
    sizes = set()

    n = len(files)
    for i, filename in enumerate(files):
        _, _, pos, digit = filename.stem.split('_')
        digit = int(digit.strip('digit='))
        
        im = Image.open(filename)
        sizes.add(im.size)

        # get a cropped image
        # im = ImageOps.invert(im)
        # im = im.crop(im.getbbox())
        # im = ImageOps.invert(im)

        digit_images[digit].append(im)

        # Train on first 80%, compare against the rest.
        # if i > 0.8 * n:
        #     break

        # print_pixels(im)
        # print()
    assert len(sizes) == 1
    width, height = sizes.pop()

    def print_grid(grid):
        for row in grid:
            # print(' '.join(f"{x:.1f}" if x != 0 else ' ' for x in row))
            print(' '.join(f"{x:.1f}" if x > 0.2 else '   ' for x in row))

    # Produce a heatmap.
    for i in range(10):
        grid = [[0] * width for _ in range(height)]
        
        for im in digit_images[i]:
            for y, row in enumerate(get_rows(im)):
                for x, value in enumerate(row):
                    grid[y][x] += [0,1][value == 0]
        
        n = len(digit_images[i])
        if n == 0:
            print(f"{i} is 0")
        else:
            for y, row in enumerate(grid):
                for x, value in enumerate(row):
                    grid[y][x] /= n

            print_grid(grid)
            print()
