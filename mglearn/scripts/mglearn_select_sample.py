# mglearn_select_sample.py
#
# Created by Brett H. Andrews on 31 Mar 2017.

from __future__ import division, print_function, absolute_import, unicode_literals
import os

import click
from marvin import config

from mglearn import selection


@click.command()
@click.option('--release', default=None)
@click.option('--drpver', default=None)
@click.option('--path-drpall', default=None)
@click.option('--bits', '-b', type=click.INT, multiple=True, help='DAP pixel bitmasks.')
@click.option('--targeting_bit', default='mngtarg1')
@click.option('--main_sample', default=False, is_flag=True)
@click.option('--path_out', default=None)
@click.option('--overwrite', '-o', default=False, is_flag=True)
@click.argument('filename', click.File('w'))
def select_sample(filename, release, drpver, path_drpall, bits, targeting_bit, main_sample,
                  path_out, overwrite):
    """Select MaNGA sample.

    Parameters:
        filename (str):
            Output file of plate-ifu identifiers.
        release (str):
            MaNGA MPL release.  Default is None.
        drpver (str):
            MaNGA data reduction pipeline (DRP) version.  Default is None.
        path_drpall (str):
            Path to local drpall file.  Default is None.
        bits (int):
            Bits of ``targeting_bit`` to use for sample selection.
        targeting_bit (str):
            Targeting bit to use.  Default is ``mngtarg1``.
    """

    drpver_ = selection.set_drpver(drpver=drpver, release=release)
    release_ = config.lookUpRelease(drpver_)

    if main_sample:
        bits = (10, 11, 12)
        desc = 'Main Sample (Primary, Secondary, and Color Enhanced galaxies)'
    else:
        if not isinstance(bits, tuple):
            bits = (bits,) if isinstance(bits, int) else tuple(bits)

        desc = '{0} bits {1}'.format(targeting_bit, *bits) if len(bits) > 0 else 'No bits set.'

    header = '# {0} {1}\n'.format(release_, desc)

    drpall = selection.read_drpall(drpver=drpver_, path_drpall=path_drpall)
    sample_obs = selection.apply_bitmasks(drpall[targeting_bit], bits)
    plateifus = drpall['plateifu'][sample_obs]
    mangaids = drpall['mangaid'][sample_obs]

    sn2 = drpall['bluesn2'] + drpall['redsn2']
    sample_unique = selection.remove_duplicates(plateifus, mangaids, sn2)

    if path_out is None:
        path_out = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')),
                                'data', 'samples', filename.split('.')[0])

    if not os.path.isdir(path_out):
        os.mkdir(path_out)

    path_full = os.path.join(path_out, filename)

    if overwrite or (not os.path.isfile(path_full)):
        selection.write(sample_unique, path_full, header)
        click.echo('\nWrote plate-ifu list to:\n{}\n'.format(path_full))
    else:
        click.echo('\nFile already exists:\n{}\n\nUse "-o" to overwrite.\n'.format(path_full))
