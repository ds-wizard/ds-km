import pytest
from helper.kmfs import is_chapter, extract_chapterid


# Test if folder name == namespace in chapter file
def check_folder_namespace(chapters, ch, ns):
    if ch in chapters:
        in_file = chapters[ch]['namespace']
        assert ns == in_file,\
               'Namespace "{}" does not match related folder "{}" in {}'.\
               format(in_file, ns, ch)


def test_folders_namespaces_core(kmfs, chapters):
    for ch in kmfs['dirs']['core']['files']:
        check_folder_namespace(chapters, ch, 'core')


def test_folders_namespaces_local(kmfs, chapters):
    for ns in kmfs['dirs']['local']['dirs']:
        for ch in kmfs['dirs']['local']['dirs'][ns]['files']:
            check_folder_namespace(chapters, ch, ns)
