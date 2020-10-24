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

class ColourGrid(MapLayer):
    """
    Create a Colour grid plot.

    Arguments:
        data (list): data values, organised as a list of rows, where each row is an equal size list of column values
        lats (list): a list of the lat values providing the center of each row
        lons (list): a list of the lon values providing the center of each column

    Keyword Arguments:
        palette(object): a ContinuousPalette or DiscretePalette
        sharpen(bool): produce a sharper (double resolution) image at 2x resolution, slower to run

    """

    def __init__(self, data, lats, lons, palette=None, sharpen=False):
        super().__init__()
        self.data = data
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
        self.rows = len(self.data)
        self.columns = 0
        if self.data:
            self.columns = len(self.data[0])
            if self.columns == 0:
                raise Exception(ColourGrid.INPUT_DATA_FORMAT_ERROR)
        for row in self.data:
            if len(row) != self.columns:
                raise Exception(ColourGrid.INPUT_DATA_FORMAT_ERROR)
        self.projection = None
        self.max_val = None
        self.min_val = None
        if self.data:
            self.max_val = max([v for rowdata in self.data for v in rowdata if v is not None and math.isfinite(v)])
            self.min_val = min([v for rowdata in self.data for v in rowdata if v is not None and math.isfinite(v)])

        if palette is None:
            palette = ContinuousPalette(withIntervals=True)
        self.setPalette(palette)
        self.getPalette().getColour(self.min_val)
        self.getPalette().getColour(self.max_val)

    INPUT_DATA_FORMAT_ERROR = "data parameter must be a non-empty list of equally sized non-empty lists containing data values"

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
        return self.data[y_index][x_index]

    def draw(self, doc, cx, cy):
        ox = cx - self.width/2
        oy = cy - self.height/2

        c = None
        thresholds = []
        colours = [Colour.parseColour(self.getPalette().getDefaultColour())]
        palette = self.getPalette()
        if palette.isDiscrete():
            colourlist = palette.getCategories()
        else:
            intervals = self.getPalette().getIntervals()
            if not intervals:
                low = palette.getMinValue()
                high = palette.getMaxValue()
                colourlist = []
                for idx in range(255):
                    val0 = low + (idx/255)*(high-low)
                    val1 = val0 + (1 / 255) * (high - low)
                    col = palette.getColour((val0+val1)/2)
                    colourlist.append((val0,val1,col))
            else:
                colourlist = [(val0,val1,col) for (val0, val1, col) in intervals]

        for (val0, val1, col) in colourlist:
            if col != c:
                r = int(col[1:3], 16)
                g = int(col[3:5], 16)
                b = int(col[5:7], 16)
                o = 255 if len(col) == 7 else int(col[7:9], 16)
                thresholds.append((val0, val1, len(colours)))
                colours.append((r, g, b, o))
            c = col

        if len(colours) > 256:
            raise Exception("Colour Grid cannot display more than 256 colours: %d colours requested"%(len(colours)))

        def getColourIndex(val):
            if val is None:
                return 0
            if self.getPalette().isDiscrete():
                for (value, index) in thresholds:
                    if val == value:
                        return index
                return 0
            else:
                for idx in range(len(thresholds)):
                    (threshold0, threshold1, index) = thresholds[idx]
                    if val >= threshold0 and ((val < threshold1) or ((idx == len(thresholds)-1) and (val <= threshold1))):
                        return index
                return 0

        # get the eastings and northings of the SW and NE corners
        ((min_e, min_n), (max_e, max_n)) = Projections.getENBoundaries(self.projection, self.boundaries)

        height_px = self.rows
        width_px = self.columns
        if self.sharpen:
            height_px *= 2
            width_px *= 2
        x_step = (max_e - min_e)/width_px
        y_step = (max_n - min_n)/height_px
        # create an image canvas and fill out each point
        c = PngCanvas(height_px, width_px, colours)
        for x in range(width_px):
            e = min_e + (x_step/2) + x*x_step
            for y in range(height_px):
                n = max_n - (y_step / 2) - y*y_step
                # (e,n) is the easting and northing of each pixel
                # now get the lon/lat according to the map CRS
                (lon,lat) = self.projection.toLonLat((e,n))
                # obtain the closest value in the input data
                v = self.getValueAt(lon,lat)
                # get the colour of the pixel
                ci = getColourIndex(v)
                c.addpixel(x, y, ci)

        file = io.BytesIO()
        c.write(file)
        file.seek(0)

        uri = "data:image/png;charset=US-ASCII;base64," + str(base64.b64encode(file.read()), "utf-8")

        i = image(ox,oy,self.width,self.height,uri)
        i.addAttr("preserveAspectRatio","none")
        doc.add(i)

        with open(os.path.join(os.path.split(__file__)[0], "colourgrid.js"), "r") as jsfile:
            jscode = jsfile.read()
        config = {}
        Js.registerJs(doc, self, jscode, "colourgrid", cx, cy, config)
