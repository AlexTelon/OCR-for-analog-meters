from PIL import Image, ImageOps
from pathlib import Path
from collections import defaultdict
import create_overview_doc
from glob import glob
import random


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


def print_pixels(im: Image.Image):
    for row in get_rows(im):
        row = ['.#'[x==255] for x in row]
        print(''.join(row))


def get_rows(im: Image.Image):
    width, height = im.size
    data = list(im.getdata())

    rows = [data[y*width:(y+1)*width] for y in range(height)]
    return rows

def to_grid(im: Image.Image):
    grid = get_rows(im)
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            grid[y][x] = [0,1][value == 0]
    return grid


def produce_heatmap(images):
    grid = [[0] * width for _ in range(height)]
    n = len(images)

    for im in images:
        for y, row in enumerate(get_rows(im)):
            for x, value in enumerate(row):
                grid[y][x] += [0,1][value == 0]
    
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            grid[y][x] /= n
    return grid


def print_grid(grid):
    for row in grid:
        # print(' '.join(f"{x:.1f}" if x != 0 else ' ' for x in row))
        print(' '.join(f"{x:.1f}" if x > 0.2 else '   ' for x in row))

def _dist(A, B):
    diffs = 0
    for aa, bb in zip(A, B):
        for a, b in zip(aa, bb):
            diffs += abs(a - b)
    return diffs

def dist(A, B):
    # Move A around over B to find the best overlap!
    # Not implemented yet though
    return _dist(A, B)

def closest(grid, heatmap):
    distances = {}
    for key, ref in heatmap.items():
        distances[key] = dist(ref, grid)

    # for key, value in distances.items():
    #     print(key, value)

    digit, _ = min(distances.items(), key=lambda x: x[1])
    return digit


if __name__ == "__main__":
    # PATH_OUTPUT = Path('digits_images')
    # create_digit_images(PATH_OUTPUT)
    # create_overview_doc.create_doc(f"{PATH_OUTPUT}/**/*.png")

    files = list(Path('digits_images').glob('**/*.png'))
    random.shuffle(files)

    images = []
    sizes = set()
    for i, filename in enumerate(files):
        _, _, pos, digit = filename.stem.split('_')
        digit = int(digit.strip('digit='))
        
        im = Image.open(filename)
        sizes.add(im.size)

        # get a cropped image
        # im = ImageOps.invert(im)
        # im = im.crop(im.getbbox())
        # im = ImageOps.invert(im)
        images.append((digit, im))


    n = len(images)
    training_files   = images[:round(n*0.8)]
    validation_files = images[round(n*0.8):]

    training_images = defaultdict(list)
    for digit, im in training_files:
        training_images[digit].append(im)

    validation_images = defaultdict(list)
    for digit, im in validation_files:
        validation_images[digit].append(im)

    assert len(sizes) == 1
    width, height = sizes.pop()

    # Produce a heatmap.
    heatmap = {}
    for i in range(10):
        grid = produce_heatmap(training_images[i])
        heatmap[i] = grid

    results = []
    for digit, im in validation_files:
        grid = to_grid(im)
        guess = closest(grid, heatmap)
        print(f"correct: {digit}, guess: {guess} ", "Ok!" if guess == digit else '')
        results.append(guess == digit)
    
    accuracy = sum(results) / len(results)
    print(f"{accuracy:%}")

    # for digit, grid in heatmap.items():
    #     print_grid(grid)
    #     print()
