import pytest
from helper.km import *


def test_load_chapters(chapters, km):
    for chapter in chapters.values():
        load_chapter(km, chapter)

# TODO: check namespace (on question) references
def test_local_questions():
    pass


# TODO: check precondition references
def test_preconditions():
    pass

# TODO: check questionpointer references
def test_questionpointers():
    pass


# TODO: check crossreferences
def test_xrefs():
    pass
