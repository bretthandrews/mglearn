import pytest
from marvin import config

from .context import mglearn

# import os
# import sys

# sys.path.append(os.path.join(os.path.expanduser('~'), 'projects', 'mangaML', 'python'))
# from mangaML.utils import data_access




def get_drpver(drpver, release):
    """Open DRPall file.
        
    Parameters:
        drpver (str):
            DRP version.
        release (str):
            MaNGA release (MPL or DR).
    
    Returns:
        drpver (str)
    """
    release = release if release is not None else config.release

    if ('MPL' in release) or ('DR' in release):
        config_drpver, __ = config.lookUpVersions(release)
    
    drpver = drpver if drpver is not None else config_drpver

    return drpver


@pytest.mark.parametrize('drpver, release, expected',
                         [('v1_5_1', None, 'v1_5_1'),
                          ('v1_5_1', 'MPL-4', 'v1_5_1'),
                          ('v1_5_1', 'MPL-5', 'v1_5_1'),
                          ('v2_0_1', None, 'v2_0_1'),
                          ('v2_0_1', 'MPL-4', 'v2_0_1'),
                          ('v2_0_1', 'MPL-5', 'v2_0_1'),
                          (None, 'MPL-4', 'v1_5_1'),
                          (None, 'MPL-5', 'v2_0_1')])
def test_get_drpver(drpver, release, expected):
    assert get_drpver(drpver, release) == expected
