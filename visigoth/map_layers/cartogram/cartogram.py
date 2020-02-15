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


from math import sqrt
import copy
import os.path
import random

from visigoth.svg import circle, line
from visigoth.map_layers import MapLayer
from visigoth.utils.term.progress import Progress
from visigoth.utils.js import Js

class Cartogram(MapLayer):

    """
    Create a Cartogram plot layer in which a list of points with assigned radii are peturbed
    from their original positions to avoid overlap.

    Hover over a point to see a link to the original position

    Arguments:
        data(tuple) : data in the form (lon,lat,category,label,radius)
        palette(list) : a DiscretePalette assigning categories to colours

    Keyword Arguments:
        iterations(int): number of iterations to run
        stroke (str): stroke color for circumference of circles
        stroke_width (int): stroke width for circumference of circles
        font_height (int): the height of the font for text labels
        text_attributes (dict): SVG attribute name value pairs to apply to labels
        link_stroke (str): colour to draw links to original position
        link_stroke_width (int): the width of links
        f1 (float): relative force attracting each point to its original location
        f2 (float): relative force repelling overlapping points

    Notes:

    """

    def __init__(self, data, palette, iterations=30, stroke="black",stroke_width=1,font_height=24, text_attributes={},link_stroke="grey",link_stroke_width=2,f1=0.01,f2=0.5):
        super(Cartogram, self).__init__()
        self.data = data
        self.width = None
        self.height = None
        self.palette = palette
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.iterations = iterations
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.link_stroke = link_stroke
        self.link_stroke_width = link_stroke_width
        self.built = False
        self.plots = []
        self.f1 = f1
        self.f2 = f2
        self.categories = {}
        self.links = {}

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
        self.width = width
        self.boundaries = boundaries
        self.projection = projection
        (self.x0,self.y0) = projection.fromLonLat(boundaries[0])
        (self.x1,self.y1) = projection.fromLonLat(boundaries[1])
        self.height = height
        self.scale_x = self.width/(self.x1-self.x0)
        self.scale_y = self.height/(self.y1-self.y0)

    def getBoundaries(self):
        return self.boundaries

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

    def build(self):
        if self.built:
            return

        for d in self.data:
            p = self.projection.fromLonLat((d[0],d[1]))
            self.plots.append({"x":p[0],"y":p[1],"ox":p[0],"oy":p[1],"fx":0,"fy":0,"label":d[3],"cat":d[2],"r":d[4]})

        for i in range(0,len(self.plots)):
            self.plots[i]["id"] = i

        self.built = True
        distance = lambda x1,y1,x2,y2: sqrt((x1-x2)**2+(y1-y2)**2)

        best_plots = None
        best_error = None

        rng = random.Random(0)

        progress = Progress("cartogram")

        for iter in range(self.iterations):

            overlaps = 0
            error = 0
            for plot in self.plots:
                ox = plot["ox"]
                oy = plot["oy"]
                nx = plot["x"]
                ny = plot["y"]
                nr = plot["r"]

                d = distance(nx,ny,ox,oy)
                fx = 0
                fy = 0
                if d > 0.0:
                    fx = (ox-nx)*self.f1
                    fy = (oy-ny)*self.f1
                    error += d

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
                            fac = -1*self.f2*(d-overlap_radius)/overlap_radius
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
                # ensure the plot is completely visible
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

        ox = cx - self.getWidth()/2
        oy = cy - self.getHeight()/2

        nw = self.projection.fromLonLat(self.boundaries[0])

        for plot in self.plots:
            x = plot["x"]
            y = plot["y"]
            label = plot["label"]
            cat = plot["cat"]
            r = plot["r"]

            col = self.palette.getColour(cat)
            cx = ox+(x-nw[0])*self.scale_x
            cy = oy+(self.height - (y-nw[1])*self.scale_y)

            circ = circle(cx,cy,r,col,tooltip=label)
            cid = circ.getId()
            plot["cid"] = cid
            ids = self.categories.get(cat,[])
            ids.append(cid)
            self.categories[cat] = ids
            circ.addAttr("stroke",self.stroke)
            circ.addAttr("stroke-width",self.stroke_width)
            svgdoc.add(circ)

        if self.link_stroke and self.link_stroke_width:
            for plot in self.plots:
                x = plot["x"]
                y = plot["y"]
                orig_x = plot["ox"]
                orig_y = plot["oy"]

                x1 = ox+(x-nw[0])*self.scale_x
                y1 = oy+(self.height - (y-nw[1])*self.scale_y)

                x2 = ox + (orig_x - nw[0]) * self.scale_x
                y2 = oy + (self.height - (orig_y - nw[1]) * self.scale_y)

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
