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

from visigoth.svg import image
from visigoth.map_layers import MapLayer
from visigoth.utils.js import Js
from visigoth.utils.image.png_canvas import PngCanvas
from visigoth.utils.colour import ContinuousPalette, Colour
from visigoth.utils.mapping import Projections

class ColourGrid(MapLayer):
    """
    Create a Colour grid plot

    Arguments:
        data (list): list of rows, where each row is an equal size list of column values values
        boundaries(tuple): a tuple containing (min-lon,min-lat) and (max-lon,max-lat) pairs

    Keyword Arguments:
        palette(object): a ContinuousPalette or DiscretePalette
    """

    def __init__(self, data, boundaries, palette=None):
        super().__init__()
        self.data = data
        self.region_boundaries = boundaries
        self.boundaries = boundaries
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
            self.max_val = max([v for rowdata in self.data for v in rowdata if v is not None])
            self.min_val = min([v for rowdata in self.data for v in rowdata if v is not None])

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
        x_frac = (lon - min_lon)/(max_lon-min_lon)
        x_index = min(round(self.columns * x_frac),self.columns-1)
        y_frac = (lat - min_lat)/(max_lat - min_lat)
        y_index = min(round(self.rows * y_frac),self.rows-1)
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

        ((min_e, min_n), (max_e, max_n)) = Projections.getENBoundaries(self.projection, self.boundaries)

        height_px = self.rows
        width_px = self.columns
        x_step = (max_e - min_e)/width_px
        y_step = (max_n - min_n)/height_px
        c = PngCanvas(height_px, width_px, colours)
        for x in range(width_px):
            e = min_e + (x_step/2) + x*x_step
            for y in range(height_px):
                n = max_n - (y_step / 2) - y*y_step
                (lon,lat) = self.projection.toLonLat((e,n))
                v = self.getValueAt(lon,lat)
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
