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

from visigoth.svg import image, embedded_svg
from visigoth.common.diagram_element import DiagramElement
from visigoth.utils.httpcache import HttpCache
import base64
import struct

class Image(DiagramElement):

    """
    Create an Image (gif,png and jpeg formats are supported)

    Keyword Arguments:
        mime_type(str) : the mime type (either image/png, image/jpeg or image/gif)
        content_bytes(list) : list with the raw bytes of the image
        path_or_url(str) : the path or URL to the image file
        width(int) : the width of the image in bytes
        height(int) : the height of the image in bytes
        scale(float) : used to scale the image
        tooltip(str) : a tooltip to display when hovering over the image
    Notes:
        Caller must provide EITHER path_or_url OR (content_bytes AND mimeType)
        If width and height are not provided they will be extracted from the image
    """
    def __init__(self,mime_type="",content_bytes=[],path_or_url="",width=0,height=0,scale=1.0,tooltip=""):
        DiagramElement.__init__(self)
        self.mimeType=mime_type
        self.contentBytes=content_bytes
        self.path_or_url=path_or_url
        self.width=width
        self.height=height
     
        self.tooltip=tooltip
        self.scale = scale
        if not self.path_or_url and not (self.contentBytes and self.mimeType):
            raise Exception("Caller must provide path_or_url or contentBytes+mimeType")
            
    def build(self):
        if self.mimeType == "":
            self.extractMimeType()
        if not self.contentBytes:
            self.loadContent()
        if self.width <= 0 or self.height <= 0:
            self.extractDimensions()
        self.width *= self.scale
        self.height *= self.scale

    def extractMimeType(self):
        if self.path_or_url.endswith("gif"):
            self.mimeType = "image/gif"
        elif self.path_or_url.endswith("png"):
            self.mimeType = "image/png"
        elif self.path_or_url.endswith("jpeg") or self.path_or_url.endswith("jpg"):
            self.mimeType = "image/jpeg"
        else:
            raise Exception("Unable to recognise image type as gif,png or jpeg for image path/url: "+self.path_or_url)
    
    def loadContent(self):
        if self.path_or_url.startswith("http"):
            self.contentBytes = HttpCache.fetch(self.path_or_url)
        else:
            self.contentBytes = open(self.path_or_url,"rb").read()
        
    def extractDimensions(self):
        # based on https://gist.github.com/EdgeCaseBerg/8240859
        if self.mimeType == "image/gif":
            w, h = struct.unpack("<HH", self.contentBytes[6:10])
            self.width = int(w)
            self.height = int(h)
        elif self.mimeType == "image/png":
            w, h = struct.unpack(">LL", self.contentBytes[16:24])
            self.width = int(w)
            self.height = int(h)
        elif self.mimeType == "image/jpeg":
            b = self.contentBytes[2]
            ctr = 3
            
            while (b and b != 0xDA):
                while (b != 0xFF): 
                    b = self.contentBytes[ctr]
                    ctr += 1
                while (b == 0xFF): 
                    b = self.contentBytes[ctr]
                    ctr += 1
                if (b >= 0xC0 and b <= 0xC3):
                    ctr += 3
                    h, w = struct.unpack(">HH", self.contentBytes[ctr:ctr+4])
                    ctr += 4
                    break
                else:
                    ctr += int(struct.unpack(">H", self.contentBytes[ctr:ctr+2])[0])
                b = self.contentBytes[ctr]
                ctr += 1
            self.width = int(w)
            self.height = int(h)

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def draw(self,d,cx=None,cy=None,ox=None,oy=None):
        if cy != None:
            oy = cy - self.height/2
        if cx != None:
            ox = cx - self.width/2

        if self.mimeType=="image/svg+xml":
            es = embedded_svg(self.width,self.height,ox,oy,str(self.contentBytes,"utf-8"))
            d.add(es)
        else:
            uri="data:"+self.mimeType+";charset=US-ASCII;base64,"+str(base64.b64encode(self.contentBytes),"utf-8")
            i = image(ox,oy,self.width,self.height,uri,tooltip=self.tooltip)
            d.add(i)
