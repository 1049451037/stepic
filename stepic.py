# stepic - Python image steganography
# Copyright (C) 2007 Lenny Domnitser
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

'''Python image steganography

Stepic hides arbitrary data inside PIL images.

Stepic uses the Python Image Library
(apt: python-imaging, web: <http://www.pythonware.com/products/pil/>).
'''

__author__ = 'Lenny Domnitser <http://domnit.org/>, modified by Qingsong Lv.'
__version__ = '1.0'


import warnings

__all__ = ('encode_imdata','encode_inplace', 'encode',
           'decode_imdata', 'decode')


def encode_imdata(imdata, data):
    '''given a sequence of pixels, returns an iterator of pixels with
    encoded data'''

    datalen = len(data)
    if datalen == 0:
        raise ValueError('data is empty')
    if datalen * 3 > len(imdata):
        raise ValueError('data is too large for image')

    imdata = iter(imdata)

    for i in range(datalen):
        pixels = [value & ~1 for value in
                  imdata.__next__()[:3] + imdata.__next__()[:3] + imdata.__next__()[:3]]
        byte = data[i]
        for j in range(7, -1, -1):
            pixels[j] |= byte & 1
            byte >>= 1
        if i == datalen - 1:
            pixels[-1] |= 1
        pixels = tuple(pixels)
        yield pixels[0:3]
        yield pixels[3:6]
        yield pixels[6:9]


def encode_inplace(image, data):
    '''hides data in an image'''

    w = image.size[0]
    (x, y) = (0, 0)
    for pixel in encode_imdata(image.getdata(), data):
        image.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1


def encode(image, data):
    '''generates an image with hidden data, starting with an existing
    image and arbitrary data'''

    image = image.copy()
    encode_inplace(image, data)
    return image


def decode_imdata(imdata):
    '''Given a sequence of pixels, returns an iterator of characters
    encoded in the image'''

    imdata = iter(imdata)
    while True:
        pixels = list(imdata.__next__()[:3] + imdata.__next__()[:3] + imdata.__next__()[:3])
        byte = 0
        for c in range(7):
            byte |= pixels[c] & 1
            byte <<= 1
        byte |= pixels[7] & 1
        yield chr(byte)
        if pixels[-1] & 1:
            break


def decode(image):
    '''extracts data from an image'''

    return ''.join(decode_imdata(image.getdata()))
