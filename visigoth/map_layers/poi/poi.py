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
from visigoth.map_layers.poi.twitter import encodeTweet
from visigoth.utils.js import Js
from visigoth.utils.data import Dataset
from visigoth.utils.colour import DiscretePalette, ContinuousPalette
from visigoth.utils.marker import MarkerManager


class POI(Geoplot):

    """
    Plot points of interest as media popups

    Arguments:
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)

    Keyword Arguments:
        lat (str or int): Identify the column to provide the latitude value for each point
        lon (str or int): Identify the column to provide the longitude value for each point
        colour (str or int): Identify the column to define the point colour (use palette default colour if not specified)
        label (str or int): Identify the column to define the label
        size (str or int): Identify the column to determine the size of each marker
        tweet (str or int): Identify the column containing a tweet status (identifier)
        image (str or int): Identify the column containing a path or url of an image
        image_scale (str or int): Identify the column containing the amount to scale an image
        palette(object) : a ContinuousPalette or DiscretePalette instance to control chart colour
        marker_manager(object) : a MarkerManager instance to control marker appearance
    """

    def __init__(self, data, lon=0, lat=1, colour=None, label=None, size=None, tweet=None, image=None, image_scale=None, palette=None, marker_manager=None):
        super().__init__()
        self.dataset = Dataset(data)

        self.lat = lat
        self.lon = lon
        self.colour = colour
        self.label = label
        self.size = size
        self.tweet = tweet
        self.image = image
        self.image_scale = image_scale

        if not palette:
            if not self.colour or self.dataset.isDiscrete(self.colour):
                palette = DiscretePalette()
            else:
                palette = ContinuousPalette()
        self.setPalette(palette)

        if not marker_manager:
            marker_manager = MarkerManager()
            marker_manager.setMarkerType("pin")
            marker_manager.setDefaultRadius(15)
        self.setMarkerManager(marker_manager)

        self.tweets = []
        self.images = []

        for (size,colour) in self.dataset.query([self.size,self.colour]):
            self.getMarkerManager().noteSize(size)
            self.getPalette().getColour(colour)

    def getBoundaries(self):
        return MapLayer.computeBoundaries(self.dataset.query([self.lon,self.lat]))

    def build(self):
        super().clear()
        data = self.dataset.query([self.lon, self.lat, self.label, self.colour, self.size, self.tweet, self.image, self.image_scale])

        for (lon,lat,label,colour,size,tweet,image,image_scale) in data:
            marker = self.getMarkerManager().getMarker(size)
            col = self.palette.getColour(colour)
            if tweet:
                html = EmbeddedHtml(encodeTweet(tweet), "", width=300, height=300)
                popup = Popup(html, label)
                self.add(Multipoint([(lon, lat)], popup=popup, marker=marker, fill=col))

            if image:
                scale = image_scale if image_scale is not None else 1.0
                image = Image(path_or_url=image,scale=scale)
                popup = Popup(image,label)
                self.add(Multipoint([(lon,lat)],popup=popup,fill=col,tooltip=label,marker=marker))
        super().build()

    def draw(self,doc,cx,cy):
        config = super().draw(doc,cx,cy,False)
        with open(os.path.join(os.path.split(__file__)[0],"poi.js"),"r") as jsfile:
            jscode = jsfile.read()
        Js.registerJs(doc,self,jscode,"POI",cx,cy,config)
        # doc.getDiagram().connect(self,"zoom",self.geoplot,"zoom")
        # doc.getDiagram().connect(self,"visible_window",self.geoplot,"visible_window")
