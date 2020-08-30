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

import os
import urllib
from xml.dom.minidom import parseString

from visigoth.common.image import Image
from visigoth.utils.httpcache import HttpCache
from visigoth.map_layers import MapLayer
from visigoth.utils.js import Js
from visigoth.utils.mapping import Projections

class WMS(MapLayer):

    mundialis_url = "http://ows.mundialis.de/services/service?&VERSION=1.1.1"

    gibs_4326_url = "https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?VERSION=1.1.1"

    gibs_3857_url = "https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi?VERSION=1.1.1"

    gibs_attribution = ("We acknowledge the use of imagery provided by services from NASA's Global Imagery Browse Services (GIBS), part of NASA's Earth Observing System Data and Information System (EOSDIS).","https://earthdata.nasa.gov/")
    mundialis_attribution = ("Contains modified SRTM data (2014)/NASA, processed by mundialis (www.mundialis.de) and vector data by OpenStreetMap contributors (2020), www.openstreetmap.org","https://www.mundialis.de/en/ows-mundialis/")

    layer_lookup = {
        ("satellite","EPSG:3857"):(gibs_3857_url,"Landsat_WELD_CorrectedReflectance_TrueColor_Global_Annual",gibs_attribution),
        ("satellite", "EPSG:4326"):(gibs_4326_url, "Landsat_WELD_CorrectedReflectance_TrueColor_Global_Annual",gibs_attribution),
        ("osm","EPSG:3857"):(mundialis_url,"OSM-WMS",mundialis_attribution),
        ("osm","EPSG:4326"):(mundialis_url,"OSM-WMS",mundialis_attribution),
    }

    """
    Create a WMS plot

    Keyword Arguments:
        type(str): "satellite" or "osm"
        image(str): type of image, for example "jpeg", "png"
        layer_name(str): the name of the layer to use
        url(str): a URL with the following format strings %(height)d, %(width)d, %(e_min)f, %(e_max)f, %(n_min)f, %(n_max)f
        date(datetime): date for which imagery is requested
        attribution(str): a citation or acknowledgement for the data provider
        attribution_url(str): a URL for the data provider
        embed_images(bool): whether to download and embed images into the document or link to them
        
        Note: specify either (type AND image) OR (url)
        Note: WMS layer can only currently work with the default Web Mercator (EPSG:3857) or Platte-Carrerre (EPSG:4326) projection
    """
    def __init__(self,
        type="satellite",
        image="png",
        layer_name="",
        url="",
        date=None,
        attribution="",
        attribution_url="",
        embed_images=True
        ):
        super(WMS, self).__init__()
        self.bounds = None
        self.width = None
        self.attribution = attribution
        self.attribution_url = attribution_url
        self.url = url
        self.date = date
        self.layer_name = layer_name
        self.projection = None
        self.type = type
        self.image = image
        self.content = {}
        self.embed_images = embed_images

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to,fmt):
        self.ownermap = ownermap
        self.width = width
        self.height = int(height)
        self.bounds = boundaries
        self.projection = projection
        self.zoom_to = zoom_to

    @staticmethod
    def getCapabilitiesUrl(base_url):
        scheme, netloc, path, query_string, fragment = urllib.parse.urlsplit(base_url)
        params = urllib.parse.parse_qs(query_string)
        keys = list(params.keys())
        for key in keys:
            if key != "SERVICE" and key != "VERSION":
                del params[key]

        if "VERSION" not in params:
            params["VERSION"] = "1.1.1"

        params["SERVICE"] = "WMS"
        params["REQUEST"] = "GetCapabilities"
        query_string = urllib.parse.urlencode(params, doseq=True)
        return urllib.parse.urlunsplit((scheme, netloc, path, query_string, fragment))

    @staticmethod
    def getFeatureInfoUrl(parameters, x, y, type = "satellite",projection = Projections.EPSG_3857,layer_name="", url = ""):
        projname = projection.getName()
        details = WMS.layer_lookup.get((type,projname), None)
        if not url:
            url = details[0]
        if not layer_name:
            layer_name = details[1]
        scheme, netloc, path, query_string, fragment = urllib.parse.urlsplit(url)
        params = urllib.parse.parse_qs(query_string)
        keys = list(params.keys())
        for key in keys:
            if key != "SERVICE" and key != "VERSION":
                del params[key]

        if "VERSION" not in params:
            params["VERSION"] = "1.1.1"

        params["SRS"] = projname
        params["TRANSPARENT"] = "true"
        params["FORMAT"] = "image/%(image_type)s" % (parameters)
        params["QUERY_LAYERS"] = layer_name
        params["LAYERS"] = layer_name

        params["HEIGHT"] = "%(height)d" % (parameters)
        params["WIDTH"] = "%(width)d" % (parameters)
        params["BBOX"] = "%(e_min)f,%(n_min)f,%(e_max)f,%(n_max)f" % (parameters)
        params["X"] = x
        params["Y"] = y
        params["INFO_FORMAT"] = "text/xml"

        if "date" in parameters:
            params["TIME"] = parameters["date"].strftime("%Y-%m-%d")

        params["SERVICE"] = "WMS"
        params["REQUEST"] = "GetFeatureInfo"
        query_string = urllib.parse.urlencode(params, doseq=True)
        return urllib.parse.urlunsplit((scheme, netloc, path, query_string, fragment))

    @staticmethod
    def getMapUrl(base_url,parameters):
        # good concise summary of the WMS protocol
        # https://www.nrcan.gc.ca/earth-sciences/geomatics/canadas-spatial-data-infrastructure/standards-policies/8938
        scheme, netloc, path, query_string, fragment = urllib.parse.urlsplit(base_url)
        params = urllib.parse.parse_qs(query_string)
        if "VERSION" not in params:
            params["VERSION"] = "1.1.1"
        if "STYLES" not in params:
            params["STYLES"] = ""
        params["SERVICE"] = "WMS"
        params["SRS"] = "%(projection)s" % (parameters)
        params["TRANSPARENT"] = "true"
        params["FORMAT"] = "image/%(image_type)s" % (parameters)
        params["LAYERS"] = "%(layers)s" % (parameters)
        params["HEIGHT"] = "%(height)d" % (parameters)
        params["WIDTH"] = "%(width)d" % (parameters)
        params["BBOX"] = "%(e_min)f,%(n_min)f,%(e_max)f,%(n_max)f" % (parameters)
        params["REQUEST"] = "GetMap"
        if "date" in parameters:
            params["TIME"] = parameters["date"].strftime("%Y-%m-%d")


        query_string = urllib.parse.urlencode(params, doseq=True)
        return urllib.parse.urlunsplit((scheme, netloc, path, query_string, fragment))

    @staticmethod
    def getLayerNames(type = "satellite",projection = Projections.EPSG_3857,url = ""):
        projname = projection.getName()
        if not url:
            details = WMS.layer_lookup.get((type,projname), None)
            url = details[0]

        capabilities_url = WMS.getCapabilitiesUrl(url)

        # fire off the GetCapabilities request
        capabilities = HttpCache.fetch(capabilities_url)

        s = capabilities.decode("utf-8")

        d = parseString(s)
        layer_names = []

        def getText(node):
            rc = []
            for childnode in node.childNodes:
                if childnode.nodeType == node.TEXT_NODE:
                    rc.append(childnode.data)
            return ''.join(rc)

        layers = d.getElementsByTagName("Layer")
        for layer in layers:
            names = layer.getElementsByTagName("Name")
            for name in names:
                if name.parentNode == layer:
                    layer_names.append(getText(name))

        return layer_names

    @staticmethod
    def getFeatureInfo(parameters, x, y, type="satellite", projection=Projections.EPSG_3857,url=""):
        info_url = WMS.getFeatureInfoUrl(parameters,x,y,type,projection,url=url)
        info = HttpCache.fetch(info_url)
        print(info.decode("utf-8"))

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def build(self,fmt):
        url = self.url
        projname = self.projection.getName()
        attribution = self.attribution
        attribution_url = self.attribution_url
        if not url:
            details = WMS.layer_lookup.get((self.type,projname),None)
            if details is not None:
                (url,layer_name,attribution) = details
                (attribution,attribution_url) = attribution
            else:
                raise Exception("No WMS configuration for combination "+str((self.type,projname)))
        if self.layer_name:
            layer_name = self.layer_name
        self.setInfo(name="WMS", attribution=attribution, url=attribution_url)

        (lonmin,latmin) = self.bounds[0]
        (lonmax,latmax) = self.bounds[1]
        (xmin,ymin) = self.projection.fromLonLat((lonmin,latmin))
        (xmax,ymax) = self.projection.fromLonLat((lonmax,latmax))

        zoom = 1
        while zoom <= self.zoom_to:
            self.content[zoom] = {}
            for zx in range(zoom):
                for zy in range(zoom):
                    x1 = xmin + zx*(xmax-xmin)/zoom
                    x2 = xmin + (zx+1)*(xmax-xmin)/zoom
                    y1 = ymin + zy*(ymax-ymin)/zoom
                    y2 = ymin + (zy+1)*(ymax-ymin)/zoom
                    parameters = {
                        "layers":layer_name,
                        "projection":projname,
                        "e_min":x1,
                        "n_min":y1,
                        "e_max":x2,
                        "n_max":y2,
                        "image_type":self.image,
                        "width":self.width,
                        "height":self.height}
                    if self.date != None:
                        parameters["date"] = self.date
                    resolved_url = WMS.getMapUrl(url,parameters)
                    if self.embed_images:
                        try:
                            self.content[zoom][(zx,zy)] = HttpCache.fetch(resolved_url)
                        except:
                            print("Unable to download WMS image from %s"%(resolved_url))
                            self.content[zoom][(zx, zy)] = b""
                    else:
                        self.content[zoom][(zx, zy)] = resolved_url
            zoom *= 2


    def getBoundaries(self):
        return self.bounds

    def draw(self,doc,cx,cy):
        zoom_groups = []
        ox = cx - self.width/2
        oy = cy - self.height/2
        zoom = 1
        while zoom <= self.zoom_to:
            g = doc.openGroup()
            g.addAttr("pointer-events","none")
            if zoom != 1:
                g.addAttr("visibility","hidden")
            tw = self.width/zoom
            th = self.height/zoom
            for zx in range(zoom):
                for zy in range(zoom):
                    i = None
                    if self.embed_images:
                        bytes = self.content[zoom][(zx,zy)]
                        if bytes:
                            i = Image("image/%s"%(self.image),content_bytes=bytes,width=tw,height=th)
                    else:
                        url = self.content[zoom][(zx, zy)]
                        i = Image("image/%s" % (self.image), path_or_url=url, width=tw, height=th, embed_image=False)
                    if i:
                        i.draw(doc, ox + (zx + 0.5) * tw, oy + self.height - (zy + 0.5) * th)
            zoom_groups.append(g.getId())
            doc.closeGroup()
            zoom *= 2

        with open(os.path.join(os.path.split(__file__)[0],"wms.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = { "zoom_groups":zoom_groups }
        Js.registerJs(doc,self,jscode,"wms",cx,cy,config)
