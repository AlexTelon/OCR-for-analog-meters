from glob import glob
from pathlib import Path
import shutil
import os
# Move images from output to samples folder
# for file in glob('output/**/*.bmp', recursive=True):
#     # file = Path(file)
#     shutil.copy(file, 'samples')

files = list(glob('output/**/*.bmp', recursive=True))

# print a markdown table with all images.
output = []
for file in glob('output/**/*.bmp', recursive=True):
    short = Path(file).stem
    short = short.replace('sample_','').replace('ppt','%').replace('_', ' ')
    # if '10%' in short:
    size = os.path.getsize(file)
    output.append((size, f"{size:,} bytes | {short} | ![{short}]({file})"))

output = sorted(output)

output = [(size, f"{i} | "+name) for i, (size, name) in enumerate(output)]

with open('output_overview.md', 'w') as f:
    content = ''
    content += 'i | Size | Conversions and order | Image\n'
    content += '---|-------|-------|-------\n'
    content += '\n'.join(name for _, name in output)
    f.write(content)
