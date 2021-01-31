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

import math

from visigoth.map_layers import MapLayer

from visigoth.utils.colour import ContinuousColourManager

class ColourGrid(MapLayer):
    """
    Create a Colour grid plot.

    Arguments:
        data (list): data values, organised as a list of rows, where each row is an equal size list of column values
        lats (list): a list of the lat values providing the center of each row
        lons (list): a list of the lon values providing the center of each column

    Keyword Arguments:
        colour_manager(object): a ContinuousColourManager or DiscreteColourManager
        sharpen(bool): produce a sharper (double resolution) image at 2x resolution, slower to run

    """

    def __init__(self, data, lats, lons, colour_manager=None, sharpen=False):
        super().__init__()
        self.data = data

        rows = len(self.data)
        columns = len(self.data[0])

        for row in self.data:
            if len(row) != columns:
                raise Exception(ColourGrid.INPUT_DATA_FORMAT_ERROR)

        self.max_val = None
        self.min_val = None
        if self.data:
            valid_values = [v for rowdata in self.data for v in rowdata if v is not None and math.isfinite(v)]
            if valid_values:
                self.max_val = max(valid_values)
                self.min_val = min(valid_values)
            else:
                self.min_val = 0
                self.max_val = 0

        if colour_manager is None:
            colour_manager = ContinuousColourManager(withIntervals=True)
        self.setPalette(colour_manager)
        if not self.getPalette().isDiscrete():
            self.getPalette().allocateColour(self.min_val)
            self.getPalette().allocateColour(self.max_val)
        # set up an ImageGrid to handle the real work, with empty data (we'll bind it to the real data at drawing time)
        from visigoth.map_layers import ImageGrid
        self.imagegrid = ImageGrid(r=[],g=[],b=[],a=[],lats=lats,lons=lons,sharpen=sharpen)

    INPUT_DATA_FORMAT_ERROR = "data parameter must be a non-empty list of equally sized non-empty lists containing data values"

    def getBoundaries(self):
        return self.imagegrid.getBoundaries()

    def configureLayer(self, ownermap, width, height, boundaries, projection, zoom_to, fmt):
        self.imagegrid.configureLayer(ownermap, width, height, boundaries, projection, zoom_to, fmt)

    def getHeight(self):
        return self.imagegrid.getHeight()

    def getWidth(self):
        return self.imagegrid.getWidth()

    def draw(self, doc, cx, cy):
        r_data = []
        g_data = []
        b_data = []
        a_data = []
        for row_idx in range(len(self.data)):
            row = self.data[row_idx]
            r_row = []
            g_row = []
            b_row = []
            a_row = []
            for col_idx in range(len(row)):
                value = row[col_idx]
                col = self.colour_manager.getColour(value)
                if col == "red":
                    print("red?")
                # col should be a hex encoded string, either #RRGGBBAA or #RRGGBB
                r = int(col[1:3], 16)
                g = int(col[3:5], 16)
                b = int(col[5:7], 16)
                a = 255 if len(col) == 7 else int(col[7:9], 16)
                r_row.append(r)
                g_row.append(g)
                b_row.append(b)
                a_row.append(a)
            r_data.append(r_row)
            g_data.append(g_row)
            b_data.append(b_row)
            a_data.append(a_row)
        self.imagegrid.update_data(r=r_data,g=g_data,b=b_data,a=a_data)
        return self.imagegrid.draw(doc,cx,cy)



