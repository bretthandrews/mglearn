from __future__ import division, print_function, absolute_import
import os

import pytest
import astropy
from marvin import config

from mglearn import selection


drpver_cfg, __ = config.lookUpVersions()


@pytest.mark.parametrize('drpver, release, expected',
                         [('v2_0_1', None, 'v2_0_1'),
                          (None, 'MPL-5', 'v2_0_1'),
                          (None, None, drpver_cfg)])
def test_set_drpver(drpver, release, expected):
    assert sample_select.set_drpver(drpver, release) == expected


@pytest.mark.parametrize('drpver, release',
                         [('v2_0_1', 'MPL-5')])
def test_set_drpver_conflict(drpver, release):
    with pytest.raises(AssertionError) as excinfo:
        sample_select.set_drpver(drpver, release)
    assert 'Both ``drpver`` and ``release`` are set' in str(excinfo.value)

@pytest.mark.parametrize('drpver, release, path_drpall, rows, cols',
    [('v2_0_1', None, None, 9707, 89),
     (None, 'MPL-5', None, 9707, 89),
     (None, None, os.path.join(os.environ['MANGA_SPECTRO_REDUX'], drpver_cfg), 9707, 89)
     ])
def test_read_drpall(drpver, release, path_drpall, rows, cols):
    data = sample_select.read_drpall(drpver, release, path_drpall)
    assert isinstance(data, astropy.io.fits.fitsrec.FITS_rec)
    assert len(data) == rows
    assert len(data.columns) == cols


@pytest.mark.parametrize('drpver, bits, expected',
                         [('v2_0_1', (10, 11, 12), 2672)])
def test_apply_bitmasks(drpver, bits, expected):
    data = sample_select.read_drpall(drpver=drpver)
    assert sum(sample_select.apply_bitmasks(data['mngtarg1'], bits)) == expected


@pytest.mark.parametrize('drpver, bits, expected',
                         [('v2_0_1', (10, 11, 12), 2622)])
def test_remove_duplicates(drpver, bits, expected):
    data = sample_select.read_drpall(drpver=drpver)
    sample = sample_select.apply_bitmasks(data['mngtarg1'], bits)
    plateifus = data['plateifu'][sample]
    mangaids = data['mangaid'][sample]
    sn2 = data['bluesn2'] + data['redsn2']
    uniques = sample_select.remove_duplicates(plateifus, mangaids, sn2)
    assert len(uniques) == expected


@pytest.mark.parametrize('plateifus, header',
                         [(['7443-1901'], '# Sample\n'),
                          (['7443-1901', '8485-1901'], '# Sample\n# MPL-5\n')])
def test_write(tmpdir, plateifus, header):
    tmp_file = tmpdir.join('tmp_sample.txt')
    sample_select.write(plateifus, tmp_file, header)
    assert tmp_file.read() == '{}'.format(header) + '\n'.join(plateifus + [''])
