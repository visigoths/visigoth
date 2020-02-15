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

import os.path

from visigoth.map_layers import MapLayer
from visigoth.map_layers.geoplot import Geoplot, Multipoint
from visigoth.containers.popup import Popup
from visigoth.common import Image
from visigoth.common.embedded_html import EmbeddedHtml
from visigoth.utils.mapping import Mapping
from visigoth.map_layers.poi.twitter import encodeTweet
from visigoth.utils.js import Js

class POI(MapLayer):

    """
    Plot points of interest as media popups

    Keyword Arguments:
        fill (str): colour for each circle or marker
        stroke (str): stroke colour for circles representing points of interest
        stroke_width (int): stroke width for circles representing points of interest
        radius (int): radius of circles representing points of interest
        marker (boolean): use a marker rather than a circle
    """

    def __init__(self, fill="red",stroke="black",stroke_width=1,radius=20, marker=True):
        super(POI, self).__init__()
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.radius = radius
        self.boundaries = None
        self.scale  = None
        self.projection = None
        self.tweets = []
        self.images = []
        self.locations = []
        self.marker = marker


    def addTweet(self,status_id,lon,lat,title="",fill=None):
        """
        Add a geo-located tweet.

        Arguments:
            status_id (str): the id of the tweet
            lon (float): the tweet location, longitude
            lat (float): the tweet location, latitude

        Keyword Arguments:
            title (str): a title for the popup
            fill (str): override default colour for the marker/circle
        """
        self.locations.append((lon,lat))
        if not fill:
            fill = self.fill
        self.tweets.append((status_id,lon,lat,title,fill))

    def addImage(self,path_or_url,lon,lat,title="",scale=1.0,fill=None):
        """
        Add a geo-located image.

        Arguments:
            path_or_url (str): the path to the image or the URL of the file
            lon (float): the image location, longitude
            lat (float): the image location, latitude

        Keyword Arguments:
            title (str): a title for the popup
            scale (float): scale the image by this amount
            fill (str): override default colour for the marker/circle
        """
        self.locations.append((lon,lat))
        if not fill:
            fill = self.fill
        self.images.append((path_or_url,lon,lat,title,scale,fill))

    def getBoundaries(self):
        if not self.boundaries:
            self.boundaries = Mapping.getBoundingBox(self.locations,0.05)
        return self.boundaries

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
        self.ownermap = ownermap
        self.width = width
        self.height = height
        self.boundaries = boundaries
        self.projection = projection
        self.zoom_to = zoom_to

    def getWidth(self):
        return self.geoplot.getWidth()

    def getHeight(self):
        return self.geoplot.getHeight()

    def build(self):
        multipoints = []
        
        for (status_id,lon,lat,title,fill) in self.tweets:
            html = EmbeddedHtml(encodeTweet(status_id),"",width=300,height=300)
            popup = Popup(html,title)
            multipoints.append(Multipoint([(lon,lat)],popup=popup,fill=fill,marker=self.marker,radius=self.radius,stroke=self.stroke,stroke_width=self.stroke_width))

        for (path_or_url,lon,lat,title,scale,fill) in self.images:
            image = Image(path_or_url=path_or_url,scale=scale)
            popup = Popup(image,title)
            multipoints.append(Multipoint([(lon,lat)],popup=popup,fill=fill,tooltip=title,marker=self.marker,radius=self.radius,stroke=self.stroke,stroke_width=self.stroke_width))

        self.geoplot = Geoplot(multipoints=multipoints)
        self.geoplot.configureLayer(self.ownermap,self.width,self.height,self.boundaries,self.projection,self.zoom_to)
        self.geoplot.build()


    def draw(self,doc,cx,cy):
        self.geoplot.draw(doc,cx,cy)
        with open(os.path.join(os.path.split(__file__)[0],"poi.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = {}
        Js.registerJs(doc,self,jscode,"POI",cx,cy,config)
        doc.getDiagram().connect(self,"zoom",self.geoplot,"zoom")
        doc.getDiagram().connect(self,"visible_window",self.geoplot,"visible_window")
