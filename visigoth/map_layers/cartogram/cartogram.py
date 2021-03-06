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


from math import sqrt
import copy
import os.path
import random

from visigoth.svg import circle, line
from visigoth.map_layers import MapLayer
from visigoth.utils.term.progress import Progress
from visigoth.utils.js import Js
from visigoth.utils.data import Dataset
from visigoth.utils.colour import DiscreteColourManager, ContinuousColourManager
from visigoth.utils.marker import MarkerManager

class Cartogram(MapLayer):

    """
    Create a Cartogram plot layer in which a list of points with assigned radii are peturbed
    from their original positions to avoid overlap.

    Hover over a point to see a link to the original position

    Arguments:
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)


    Keyword Arguments:

        lat (str or int): Identify the column to provide the latitude value for each point
        lon (str or int): Identify the column to provide the longitude value for each point
        colour (str or int): Identify the column to define the point colour (use colour_manager default colour if not specified)
        label (str or int): Identify the column to define the label
        size (str or int): Identify the column to determine the size of each marker
        iterations(int): number of iterations to run
        font_height (int): the height of the font for text labels
        text_attributes (dict): SVG attribute name value pairs to apply to labels
        link_stroke (str): colour to draw links to original position
        link_stroke_width (int): the width of links
        f1 (float): relative force attracting each point to its original location
        f2 (float): relative force repelling overlapping points
        colour_manager(object) : a ContinuousColourManager or DiscreteColourManager instance to control chart colour
        marker_manager(object) : a MarkerManager instance to control marker appearance

    Notes:

    """

    def __init__(self, data, lon=0, lat=1, colour=None, label=None, size=None, iterations=30, font_height=24, text_attributes={},link_stroke="grey",link_stroke_width=2,f1=0.01,f2=0.5, colour_manager=None, marker_manager=None):
        super(Cartogram, self).__init__()
        self.lat = lat
        self.lon = lon
        self.colour = colour
        self.label = label
        self.size = size
        self.dataset = Dataset(data)
        self.data = self.dataset.query([self.lon,self.lat, self.colour,self.label,self.size])

        self.width = None
        self.height = None
        self.colour_manager = colour_manager
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.iterations = iterations

        if not colour_manager:
            if not self.colour or self.dataset.isDiscrete(self.colour):
                colour_manager = DiscreteColourManager()
            else:
                colour_manager = ContinuousColourManager()
        self.setPalette(colour_manager)

        if not marker_manager:
            marker_manager = MarkerManager()
            marker_manager.setDefaultRadius(15)
        self.setMarkerManager(marker_manager)

        for (lon,lat,colour,label,size) in self.data:
            self.getMarkerManager().noteSize(size)
            self.getPalette().allocateColour(colour)

        self.link_stroke = link_stroke
        self.link_stroke_width = link_stroke_width
        self.built = False
        self.plots = []
        self.f1 = f1
        self.f2 = f2
        self.categories = {}
        self.links = {}

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def distance_lteq(self,x1,y1,x2,y2,lim):
        x_diff = abs(x1-x2)
        if x_diff > lim:
            return None
        y_diff = abs(y1-y2)
        if y_diff > lim:
            return None
        d = sqrt(x_diff**2 + y_diff**2)
        if d > lim:
            return None
        return d

    def build(self,fmt):
        if self.built:
            return

        for (lon,lat,colour,label,size) in self.data:
            r = self.getMarkerManager().getRadius(size)
            (x,y) = self.projection.fromLonLat((lon,lat))
            self.plots.append({"x":x,"y":y,"ox":x,"oy":y,"fx":0,"fy":0,"label":label,"cat":colour,"r":r})

        for i in range(0,len(self.plots)):
            self.plots[i]["id"] = i

        self.built = True
        distance = lambda x1,y1,x2,y2: sqrt((x1-x2)**2+(y1-y2)**2)

        best_plots = None
        best_error = None

        rng = random.Random(0)

        progress = Progress("cartogram")
        progress.report("building", 0)

        for iter in range(self.iterations):

            # gradually increase the force attracting each point to its original position...
            # ... whilst reducing the force repelling overlapping points
            # f1 = self.f1/2 + ((self.f1/2) * ((iter+1)/self.iterations))
            # f2 = self.f2*2 - (self.f2 * ((iter+1))/self.iterations)
            f1 = self.f1
            f2 = self.f2
            # print(f1,f2)
            overlaps = 0
            error = 0
            for plot in self.plots:
                ox = plot["ox"]
                oy = plot["oy"]
                nx = plot["x"]
                ny = plot["y"]
                nr = plot["r"]

                d = distance(nx,ny,ox,oy)

                # compute the forces on this point, fx and fy
                fx = 0
                fy = 0

                # first, attract the point to its original position
                if d > 0.0:
                    fx = (ox-nx)*f1
                    fy = (oy-ny)*f1
                    error += d

                # next, repel the point from any overlapping points
                for otherplot in self.plots:
                    if plot["id"] != otherplot["id"]:
                        opx = otherplot["x"]
                        opy = otherplot["y"]
                        onr = otherplot["r"]
                        overlap_radius = (onr+nr) / self.scale_x

                        if nx == opx and ny == opy:
                            # handle special case of exactly superimposed points by nudging
                            if nx+ny:
                                nudge = (nx+ny)*0.001
                            else:
                                nudge = 0.001
                            nx += nudge*rng.random()-nudge*0.5
                            ny += nudge*rng.random()-nudge*0.5
                        d = self.distance_lteq(nx,ny,opx,opy,overlap_radius)
                        if d != None:
                            fac = -1*f2*(d-overlap_radius)/overlap_radius
                            fx += (nx-opx)*fac
                            fy += (ny-opy)*fac
                            overlaps += 1

                plot["fx"] = fx
                plot["fy"] = fy

            if overlaps < 3 and (best_error == None or error < best_error):
                best_error = error
                best_plots = copy.deepcopy(self.plots)

            for plot in self.plots:
                d = plot["r"] / self.scale_x
                x = plot["x"]
                y = plot["y"]

                x = x + plot["fx"]
                y = y + plot["fy"]
                # ensure the point is completely visible
                # ...stop the point from going out of the plot boundaries
                if x - d < self.x0:
                    x = self.x0+d
                if x + d > self.x1:
                    x = self.x1-d
                if y - d < self.y0:
                    y = self.y0 + d
                if y + d > self.y1:
                    y = self.y1 - d
                plot["x"] = x
                plot["y"] = y

            progress.report("building",(iter+1)/self.iterations)

        if best_plots:
            self.plots = best_plots

        progress.complete("complete")

    def draw(self,svgdoc,cx,cy):

        for plot in self.plots:
            x = plot["x"]
            y = plot["y"]
            label = plot["label"]
            cat = plot["cat"]
            r = plot["r"]

            col = self.getPalette().getColour(cat)
            (cx,cy) = self.getXY((x,y))

            cm = self.getMarkerManager().getCircleMarker(r)
            cid = cm.plot(svgdoc,cx,cy,label,col)
            plot["cid"] = cid
            ids = self.categories.get(cat,[])
            ids.append(cid)
            self.categories[cat] = ids

        if self.link_stroke and self.link_stroke_width:
            for plot in self.plots:
                x = plot["x"]
                y = plot["y"]
                orig_x = plot["ox"]
                orig_y = plot["oy"]

                (x1,y1) = self.getXY((x,y))
                (x2,y2) = self.getXY((orig_x,orig_y))

                l = line(x1,y1,x2,y2,stroke=self.link_stroke,stroke_width=self.link_stroke_width)
                c1 = circle(x1, y1, self.link_stroke_width*2, self.link_stroke)
                c2 = circle(x2, y2, self.link_stroke_width*2, self.link_stroke)

                svgdoc.openGroup()
                svgdoc.add(l)
                svgdoc.add(c1)
                svgdoc.add(c2)
                grp = svgdoc.closeGroup()
                grp.addAttr("visibility","hidden")
                self.links[plot["cid"]] = grp.getId()

        with open(os.path.join(os.path.split(__file__)[0], "cartogram.js"), "r") as jsfile:
            jscode = jsfile.read()
        config = {"categories":self.categories, "links":self.links}
        Js.registerJs(svgdoc, self, jscode, "cartogram", cx, cy, config)
