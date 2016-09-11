import pytest
import os
from helper.chapters import load_chapter


# TODO test loading actual schema


# TODO test loading archived schema (in /schema folder)


# Test loading all chapter files as json
def check_chapter_file(chapters, chapterfile):
    load_chapter(chapters, chapterfile)  # TODO: catch and provide nicer info


def test_core_chapter_json(kmfs, chapters):
    for chapterfile in kmfs['dirs']['core']['files']:
        check_chapter_file(chapters, chapterfile)


def test_local_chapter_json(kmfs, chapters):
    for ns in kmfs['dirs']['local']['dirs']:
        for chapterfile in kmfs['dirs']['local']['dirs'][ns]['files']:
            check_chapter_file(chapters, chapterfile)


# TODO test checking all chapter files via schema (or older schema with
#      warning, decide version by "formatversion attribute")
