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

import json
import os

from visigoth.common.diagram_element import DiagramElement
from visigoth.svg import polygon, line, circle, rectangle
from visigoth.utils.mapping import Mapping
from visigoth.utils.mapping import Projections
from visigoth.common.text import Text
from visigoth.common.panzoom import PanZoom
from visigoth.utils.js import Js


class Map(DiagramElement):

    """
    Overlay multiple layers to create a map

    Arguments:
        width(int) : width of the map in pixels

    Keyword Arguments:
        boundaries(tuple): tuple containing (min-lon,min-lat) and (max-lon,max-lat) pairs
        projection(object): the projection system to use
        font_height(int) : font size in pixels
        text_attributes(dict): a dict containing SVG name/value attributes
        width_to_height(float): if specified, sets the width to height ratio of the map
        zoom_to(int): specify how much magnification can be selected - must be a power of 2
        panzoom_radius(int) : specify redius in pixels for the pan/zoom control
        fill(str): specify a background colour
    """
    def __init__(self,width,boundaries=None,projection=Projections.EPSG_3857,font_height=10,text_attributes={},width_to_height=None,zoom_to=1,panzoom_radius=40,fill="white"):
        DiagramElement.__init__(self)
        self.layers = []
        self.elements = []
        self.attributions = []
        self.width = width
        self.boundaries = boundaries
        self.projection = projection
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.width_to_height = width_to_height
        self.zoom_to = zoom_to
        self.panzoom_radius = panzoom_radius
        self.fill = fill
        self.built = False

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getProjection(self):
        return self.projection

    def mergeBoundaries(self,boundaries):
        if boundaries == None:
            return
        if self.boundaries == None:
            self.boundaries = boundaries
        else:
            ((min_lon1,min_lat1),(max_lon1,max_lat1)) = self.boundaries
            ((min_lon2,min_lat2),(max_lon2,max_lat2)) = boundaries
            self.boundaries = ((min(min_lon1,min_lon2),min(min_lat1,min_lat2)),(max(max_lon1,max_lon2),max(max_lat1,max_lat2)))

    def expandBoundaries(self,frac):
        if self.boundaries:
            ((min_lon,min_lat),(max_lon,max_lat)) = self.boundaries
            lat_range = max_lat - min_lat
            lon_range = max_lon - min_lon
            lat_delta = lat_range * frac * 0.5
            lon_delta = lon_range * frac * 0.5
            self.boundaries = ((min_lon-lon_delta,min_lat-lat_delta),(max_lon+lon_delta,max_lat+lat_delta))

    def build(self,fmt):
        if self.built:
            return
        self.built = True

        if not self.boundaries:
            # if no boundaries have been set, try and compute the boundaries
            # from the union of any boundaries obtained from individual layers
            for layer_element in self.layers:
                boundaries = layer_element.getBoundaries()
                if boundaries:
                    self.mergeBoundaries(boundaries)
            # also increase the visible area by 10% along each axis
            # this means any features in the layers are not left on the edge of the map
            self.expandBoundaries(0.1)

        if not self.boundaries:
            # default to world display if unable to determine boundaries otherwise
            self.boundaries = ((-180,-75),(180,75))
                        
        (lonmin,latmin) = self.boundaries[0]
        (lonmax,latmax) = self.boundaries[1]
        ((xmin,ymin),(xmax,ymax)) = Projections.getENBoundaries(self.projection,self.boundaries)

        if self.width_to_height:
            width = xmax-xmin
            height = ymax-ymin
            if width/height > self.width_to_height:
                # alter the height to make the map square, keep the content centered
                delta = width/self.width_to_height - height
                ymin -= delta*0.5
                ymax += delta*0.5
                latmin= self.projection.toLonLat((0,ymin))[1]
                latmax= self.projection.toLonLat((0,ymax))[1]
                self.boundaries = ((lonmin,latmin),(lonmax,latmax))
            else:
                # alter the longitude boundaries to make the map square, keep the content centered
                delta = height*self.width_to_height - width
                xmin -= delta*0.5
                xmax += delta*0.5
                lonmin= self.projection.toLonLat((xmin,0))[0]
                lonmax= self.projection.toLonLat((xmax,0))[0]
                self.boundaries = ((lonmin,latmin),(lonmax,latmax))
    
        scale = self.width/(xmax-xmin)
        self.height = scale * (ymax-ymin)
        
        self.content_width = self.width
        self.content_height = self.height

        self.elements = []
        for layer_element in self.layers:
            self.elements.append((layer_element,layer_element.getId()))

        for idx in range(len(self.elements)):
            self.elements[idx][0].configureLayer(self,self.content_width,self.content_height,self.boundaries,self.projection,self.zoom_to,fmt)
            self.elements[idx][0].build(fmt)

        self.attributions = []
        self.displayed = set()
        for layer_element in self.layers:
            md = layer_element.getMetadata()
            name =  md.getName()
            if name:
                displaytext = name
                if md.getAttribution():
                    displaytext += " - " + md.getAttribution()
                    if displaytext not in self.displayed:
                        self.displayed.add(displaytext)
                        t = Text(displaytext,max_width=self.content_width,font_height=self.font_height,text_attributes=self.text_attributes)
                        t.build(fmt)
                        self.attributions.append(t)
                        self.height += t.getHeight()
                        url = md.getUrl()
                        if url:
                            t = Text(url,max_width=self.content_width,font_height=self.font_height,url=url,text_attributes=self.text_attributes)
                            t.build(fmt)
                            self.attributions.append(t)
                            self.height += t.getHeight()

    def add(self,layer_element):
        """
        Add a layer to the map

        Arguments:
            element(DiagramElement): the element to place into the overlay
        """
        self.layers.append(layer_element)

    def drawLayer(self,doc,element,identifier,ox,oy,metadata):
        g = doc.openGroup(identifier)
        element.drawTo(ox+self.content_width/2,oy+self.content_height/2)
        element.draw(doc,ox+self.content_width/2,oy+self.content_height/2)
        g.addAttr("opacity",element.getOpacity())
        if not element.getVisible():
            g.addAttr("opacity",0.0)
        doc.closeGroup()
        metadata.append(element.getMetadata())

    def draw(self,doc,cx,cy):
        doc.openGroup(self.getId())
        oy = cy - self.height/2
        ox = cx - self.width/2



        with open(os.path.join(os.path.split(__file__)[0],"map.js"),"r") as jsfile:
            jscode = jsfile.read()
        opacities = {}
        for (element,identifier) in self.elements:
            opacities[identifier] = element.getOpacity()

        # cache any popup groups in the doc, these will be restored later
        cached_pop_groups = doc.getPopGroups()
        # start a new list in which to collect popups created in this map's layers
        doc.setPopGroups([])

        # open a cliping area for the map layers
        self.openClip(doc,ox+self.content_width/2,oy+self.content_height/2,self.content_width,self.content_height)
    
        metadata = []
        layerGroup = doc.openGroup()
        if self.fill:
            r = rectangle(ox,oy,self.width,self.height,self.fill)
            r.addAttr("pointer-events","none") # don't block events so they reach the overlay layer (if present)
            doc.add(r)

        overlayId = ""
        if self.zoom_to > 1:
            # add a transparent rectangle to receive touch events, underneath the other layers
            overlay = rectangle(ox, cy - self.height / 2, self.width, self.height, fill="#FFFFFF01")
            # overlay.addAttr("pointer-events","visible")
            overlayId = overlay.getId()
            doc.add(overlay)

        # add non-foreground layers
        for (element,identifier) in self.elements:
            if not element.isForegroundLayer():
                self.drawLayer(doc,element,identifier,ox,oy,metadata)
                
        doc.closeGroup()
        
        self.closeClip(doc)

        # add any foreground layers
        for (element,identifier) in self.elements:
            if element.isForegroundLayer():
                self.drawLayer(doc,element,identifier,ox,oy,metadata)
        
        oy += self.content_height

        # create a group "layer" in which to put any popups created from the map layers
        pop_groups = doc.getPopGroups()
        doc.setPopGroups([])
        popGroupLayer = doc.openGroup(popup=True)
        for group in pop_groups:
            popGroupLayer.add(group)
        doc.closeGroup()

        # restore any cached popup groups back to the document
        doc.setPopGroups(doc.getPopGroups()+cached_pop_groups)
        
        for attribution_text in self.attributions:
            attribution_text.build(doc.getFormat())
            ah = attribution_text.getHeight()
            attribution_text.draw(doc,cx,oy+ah/2)
            oy += ah



        if self.zoom_to > 1:
            px = cx - self.width/2 + self.panzoom_radius + 10
            py = cy - self.height/2 + self.panzoom_radius + 10
            pz = PanZoom(self.zoom_to,initial_zoom=0,radius=self.panzoom_radius)
            pz.build(doc.getFormat())
            pz.draw(doc,px,py)
            doc.getDiagram().connect(pz,"pan",self,"pan")
            doc.getDiagram().connect(pz,"zoom",self,"zoom")
            for (element,_) in self.elements:
                if Js.isRegistered(element):
                    doc.getDiagram().connect(self,"zoom",element,"zoom")
                    doc.getDiagram().connect(self,"visible_window",element,"visible_window")

        for (element,_) in self.elements:
            if Js.isRegistered(element):
                doc.getDiagram().connect(self,"search",element,"search")

        Js.registerJs(doc,self,jscode,"map",cx,cy,
            {"opacities":opacities,
            "max_zoom":self.zoom_to,
            "layerGroupId":layerGroup.getId(),
            "popGroupId":popGroupLayer.getId(),
             "overlayId":overlayId})

        doc.closeGroup()



