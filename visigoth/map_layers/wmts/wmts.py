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

from visigoth.common.image import Image
from visigoth.utils.httpcache import HttpCache
from visigoth.utils.js import Js
from visigoth.map_layers import MapLayer

class WMTS(MapLayer):

    default_osm_url = "https://a.tile.openstreetmap.de/%(zoom)d/%(tilex)d/%(tiley)d.png"

    """
    Create a WMTS plot using open streetmap by default
    
    Keyword Arguments:
            url(str): WMTS url with three  format string parameters %(zoom)d, %(tilex)d, %(tiley)d

            Note:  WMTS can only currently work with the default Web Mercator (ESPG:3857) projection
    """
    def __init__(self,url=default_osm_url):
        super(WMTS, self).__init__()
        if url == WMTS.default_osm_url:
            self.setInfo(name="WMTS",attribution="© OpenStreetMap contributors",url="http://www.openstreetmap.org/copyright")
        self.bounds = None
        self.width = None
        self.wmts_url = url

        self.image = "png"
        if self.wmts_url.endswith("jpg"):
            self.image = "jpeg"

        self.projection = None
        self.content = {}
        self.zoom = 0
    
    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
        self.ownermap = ownermap
        self.width = width
        self.height = int(height)
        self.bounds = boundaries
        self.projection = projection
        self.zoom_to = zoom_to

        if self.projection.getName() != "EPSG:3857":
            raise Exception("WMTS layer does not yet support projection=\""+self.projection.getName()+"\" - currently only \"ESPG:3857\" is supported")

    def getTileWidthM(self,lat_deg,zoom_level):
        return 40075016.686*math.cos(math.radians(lat_deg))/(2**zoom_level)

    def getTileXY(self,lat_deg,lon_deg,zoom):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = (lon_deg + 180.0) / 360.0 * n
        ytile = (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n
        return (int(xtile), int(ytile), xtile-int(xtile), ytile-int(ytile))

    def getTileLocationNWLonLat(self,xtile,ytile,zoom):
        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return (lon_deg,lat_deg)

    def getTileLocationNW(self,xtile,ytile,zoom):
        (lon_deg,lat_deg) = self.getTileLocationNWLonLat(xtile,ytile,zoom)
        return self.projection.fromLonLat((lon_deg,lat_deg))
    
    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def build(self):
        (lonmin,latmin) = self.bounds[0]
        (lonmax,latmax) = self.bounds[1]

        latmid = latmin + (latmax-latmin)/2
        lonmid = lonmin + (lonmax-lonmin)/2

        (xmin,ymin) = self.projection.fromLonLat((lonmin,latmin))
        (xmax,ymax) = self.projection.fromLonLat((lonmax,latmax))

        (lonmid,latmid) = self.projection.toLonLat((xmin+0.5*(xmax-xmin),ymin+0.5*(ymax-ymin)))
        width_m = xmax-xmin
        m_per_pixel = width_m/self.width

        for zoom in range(0,16):
            widthM = self.getTileWidthM(latmid,zoom)   
            if (widthM / 256.0 < m_per_pixel):
                break
        print("Selected zoom %d"%(zoom))

        self.zoom = zoom

        zoom_level = 1
        while zoom_level <= self.zoom_to:
            self.content[zoom_level] = {}

            zoom = self.zoom + zoom_level - 1
            width = self.width*zoom_level

            (txmin,tymax,_,_) = self.getTileXY(latmin,lonmin,zoom)
            (txmax,tymin,_,_) = self.getTileXY(latmax,lonmax,zoom)
            (tx,ty,xoff,yoff) = self.getTileXY(latmid,lonmid,zoom)

            # get xmin/max of NW tile
            (nwxmin,_) = self.getTileLocationNW(txmin,tymin,zoom)
            (nwxmax,_) = self.getTileLocationNW(txmin+1,tymin+1,zoom)

            tiles_m_per_pixel = (nwxmax-nwxmin)/256.0
            target_m_per_pixel = (xmax-xmin)/float(width)

            self.content[zoom_level]["scale"] = tiles_m_per_pixel/target_m_per_pixel
            self.content[zoom_level]["offset_x"] = (256.0/zoom_level)*(xoff+(tx-txmin))
            self.content[zoom_level]["offset_y"] = (256.0/zoom_level)*(yoff+(ty-tymin))
            self.content[zoom_level]["tiles"] = {}
            #print("scale="+str(self.scale))
            #print("offset:"+str(self.offset_x)+","+str(self.offset_y))

            for tilex in range(txmin,txmax+1):
                for tiley in range(tymin,tymax+1):
                    url =  self.wmts_url%{"zoom":zoom,"tilex":tilex,"tiley":tiley}
                    self.content[zoom_level]["tiles"][(tilex,tiley)] = HttpCache.fetch(url)

            zoom_level *= 2

    def getBoundaries(self):
        return self.bounds

    def draw(self,doc,cx,cy):
    
        zoom_groups = []
        zoom = 1
        while zoom <= self.zoom_to:
            ox = cx - self.width/2
            oy = cy - self.height/2
        
            tiles = self.content[zoom]["tiles"]
            scale = self.content[zoom]["scale"]
            offset_x = self.content[zoom]["offset_x"]
            offset_y = self.content[zoom]["offset_y"]
            
            g = doc.openGroup()
            if zoom != 1:
                g.addAttr("visibility","hidden")
            xtilemin = min([xtile for (xtile,_) in tiles])
            ytilemin = min([ytile for (_,ytile) in tiles])
            tilesz = 256.0/zoom
            for (xtile,ytile) in tiles:
                i = Image("image/%s"%(self.image),content_bytes=tiles[(xtile,ytile)],width=tilesz,height=tilesz)
                i.draw(doc,ox+tilesz/2+tilesz*(xtile-xtilemin),oy+tilesz/2+tilesz*(ytile-ytilemin))
                # r = rectangle(ox+256*(xtile-xtilemin),oy+256*(ytile-ytilemin),256,256,stroke_width=1,stroke="red")
                # doc.add(r)
            
            dx = self.width/2-offset_x
            dy = self.height/2-offset_y
            
            tx = -1*(cx-dx)*(scale-1)
            ty = -1*(cy-dy)*(scale-1)

            transform0 = "translate("+str(dx)+","+str(dy)+")"
            transform0 += " translate("+str(tx)+","+str(ty)+")"
            transform0 += " scale("+str(scale)+")"

            g.addAttr("transform",transform0)
            zoom_groups.append(g.getId())
            doc.closeGroup()

            zoom *= 2

        with open(os.path.join(os.path.split(__file__)[0],"wmts.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = { "zoom_groups":zoom_groups }
        Js.registerJs(doc,self,jscode,"wmts",cx,cy,config)
        