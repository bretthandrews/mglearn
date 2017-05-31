"""
Select sample of MaNGA galaxies.
"""

from __future__ import division, print_function, absolute_import
import os
import copy
from collections import defaultdict

import numpy as np
from astropy.io import fits


# See Marvin docs for details on how to download MaNGA galaxies
# http://sdss-marvin.readthedocs.io/en/latest/core/downloads.html

def set_drpver(drpver=None, release=None):
    
    from marvin import config
    
    assert not ((drpver is not None) and (release is not None)), \
        ('Both ``drpver`` and ``release`` are set (drpver: {0}, release: {1}).  '
         'Only set one of them.'.format(drpver, release))

    drpver_ = drpver
    if drpver is not None:
        release = config.lookUpRelease(drpver)
    
    if release is not None:
        config.setRelease(release)
    
    drpver, __ = config.lookUpVersions()
    
    if drpver_ is not None:
        assert drpver == drpver_, 'DRP versions do not match.'
    
    return drpver


def read_drpall(drpver=None, release=None, path_drpall=None):
    drpver = set_drpver(drpver, release)

    if path_drpall is None:
        path_drpall = os.path.join(os.environ['MANGA_SPECTRO_REDUX'], drpver)

    drpall_file = os.path.join(path_drpall, 'drpall-{}.fits'.format(drpver))
    data = fits.getdata(drpall_file, 1)
    return data


def apply_bitmasks(data, bits):
    subsamples = [data & 2**bit for bit in bits]
    return np.logical_or.reduce(subsamples)


def remove_duplicates(plateifus, mangaids, sn2):
    # keys are unique mangaids and values are indices within ``mangaids`` array
    mangaid_lookup = defaultdict(list)
    for ii, item in enumerate(mangaids):
        mangaid_lookup[item].append(ii)

    # keys are duplicate mangaids and values are indices within ``mangaids``
    duplicates = {k: v for k, v in mangaid_lookup.items() if len(v) > 1}

    uniques = copy.deepcopy(mangaid_lookup)
    for kk, vv in duplicates.items():
        # Choose plateifu with highest SN2 (sum of blueSN2 and redSN2)
        uniques[kk] = [vv[np.argmax(sn2[vv])]]

    inds = np.array([it for val in uniques.values() for it in val])
    return plateifus[inds]


def write(plateifus, filepath, header=None):
    with open(filepath, 'w') as fout:
        if header is not None:
            fout.write(header)

        for plateifu in plateifus:
            fout.write('{0}\n'.format(plateifu))
