# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import base64
import os
import os.path
import io

from visigoth.svg import image
from visigoth.map_layers import MapLayer
from visigoth.utils.js import Js
from visigoth.utils.image.png_canvas import PngCanvas
from visigoth.utils.colour import ContinuousPalette
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
        self.boundaries = None
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

    def configureLayer(self, ownermap, width, height, boundaries, projection, zoom_to):
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
        colours = [(255, 255, 255, 0)]
        intervals = self.getPalette().getIntervals()
        for (val, _, col) in intervals:
            if col != c:
                r = int(col[1:3], 16)
                g = int(col[3:5], 16)
                b = int(col[5:7], 16)
                o = 255
                thresholds.append((val, len(thresholds)))
                colours.append((r, g, b, o))
            c = col

        def getColourIndex(val):
            if val is None:
                return 0
            for (threshold, index) in thresholds:
                if val < threshold:
                    return index
            return len(colours) - 1


        ((min_e, min_n), (max_e, max_n)) = Projections.getENBoundaries(self.projection, self.boundaries)

        height_px = int(self.height)
        width_px = int(self.width)
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
        doc.add(i)

        with open(os.path.join(os.path.split(__file__)[0], "colourgrid.js"), "r") as jsfile:
            jscode = jsfile.read()
        config = {}
        Js.registerJs(doc, self, jscode, "colourgrid", cx, cy, config)
