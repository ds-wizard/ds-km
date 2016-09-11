import pytest
import warnings
import os


reporoot = '.'             # TODO move to some common config
modelfolder = 'datamodel'  # TODO move to some common config


@pytest.fixture(scope='module')
def kmfs():
    '''KM FS representation in dictionary'''
    from helper.kmfs import kmfs2dict
    return kmfs2dict(os.path.join(reporoot, modelfolder))


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
