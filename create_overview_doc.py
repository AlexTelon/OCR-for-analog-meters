from glob import glob
from pathlib import Path
import shutil
# Move images from output to samples folder
# for file in glob('output/**/*.bmp', recursive=True):
#     # file = Path(file)
#     shutil.copy(file, 'samples')

files = list(glob('output/**/*.bmp', recursive=True))

# print a markdown table with all images.
output = []
output.append('Conversion | image')
output.append('----------|----------')
for file in glob('output/**/*.bmp', recursive=True):
    short = Path(file).stem
    short = short.replace('sample_','').replace('ppt','%').replace('_', ' ')
    if '10%' in short:
        output.append(f"{short} | ![{short}]({file})")

with open('output_overview.md', 'w') as f:
    content = '\n'.join(output)
    f.write(content)
