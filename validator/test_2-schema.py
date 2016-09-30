import pytest
from helper.chapters import load_chapter
from helper.schemas import *


def test_load_act_schema(schemas):
    load_schema(schemas, 'schema-chapter.json', 0)


def test_load_old_schemas(schemas):
    schema_files = list_chapter_schemas()
    for file in schema_files:
        load_schema(schemas, file, extract_schemaversion(file))


def test_valid_schemas(schemas):
    for schema in schemas.values():
        check_schema(schema)


# Test loading all chapter files as json
def check_chapter_file(chapters, chapterfile):
    load_chapter(chapters, chapterfile)


def test_core_chapter_json(kmfs, chapters):
    for chapterfile in kmfs['dirs']['core']['files']:
        check_chapter_file(chapters, chapterfile)


def test_local_chapter_json(kmfs, chapters):
    for ns in kmfs['dirs']['local']['dirs']:
        for chapterfile in kmfs['dirs']['local']['dirs'][ns]['files']:
            check_chapter_file(chapters, chapterfile)


# TODO test checking all chapter files via schema (or older schema with
#      warning, decide version by "formatversion attribute")
def test_chapters_valid(chapters, schemas):
    v = get_validator(schemas[0])
    for chapterfile, chapter in chapters.items():
        v.validate(chapter)
