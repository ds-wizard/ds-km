import pytest
from helper.km import *

#TODO: refactor:
#     - error msgs file
#     - non-blocking errors (more smaller tests)
#     - nicer code, easier to read (OOP?)


def test_load_chapters(chapters, km):
    for chapter in chapters.values():
        load_chapter(km, chapter)


def test_uuid_uniqueness(km):
    build_uuid_dict(km)


def test_referencing(km):
    items = build_uuid_dict(km)
    for uuid, item in items.items():
        if 'precondition' in item:  # question precondition
            precd = item['precondition']
            assert not uuid == precd
            assert precd in items.keys()
            assert items[precd][0] in ('question', 'answer')
        if 'target' in item:  # crossreference (xref)
            target = item['target']
            assert not uuid == target
            assert target in items.keys()
            assert items[target][0] in ('question', 'answer')
