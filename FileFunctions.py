from os import path
import os
import sys
from pathlib import Path

def get_abs_path(relative_path):
    """Returns the absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', Path().absolute())
    return path.join(base_path, relative_path)

def make_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def loop_through_directory(path_input, path_output, loop_function):
    for filename in os.listdir(path_input):
        if filename.endswith(".bmp"):
            print('loop_through_directory ->On file: ' + filename)
            loop_function(path_input, filename, path_output)