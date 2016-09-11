import pytest
import json
import jsonschema
import os
from helper.kmfs import is_chapter


# TODO test loading actual schema


# TODO test loading archived schema (in /schema folder)


# Test loading all chapter files as json
def check_chapter_file(chapterfile):
    if not is_chapter(chapterfile):
        return  # skip unknown files
    with open(chapterfile, mode='r') as f:
        result = json.load(f)  # TODO: catch and provide nicer info


def test_core_chapter_json(kmfs):
    for chapterfile in kmfs['dirs']['core']['files']:
        check_chapter_file(chapterfile)


def test_local_chapter_json(kmfs):
    for ns in kmfs['dirs']['local']['dirs']:
        for chapterfile in kmfs['dirs']['local']['dirs'][ns]['files']:
            check_chapter_file(chapterfile)

# TODO test checking all chapter files via schema (or older schema with
#      warning, decide version by "formatversion attribute")
