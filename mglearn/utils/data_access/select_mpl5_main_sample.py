"""
Select MaNGA MPL-5 Main Sample galaxies.
"""

import os
import copy
from collections import defaultdict

import numpy as np
from astropy.io import fits

from marvin import config


def make_filepath(plateifu, dltype):
    """Create SAS file path within manga/spectro/ directory.
    
    To recreate the full path at Utah, append to
    /uufs/chpc.utah.edu/common/home/sdss/mangawork/manga/ .
    """
    plate, ifu = plateifu.split('-')
    
    stack = os.path.join('redux', 'v2_0_1', plate, 'stack')
    spx_plateifu = os.path.join('analysis', 'v2_0_1', '2.0.2', 'SPX-GAU-MILESHC', plate, ifu)
    
    if dltype in ['LOGCUBE', 'LOGRSS']:
        return os.path.join(stack, 'manga-{0}-{1}.fits.gz'.format(plateifu, dltype))
    elif dltype == 'images':
        return os.path.join(stack, 'images', '{}.png'.format(ifu))
    elif dltype == 'maps':
        return os.path.join(spx_plateifu, 'manga-{0}-MAPS-SPX-GAU-MILESHC.fits.gz'.format(plateifu))
    else:
        raise ValueError('Invalid dltype: {}.'.format(dltype))


# See Marvin docs for details on how to download MaNGA galaxies
# http://sdss-marvin.readthedocs.io/en/latest/core/downloads.html
config.setRelease('MPL-5')

# Download DRPall file from
# https://data.sdss.org/sas/mangawork/manga/spectro/redux/MPL-5/drpall-v2_0_1.fits
drpall_path = os.path.join(os.path.expanduser('~'), 'manga', 'spectro', 'redux', 'v2_0_1')
drpall = fits.open(os.path.join(drpall_path, 'drpall-v2_0_1.fits'))
data = drpall[1].data

# How to select all main survey galaxies:
# http://www.sdss.org/dr13/algorithms/bitmasks/#MANGA_TARGET1

# primary sample: 1278 galaxies
# secondary sample: 947 galaxies
# color enhanced sample: 447 galaxies
# main sample: 2672 galaxies
primary = data['mngtarg1'] & 2**10
secondary = data['mngtarg1'] & 2**11
color_enhanced = data['mngtarg1'] & 2**12
main_sample = np.logical_or.reduce((primary, secondary, color_enhanced))

plateifus = data['plateifu'][main_sample]
mangaids = data['mangaid'][main_sample]

sn2 = data['bluesn2'] + data['redsn2']


# Remove duplicate galaxies
# keys are unique mangaids and values are indices within `mangaids` array
mangaid_lookup = defaultdict(list)
for ii, item in enumerate(mangaids):
    mangaid_lookup[item].append(ii)

# keys are duplicate mangaids and values are indices within `mangaids`
duplicates = {k: v for k, v in mangaid_lookup.items() if len(v) > 1}

uniques = copy.deepcopy(mangaid_lookup)
for kk, vv in duplicates.items():
    # Choose plateifu with highest SN2 (sum of blueSN2 and redSN2)
    uniques[kk] = [vv[np.argmax(sn2[vv])]]

inds = np.array([it for vv in uniques.values() for it in vv])
plateifus_uniques = plateifus[inds]


samples_dir = os.path.join(os.path.expanduser('~'), 'projects', 'mangaML', 'data', 'samples')


with open(os.path.join(samples_dir, 'mpl5_main_sample.txt'), 'w') as fout:
    fout.write('# MPL-5 Main Sample (Primary, Secondary, and Color Enhanced galaxies)\n')
    for plateifu in plateifus_uniques:
        fout.write('{0}\n'.format(plateifu))


# Write MPL-5 Main Sample filepaths to file
for dltype in ['LOGCUBE', 'LOGRSS', 'images', 'maps']:
    with open(os.path.join(samples_dir, 'mpl5_main_sample_{}.txt'.format(dltype)), 'w') as fout:
        fout.write('# MPL-5 Main Sample (Primary, Secondary, and Color Enhanced galaxies)\n')
        fout.write('# source paths    destination paths\n')
        for plateifu in plateifus_uniques:
            plate = plateifu.split('-')[0]
            filepath = make_filepath(plateifu, dltype)
            fout.write('{0} {0}\n'.format(filepath))

for dltype in ['LOGCUBE', 'LOGRSS', 'images', 'maps']:
    with open(os.path.join(samples_dir, 'mpl5_main_sample_{}_test.txt'.format(dltype)), 'w') as fout:
        fout.write('# MPL-5 Main Sample (Primary, Secondary, and Color Enhanced galaxies)\n')
        fout.write('# source paths    destination paths\n')
        plateifu = plateifus_uniques[783]
        plate = plateifu.split('-')[0]
        filepath = make_filepath(plateifu, dltype)
        fout.write('{0} {0}\n'.format(filepath))


drpall.close()



