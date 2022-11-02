# What is this

Its one of 4 repositories for this [thesis paper](http://hj.diva-portal.org/smash/get/diva2:1679951/FULLTEXT01.pdf).


# How to run

This is still very much WIP. But install requirements like this:

```bash
python -m venv .env
source .env/bin/activate
python -m pip install -r requirements

# Note that running these scripts will create these two folders
# output/
# intput/
# Also stuff in output may be deleted by these scripts.
```

[find_best_steps_one.py](find_best_steps_one.py) can be used to find a nice combination of transforms to be made on an image.

[create_overview_doc.py](create_overview_doc.py) finds all `.png` files in the output folder and produce a markdown and html dokument with all images in a nice table for a quick overview.

[ocr.py](ocr.py) my attempts at ocr.

[main.py](main.py) is ever changing. Dont trust it.