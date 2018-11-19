import csv
import argparse

from PIL import Image
from urllib import request
from decimal import Decimal
from full import  get_full

import tile_system

import os
if not os.path.exists('output'):
    os.makedirs('output')

parser = argparse.ArgumentParser()

parser.add_argument('--csv', default=None, type=str)
parser.add_argument('--number', default=1, type=int)
parser.add_argument('--zoom', default=0.001, type=float)
parser.add_argument('--tile_size', default=256, type=int)
parser.add_argument('--image_size', default=1280 * 1024, type=int)
parser.add_argument('--url', default='http://h0.ortho.tiles.virtualearth.net/tiles/h{0}.jpeg?g=131', type=str)

arguments = parser.parse_args()

url = arguments.url

tile_size = arguments.tile_size
image_size = arguments.image_size
n = arguments.number
zoom = arguments.zoom
images_all = []
output_coordinates = []

def draw_coordinates(coordinate, n, b):
    c = b
    d = (2*n - 1)*c
    max_piont = [float(round(Decimal(float(coordinate[0]) + d), 6)),
                 float(round(Decimal(float(coordinate[1]) + d), 6))]
    min_point = [float(round(Decimal(float(coordinate[0]) - d), 6)),
                 float(round(Decimal(float(coordinate[1]) - d), 6))]
    print(min_point)
    print(max_piont)
    get_image = aerial_image(min_point[0], min_point[1], max_piont[0], max_piont[1])
    get_image.max_resolution_image(['full', 'image'], [max_piont[0], min_point[1],min_point[0], min_point[1]], d)
    X = []
    Y = []
    x = max_piont[0]
    X.append(x)
    y = max_piont[1]
    Y.append(y)
    while  x > min_point[0]:
        x = round(x - 2*b, 6)
        X.append(x)

    while  y > min_point[1]:
        y = round(y - 2*b, 6)
        Y.append(y)
    X = sorted(X)
    Y = sorted(Y)
    coordinates_all = []
    for i in range(0, len(Y)-1):
        for j in range(0, len(X) - 1):
            xlat, xlon, ylat, ylon = X[j], X[j+1], Y[i], Y[i+1]
            if j == n - 1  and i == n - 1 :
                get_image = aerial_image(xlat, ylat, xlon, ylon)
                get_image.max_resolution_image([j, i], [min_point[0], min_point[1], max_piont[0], max_piont[1]], d = len(X) - 1)
            else:
                get_image = aerial_image(xlat, ylat, xlon, ylon)
                get_image.max_resolution_image([j, i],[min_point[0], min_point[1], max_piont[0], max_piont[1]], d = len(X) - 1)
    return coordinates_all

class aerial_image(object):
    def __init__(self, xlat, xlon, ylat, ylon):
        self.xlat = xlat
        self.xlon = xlon
        self.ylat = ylat
        self.ylon = ylon
        self.folder = 'output/'

    def download_image(self, quadkey):
        with request.urlopen(url.format(quadkey)) as file:
            return Image.open(file)

#----------------------------------------------------------------------------------------------------------------------#

    def max_resolution_image(self, coordinate, jpg_c, d):
        for level in range(tile_system.max_level, 0, -1):
            pixelX1, pixelY1 = tile_system.lat_long_to_pixel(self.xlat, self.xlon, level)
            pixelX2, pixelY2 = tile_system.lat_long_to_pixel(self.ylat, self.ylon, level)

            pixelX1, pixelX2 = min(pixelX1, pixelX2), max(pixelX1, pixelX2)
            pixelY1, pixelY2 = min(pixelY1, pixelY2), max(pixelY1, pixelY2)
            # Bounding box's two coordinates coincide at the same pixel, which is invalid for an aerial image.
            # Raise error and directly return without retriving any valid image.
            if abs(pixelX1 - pixelX2) <= 1 or abs(pixelY1 - pixelY2) <= 1:
                #print('Cannot find a valid aerial imagery for the given bounding box!')
                return

            if abs(pixelX1 - pixelX2) * abs(pixelY1 - pixelY2) > image_size:
                #print('Current level {}'.format(level))
                continue

            tileX1, tileY1 = tile_system.pixel_to_tile(pixelX1, pixelY1)
            tileX2, tileY2 = tile_system.pixel_to_tile(pixelX2, pixelY2)

            # Stitch the tile images together
            result = Image.new('RGB', ((tileX2 - tileX1 + 1) * tile_size, (tileY2 - tileY1 + 1) * tile_size))
            retrieve_sucess = False
            for tileY in range(tileY1, tileY2 + 1):
                retrieve_sucess, horizontal_image = self.horizontal_retrieval_and_stitch_image(tileX1, tileX2, tileY,
                                                                                               level)
                if not retrieve_sucess:
                    break
                result.paste(horizontal_image, (0, (tileY - tileY1) * tile_size))

            if not retrieve_sucess:
                continue

            # Crop the image based on the given bounding box
            leftup_cornerX, leftup_cornerY = tile_system.tile_to_pixel(tileX1, tileY1)
            retrieve_image = result.crop((pixelX1 - leftup_cornerX, pixelY1 - leftup_cornerY, \
                                          pixelX2 - leftup_cornerX, pixelY2 - leftup_cornerY))
            # print("Finish the aerial image retrieval, store the image aerialImage_{0}.jpeg in folder {1}".format(level,
            #                                                                                                      self.folder))
            filename = os.path.join(self.folder, '{0}_{1}.jpeg'.format(coordinate[0], coordinate[1]))
            images_all.append(filename)
            retrieve_image.save(filename)
            #print(filename)
            get_full('output', arguments.zoom, jpg_c, filename, d)
            return True
        return False

# ----------------------------------------------------------------------------------------------------------------------#


    def horizontal_retrieval_and_stitch_image(self, xtile_start, xtile_end, ytile, level):
        images = []

        for xtile in range(xtile_start, xtile_end + 1):
            quadkey = tile_system.tile_to_quadkey(xtile, ytile, level)
            image = self.download_image(quadkey)
            images.append(image)
        result = Image.new('RGB', (len(images) * tile_size, tile_size))

        for counter, image in enumerate(images):
            result.paste(image, (counter * tile_size, 0))

        return True, result

if not os.path.exists('output'):
    os.makedirs('output')

with open(arguments.csv, 'r', newline='') as file:
    coordinates = csv.reader(file, delimiter=' ', quotechar='|')

    for coordinate in coordinates:
        draw_coordinates(coordinate, n, zoom)

# with open('output/output.csv', 'w') as file:
#     wr = csv.writer(file)
#     wr.writerow(("coordinates", "probability"))


