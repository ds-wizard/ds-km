import json
from helper.kmfs import is_chapter


def load_chapter(chapters, chapterfile):
    if is_chapter(chapterfile):
        with open(chapterfile, mode='r') as f:
            chapters[chapterfile] = json.load(f)
