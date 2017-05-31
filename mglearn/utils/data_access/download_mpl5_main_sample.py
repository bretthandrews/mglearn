"""
Download MaNGA MPL-5 Main Sample galaxy cubes.
"""

from marvin import config
from marvin.utils.general import downloadList

# See Marvin docs for details on how to download MaNGA galaxies
# http://sdss-marvin.readthedocs.io/en/latest/core/downloads.html
config.setRelease('MPL-5')

# Read MPL-5 Main Sample plateifus from file
with open('mpl5_main_sample.txt', 'r') as fin:
    plateifus = []
    for line in fin:
        if line[0] != "#":
            plateifus.append(line.strip())

for dltype in ['cube', 'map', 'image', 'rss']:
    downloadList(plateifus, dltype=dltype)