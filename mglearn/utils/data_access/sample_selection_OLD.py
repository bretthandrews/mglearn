"""Select MaNGA MPL-5 Main Sample galaxies."""


import os

import numpy as np
from astropy.io import fits

from marvin import config


__all__ = ('get_drpver')
    

def open_drpall(drpver=None, release=None, path=None):
    """Open DRPall file.
    
    Parameters:
        drpver (str):
            DRP version. Default is None.
        release (str):
            The DRP version Default is None.
        path (str):
            Path to the DRPall file. Default is None.

    Returns:
        FITS file
    
    TODO close FITS file?
  
    """
    drpver = get_drpver(drpver, release)
    path = get_drpall_path(drpver, path)
    return fits.open(os.path.join(path, 'drpall-{}.fits'.format(drpver)))




def get_drpall_path(drpver, path):
    """Get path to DRPall file.
        
    Parameters:
        drpver (str):
            DRP version.
        path (str):
            Path to the DRPall file.
    
    Returns:
        path (str)
    """
    if path is None:
        try:
            redux = os.environ['MANGA_SPECTRO_REDUX']
        except KeyError as ee:
            raise ValueError('Specify path to drpall file.')
        
        path = os.path.join(redux, drpver)

    return path


def get_drpver(drpver, release):
    """Get DRP version
        
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

# Write MPL-5 Main Sample plateifus to file
with open('mpl5_main_sample.txt', 'w') as fout:
    fout.write('# MPL-5 Main Sample (Primary, Secondary, and Color Enhanced galaxies)')
    for plateifu in plateifus:
        fout.write(plateifu + '\n')