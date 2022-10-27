from glob import glob
from pathlib import Path
import shutil
import os
from collections import defaultdict
# Move images from output to samples folder
# for file in glob('output/**/*.bmp', recursive=True):
#     # file = Path(file)
#     shutil.copy(file, 'samples')

files = list(glob('output/**/*.bmp', recursive=True))

# print a markdown table with all images.
generated_files = defaultdict(list)
# output = []
for file in glob('output/**/*.bmp', recursive=True):
    short_name = Path(file).stem
    short_name = short_name.replace('sample_','').replace('ppt','%')
    size = os.path.getsize(file)

    with open(file, 'rb') as f:
        content = f.read()
        _hash = hash(content)

    generated_files[_hash].append((size, short_name, file))
    # output.append((size, f"{size:,} bytes | {short} | ![{short}]({file})"))

# There may be multiple ways to get the same file.
# Here we add them to the same row.
output = []
for hash, items in generated_files.items():
    names = [name for _, name, _ in items]
    size, _, file = items[0]
    # <br/> is how we add newlines within a cell in markdown
    output.append((size, '<br/>'.join(names), file))

# Sort on size
output = sorted(output)

# Add a running number to the first column.
output = [((i,) + cols) for i, cols in enumerate(output)]

# f"{size:,} bytes | {short} | ![{short}]({file})"

with open('output_overview.md', 'w') as f:
    content = ''
    content += 'i | Size | Conversions and order | Image\n'
    content += '---|-------|-------|-------\n'
    for i, size, short_name, file in output:
        row = f"{i} | {size:,} bytes | {short_name} | ![{i}]({file})"
        content += row + '\n'
        # content += '\n'.join(name for _, name in output)
    f.write(content)
