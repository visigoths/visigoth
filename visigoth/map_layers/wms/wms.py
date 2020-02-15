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

import math
import os

from visigoth.common import DiagramElement
from visigoth.common.image import Image
from visigoth.utils.mapping import Mapping
from visigoth.utils.httpcache import HttpCache
from visigoth.map_layers import MapLayer
from visigoth.utils.mapping import Metadata
from visigoth.utils.js import Js

class WMS(MapLayer):

    eox_url = "https://tiles.maps.eox.at/wms?service=WMS&version=1.1.1&request=GetMap&layers=%(layers)s&srs=%(projection)s&bbox=%(e_min)f,%(n_min)f,%(e_max)f,%(n_max)f&format=image/%(image_type)s&width=%(width)d&height=%(height)d"

    layer_lookup = {
        ("satellite","EPSG:3857"):"s2cloudless_3857",
        ("osm","EPSG:3857"):"osm_3857",
        ("satellite","EPSG:4326"):"s2cloudless",
        ("osm","EPSG:4326"):"osm",
    }

    """
    Create a WMS plot

    Keyword Arguments:
        type(str): "satellite" or "osm"
        image(str): type of image, for example "jpeg", "png"
        custom_url(str): a URL with the following format strings %(height)d, %(width)d, %(e_min)f, %(e_max)f, %(n_min)f, %(n_max)f
        
        Note: specify either type/image (for EOX WMS service) or custom_url
        Note: WMS can only currently work with the default Web Mercator (EPSG:3857) or Platte-Carrerre (ESPG:4326) projection
    """
    def __init__(self,
        type="satellite",
        image="jpeg",
        custom_url=""):
        super(WMS, self).__init__()
        if not custom_url:
            self.setInfo(name="WMS",attribution="Data © OpenStreetMap contributors and others, Rendering © EOX",url="https://maps.eox.at/")
        self.bounds = None
        self.width = None
        self.custom_url = custom_url
        self.projection = None
        self.type = type
        # https://tiles.maps.eox.at/wms?service=wms&request=getcapabilities
        self.image = image
        self.content = {}


    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
        self.ownermap = ownermap
        self.width = width
        self.height = int(height)
        self.bounds = boundaries
        self.projection = projection
        self.zoom_to = zoom_to


    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def build(self):
        type_proj = (self.type,self.projection.getName())
        layer_name = WMS.layer_lookup.get(type_proj,None)
        if layer_name == None:
            raise Exception("No WMS configuration for combination "+str(type_proj))
        self.layers = [layer_name]
        (lonmin,latmin) = self.bounds[0]
        (lonmax,latmax) = self.bounds[1]
        (xmin,ymin) = self.projection.fromLonLat((lonmin,latmin))
        (xmax,ymax) = self.projection.fromLonLat((lonmax,latmax))
                 
        projname = self.projection.getName()
        layers = ",".join(self.layers)
        for zoom in range(1,self.zoom_to+1):
            self.content[zoom] = {}
            for zx in range(zoom):
                for zy in range(zoom):
                    x1 = xmin + zx*(xmax-xmin)/zoom
                    x2 = xmin + (zx+1)*(xmax-xmin)/zoom
                    y1 = ymin + zy*(ymax-ymin)/zoom
                    y2 = ymin + (zy+1)*(ymax-ymin)/zoom
                    if not self.custom_url:
                        url = WMS.eox_url%{"layers":layers,"projection":projname,"e_min":x1,"n_min":y1,"e_max":x2,"n_max":y2,"image_type":self.image,"width":self.width,"height":self.height}
                    else:
                        url = self.custom_url%{"e_min":x1,"n_min":y1,"e_max":x2,"n_max":y2,"width":self.width,"height":self.height}
                    self.content[zoom][(zx,zy)] = HttpCache.fetch(url)
                
    def getBoundaries(self):
        return self.bounds

    def draw(self,doc,cx,cy):
        zoom_groups = []
        ox = cx - self.width/2
        oy = cy - self.height/2
        for zoom in range(1,self.zoom_to+1):
            g = doc.openGroup()
            g.addAttr("pointer-events","none")
            if zoom != 1:
                g.addAttr("visibility","hidden")
            tw = self.width/zoom
            th = self.height/zoom
            for zx in range(zoom):
                for zy in range(zoom):
                    i = Image("image/%s"%(self.image),content_bytes=self.content[zoom][(zx,zy)],width=tw,height=th)
                    i.draw(doc,ox+(zx+0.5)*tw,oy+self.height-(zy+0.5)*th)

            zoom_groups.append(g.getId())
            doc.closeGroup()
        with open(os.path.join(os.path.split(__file__)[0],"wms.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = { "zoom_groups":zoom_groups }
        Js.registerJs(doc,self,jscode,"wms",cx,cy,config)

