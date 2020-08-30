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
import os

from visigoth.common.image import Image
from visigoth.utils.httpcache import HttpCache
from visigoth.utils.js import Js
from visigoth.map_layers import MapLayer
from visigoth.svg import rectangle

TRANSPARENT_1PIXEL = bytes([137,80,78,71,13,10,26,10,0,0,0,13,73,72,68,82,0,0,0,1,0,0,0,1,8,6,0,0,0,31,21,196,137,0,0,0,13,73,68,65,84,24,87,99,248,255,255,255,127,0,9,251,3,253,5,67,69,202,0,0,0,0,73,69,78,68,174,66,96,130])

class WMTS(MapLayer):

    default_url = "https://a.tile.openstreetmap.de/{z}/{x}/{y}.png"
    default_attribution = "© OpenStreetMap contributors"
    default_attribution_link = "http://www.openstreetmap.org/copyright"

    """
    Add a WMTS base map using open streetmap by default
    
    Keyword Arguments:
            url(str): WMTS url with three  format string parameters {z}, {x}, {y}
            image_type(str): the type of the returned images as "jpeg" or "png", can usually be determined from the URL
            attribution(str): set the attribution text for the WMTS provider
            attribution_link(str): set the attribution link for the WMTS provider
            
    Note:  this WMTS layer can only currently work with the default Web Mercator (EPSG:3857) projection
    """
    def __init__(self,url=default_url,image_type=None,attribution=default_attribution, default_attribution_link=default_attribution_link,embed_images=True):
        super(WMTS, self).__init__()
        if url == WMTS.default_url:
            self.setInfo(name="WMTS",attribution=attribution,url=default_attribution_link)
        self.bounds = None
        self.width = None
        self.wmts_url = url

        self.image = image_type

        if not self.image:
            if self.wmts_url.endswith("jpg") or self.wmts_url.endswith("jpeg"):
                self.image = "jpeg"
            else:
                self.image = "png"

        self.projection = None
        self.content = {}
        self.zoom = 0
        self.embed_images = embed_images
    
    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to,fmt):
        self.ownermap = ownermap
        self.width = width
        self.height = int(height)
        self.bounds = boundaries
        self.projection = projection
        self.zoom_to = zoom_to

        if self.projection.getName() != "EPSG:3857":
            raise Exception("WMTS layer does not yet support projection=\""+self.projection.getName()+"\" - currently only \"EPSG:3857\" is supported")

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

    def build(self,fmt):
        (lonmin,latmin) = self.bounds[0]
        (lonmax,latmax) = self.bounds[1]

        (xmin,ymin) = self.projection.fromLonLat((lonmin,latmin))
        (xmax,ymax) = self.projection.fromLonLat((lonmax,latmax))

        (lonmid,latmid) = self.projection.toLonLat((xmin+0.5*(xmax-xmin),ymin+0.5*(ymax-ymin)))
        width_m = xmax-xmin
        m_per_pixel = width_m/self.width

        for zoom in range(0,16):
            widthM = self.getTileWidthM(latmid,zoom)   
            if (widthM / 256.0 < m_per_pixel):
                break

        self.zoom = zoom

        zoom_level = 1
        wmts_zoom = self.zoom
        while zoom_level <= self.zoom_to:
            self.content[zoom_level] = {}

            print("wmts zoom=",wmts_zoom)
            width = self.width*zoom_level

            (txmin,tymax,_,_) = self.getTileXY(latmin,lonmin,wmts_zoom)
            (txmax,tymin,_,_) = self.getTileXY(latmax,lonmax,wmts_zoom)
            (tx,ty,xoff,yoff) = self.getTileXY(latmid,lonmid,wmts_zoom)

            # get xmin/max of NW tile
            (nwxmin,_) = self.getTileLocationNW(txmin,tymin,wmts_zoom)
            (nwxmax,_) = self.getTileLocationNW(txmin+1,tymin+1,wmts_zoom)

            tiles_m_per_pixel = (nwxmax-nwxmin)/256.0
            target_m_per_pixel = (xmax-xmin)/float(width)

            self.content[zoom_level]["scale"] = tiles_m_per_pixel/target_m_per_pixel
            self.content[zoom_level]["offset_x"] = (256.0/zoom_level)*(xoff+(tx-txmin))
            self.content[zoom_level]["offset_y"] = (256.0/zoom_level)*(yoff+(ty-tymin))
            self.content[zoom_level]["tiles"] = {}

            for tilex in range(txmin,txmax+1):
                for tiley in range(tymin,tymax+1):
                    url =  self.wmts_url.replace("{z}",str(wmts_zoom)).replace("{x}",str(tilex)).replace("{y}",str(tiley))
                    if self.embed_images:
                        try:
                            self.content[zoom_level]["tiles"][(tilex,tiley)] = HttpCache.fetch(url)
                        except Exception as ex:
                            print("Unable to download WMS image from %s: %s" % (url,str(ex)))
                            self.content[zoom_level]["tiles"][(tilex, tiley)] = b""
                    else:
                        self.content[zoom_level]["tiles"][(tilex, tiley)] = url
            zoom_level *= 2
            wmts_zoom += 1

    def getBoundaries(self):
        return self.bounds

    def draw(self,doc,cx,cy):
    
        zoom_groups = []
        zoom_levels = {}
        zoom = 1
        image_urls_by_zoom = {} # zoom => { image-id => url }
        while zoom <= self.zoom_to:
            image_urls = {}
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
                i = None
                if self.embed_images:
                    image_content = tiles[(xtile,ytile)]
                    if image_content:
                        i = Image("image/%s"%(self.image),content_bytes=image_content,width=tilesz,height=tilesz)
                else:
                    url = tiles[(xtile, ytile)]
                    if zoom == 1:
                        i = Image("image/%s" % (self.image), path_or_url=url, width=tilesz,height=tilesz, embed_image=False)
                    else:
                        i = Image("image/%s" % (self.image), content_bytes=TRANSPARENT_1PIXEL, width=tilesz, height=tilesz)

                iid = i.draw(doc,ox+tilesz/2+tilesz*(xtile-xtilemin),oy+tilesz/2+tilesz*(ytile-ytilemin))
                if not self.embed_images:
                    image_urls[iid] = url
                    print(zoom,iid,url)

            dx = self.width/2-offset_x
            dy = self.height/2-offset_y
            
            tx = -1*(cx-dx)*(scale-1)
            ty = -1*(cy-dy)*(scale-1)

            transform0 = "translate("+str(dx+tx)+","+str(dy+ty)+")"
            # transform0 += " translate("+str(tx)+","+str(ty)+")"
            transform0 += " scale("+str(scale)+")"

            zoom_levels[str(zoom)] = {"scale": scale, "offset_x": dx+tx, "offset_y":dy+ty}

            g.addAttr("transform",transform0)
            zoom_groups.append(g.getId())
            doc.closeGroup()
            image_urls_by_zoom[str(zoom)] = image_urls
            zoom *= 2

        guide = rectangle(cx,cy,0,0,stroke="red",stroke_width=1)
        guide_id = guide.getId()
        doc.add(guide)
        with open(os.path.join(os.path.split(__file__)[0],"wmts.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = { "zoom_groups":zoom_groups, "zoom_levels":zoom_levels, "guide_id":guide_id }
        if not self.embed_images:
            config["image_urls_by_zoom"] = image_urls_by_zoom
        Js.registerJs(doc,self,jscode,"wmts",cx,cy,config)
        