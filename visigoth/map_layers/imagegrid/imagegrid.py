# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#   and associated documentation files (the "Software"), to deal in the Software without 
#   restriction, including without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all copies or 
#   substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import base64
import os
import os.path
import io
import math

from visigoth.svg import image
from visigoth.map_layers import MapLayer
from visigoth.utils.js import Js
from visigoth.utils.image.png_canvas import PngCanvas
from visigoth.utils.colour import ContinuousPalette, Colour
from visigoth.utils.mapping import Projections
from visigoth.utils.data.search import Search

class ImageGrid(MapLayer):
    """
    Create an image grid plot.

    Arguments:
        r (list): red values values, organised as a list of rows, where each row is an equal size list of column values
        g (list): blue values, organised as a list of rows, where each row is an equal size list of column values
        b (list): green values, organised as a list of rows, where each row is an equal size list of column values
        a (list): alpha values, organised as a list of rows, where each row is an equal size list of column values
        lats (list): a list of the lat values providing the center of each row
        lons (list): a list of the lon values providing the center of each column

    Keyword Arguments:
        sharpen(bool): produce a sharper (double resolution) image at 2x resolution, slower to run
        
    Notes:
        r,g,b and a values must be integers in the range 0 - 255.  None values are not allowed.

    """

    def __init__(self, r, g, b, a, lats, lons, sharpen=False):
        super().__init__()
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.lats = lats[:]
        self.lons = lons[:]
        self.sharpen = sharpen

        # check if lats and lons are sorted ascending or descending
        self.lat_reversed = lats[0] > lats[-1]
        self.lon_reversed = lons[0] > lons[-1]

        # ensure lats and lons arrays are sorted into ascending order
        if self.lat_reversed:
            self.lats.reverse()
        if self.lon_reversed:
            self.lons.reverse()

        # work out the lat/lon boundaries of the plot area
        # given that the input lats and lons provide the center of each data cell
        lat_spacing_north = self.lats[-1] - self.lats[-2]
        lat_spacing_south = self.lats[1] - self.lats[0]

        lon_spacing_east = self.lons[-1] - self.lons[-2]
        lon_spacing_west = self.lons[1] - self.lons[0]

        self.boundaries = ((self.lons[0]-lon_spacing_west/2,self.lats[0]-lat_spacing_south/2),(self.lons[-1]+lon_spacing_east/2,self.lats[-1]+lat_spacing_north/2))
        self.region_boundaries = self.boundaries
        self.width = None
        self.height = None
                
        self.projection = None
        self.update_data(r,g,b,a)
        
    def update_data(self,r,g,b,a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.rows = len(r)
        if self.rows:
            self.columns = len(r[0])
        else:
            self.columns = 0
        for data in [self.r,self.g,self.b,self.a]:
            for row in data:
                if len(row) != self.columns:
                    raise Exception(ImageGrid.INPUT_DATA_FORMAT_ERROR)
                for value in row:
                    if not isinstance(value,int) or value < 0 or value > 255:
                        raise Exception(ImageGrid.INPUT_DATA_FORMAT_ERROR)


    INPUT_DATA_FORMAT_ERROR = "r,g,b and a parameters must be a non-empty list of equally sized non-empty lists containing integer values in the range 0 to 255"

    def getBoundaries(self):
        return self.boundaries

    def configureLayer(self, ownermap, width, height, boundaries, projection, zoom_to, fmt):
        self.width = width
        self.height = height
        self.ownermap = ownermap
        self.boundaries = boundaries
        self.projection = projection

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getValueAt(self,lon,lat):
        ((min_lon, min_lat), (max_lon, max_lat)) = self.region_boundaries
        if lon < min_lon or lon > max_lon:
            return None
        if lat < min_lat or lat > max_lat:
            return None
        (y_index, _) = Search.binary_search(self.lats,lat)
        if self.lat_reversed:
            y_index = (len(self.lats)-1)-y_index

        (x_index, _) = Search.binary_search(self.lons,lon)
        if self.lon_reversed:
            x_index = (len(self.lons)-1)-x_index
        return (self.r[y_index][x_index],self.g[y_index][x_index],self.b[y_index][x_index],self.a[y_index][x_index])

    def draw(self, doc, cx, cy):
        ox = cx - self.width/2
        oy = cy - self.height/2

        # get the eastings and northings of the SW and NE corners
        ((min_e, min_n), (max_e, max_n)) = Projections.getENBoundaries(self.projection, self.boundaries)

        # get the extent of the plot area for this layer
        ((min_lon, min_lat), (max_lon, max_lat)) = self.region_boundaries

        height_px = self.rows
        width_px = self.columns
        if self.sharpen:
            height_px *= 2
            width_px *= 2
        x_step = (max_e - min_e)/width_px
        y_step = (max_n - min_n)/height_px
        # create an image canvas and fill out each point
        c = PngCanvas(height_px, width_px)
        for x in range(width_px):
            e = min_e + (x_step/2) + x*x_step
            for y in range(height_px):
                n = max_n - (y_step / 2) - y*y_step
                # (e,n) is the easting and northing of each pixel
                # now get the lon/lat according to the map CRS
                (lon,lat) = self.projection.toLonLat((e,n))
                if lon < min_lon or lon > max_lon or lat < min_lat or lat > max_lat:
                    # transparent pixel
                    c.addpixel(x,y,0,0,0,0)
                else:
                    # obtain the closest (r,g,b,a) in the input data
                    (r,g,b,a) = self.getValueAt(lon,lat)
                    c.addpixel(x,y,r,g,b,a)

        file = io.BytesIO()
        c.write(file)
        file.seek(0)

        uri = "data:image/png;charset=US-ASCII;base64," + str(base64.b64encode(file.read()), "utf-8")

        i = image(ox,oy,self.width,self.height,uri)
        i.addAttr("preserveAspectRatio","none")
        i.addAttr("image-rendering","pixelated")
        doc.add(i)

        with open(os.path.join(os.path.split(__file__)[0], "imagegrid.js"), "r") as jsfile:
            jscode = jsfile.read()
        config = {}
        Js.registerJs(doc, self, jscode, "imagegrid", cx, cy, config)
