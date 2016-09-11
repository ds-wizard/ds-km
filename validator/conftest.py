import pytest
import os

reporoot = '.'
modelfolder = 'datamodel'


@pytest.fixture(scope='session')
def kmfs():
    '''KM FS representation in dictionary'''
    from helper.kmfs import kmfs2dict
    return kmfs2dict(os.path.join(reporoot, modelfolder))


# TODO: KM/JSON container for loaded chapters as fixture
