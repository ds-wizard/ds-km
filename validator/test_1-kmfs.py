import pytest
import warnings
import os


def test_core(kmfs):
    assert 'core' in kmfs['dirs'],\
           '"core" folder not found in the root of KM'
    assert len(kmfs['dirs']['core']['dirs']) == 0,\
           '"core" folder must not contain subfolders'


def test_local(kmfs):
    assert 'local' in kmfs['dirs'],\
           '"local" folder not found in the root of KM'
    assert 'core' not in kmfs['dirs']['local']['dirs'],\
           '"core" can not be name of folder in "local"'
