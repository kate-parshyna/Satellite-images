import re

from math import pi
from math import sin
from math import log
from math import floor

from itertools import chain


def clip(val, minval, maxval):
    return min(max(val, minval), maxval)


def map_size(level):
    return 256 << level


def lat_long_to_pixel(lat, long, level):
    lat = clip(lat, min_lat, max_lat)
    long = clip(long, min_lon, max_lon)

    x = (long + 180) / 360
    sinlat = sin(lat * pi / 180)
    y = 0.5 - log((1 + sinlat) / (1 - sinlat)) / (4 * pi)

    mapsize = map_size(level)

    xpixel = floor(clip(x * mapsize + 0.5, 0, mapsize - 1))
    ypixel = floor(clip(y * mapsize + 0.5, 0, mapsize - 1))

    return xpixel, ypixel


def pixel_to_tile(xpixel, ypixel):
    return floor(xpixel / 256), floor(ypixel / 256)


def tile_to_pixel(xtile, ytile):
    return xtile * 256, ytile * 256


def tile_to_quadkey(xtile, tileY, level):
    xtilebits = '{0:0{1}b}'.format(xtile, level)
    ytileybits = '{0:0{1}b}'.format(tileY, level)

    quadkey_binary = ''.join(chain(*zip(ytileybits, xtilebits)))

    return ''.join([str(int(num, 2)) for num in re.findall('..?', quadkey_binary)])


earth_radius = 6378137

min_lon, max_lon = -180., 180.
min_lat, max_lat = -85.05112878, 85.05112878

max_level = 23