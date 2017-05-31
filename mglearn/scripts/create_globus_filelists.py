#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals

from mglearn import select

__all__ = ['make_filepath', 'write_globus_files']


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


def write_globus_files(filetypes, name_stem):

    for filetype in filetypes:
        with open(os.path.join(samples_dir, '{}_{}.txt'.format(name_stem, filetype)), 'w') as fout:
            
            # TODO replace with header from Sample file (i.e., text file with list of plateifus)
            # fout.write('# MPL-5 Main Sample (Primary, Secondary, and Color Enhanced galaxies)\n')

            fout.write('# source paths    destination paths\n')
            for plateifu in plateifus:
                plate = plateifu.split('-')[0]
                filepath = make_filepath(plateifu, dltype)
                fout.write('{0} {0}\n'.format(filepath))

    


if __name__ == '__main__':
    # argparse or click
    # filetypes ['LOGCUBE', 'LOGRSS', 'images', 'maps']
    # name stem "mpl5_main_sample"
    # data dir

    write_globus_files()