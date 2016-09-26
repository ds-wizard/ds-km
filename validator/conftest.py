import pytest
import os

reporoot = '.'
modelfolder = 'datamodel'


@pytest.fixture(scope='session')
def kmfs():
    '''KM FS representation in dictionary'''
    from helper.kmfs import kmfs2dict
    return kmfs2dict(os.path.join(reporoot, modelfolder))


@pytest.fixture(scope='session')
def chapters():
    '''Chapters JSON data container'''
    return dict()


@pytest.fixture(scope='session')
def km():
    '''KM data container'''
    return dict()


@pytest.fixture(scope='session')
def schemas():
    '''JSON schemas container'''
    return dict()
