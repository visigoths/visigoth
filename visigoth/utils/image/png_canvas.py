# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

# pypng_python3.py Converted to Python from Original C-Code by Niall McCarroll, 2008 (Ported to Python3 2013):
#
# This code was written by Martin Hinner <mhi@penguin.cz> in 2000,
# no copyright is claimed. This code is in the public domain;
# do with it what you wish.
#

from zlib import crc32, compressobj


class PngCanvas(object):
    
    def __init__(self,height,width,text_attributes={}):
        self.height = height
        self.width = width
        self.bits = 8
        # data format is (r,g,b,a,index), initialise to black
        self.data = [(0,0,0,0,0) for i in range(0,width*height)]
        self.colors=(1 << self.bits)
        self.crc = 0
        self.allocated_colours = []
        self.png_magic = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
        self.compressor = compressobj(9)
        self.buffer = None
        self.text_attributes=text_attributes

    def init_palette(self,palette):
        self.plt = []
        self.trns = []
        for (r,g,b,t) in palette:
            self.plt.append((r<<16)|(g<<8)|b)
            self.trns.append(t)
        for p in range(0,256-len(palette)):
            self.plt.append(0)
            self.trns.append(255)
    
    def addpixel(self,x,y,r,g,b,a):
        """Add a pixel with a given colour (r,g,b,a) to the canvas, coordinate system is left-right (x) and top-bottom (y)"""
        index = None
        if self.allocated_colours is not None:
            # we are still attempting to use colour indexes rather than RGBA
            try:
                # see if an existing index is allocated
                index = self.allocated_colours.index((r,g,b,a))
            except Exception as ex:
                # we need a new index for this colour combination
                index = len(self.allocated_colours)
                self.allocated_colours.append((r,g,b,a))
                # check if we exceed 256 indices, the maximum allowed
                if len(self.allocated_colours) > 256:
                    # too many, so remove the allocated colours and fall back to RGBA
                    self.allocated_colours = None # overflow palette
                    index = None
        self.data[x + (y * self.width)] = (r,g,b,a,index)
        
    def pixel(self,x,y):
        return self.data[x+(y*self.width)]

    def write(self, file):
        if self.allocated_colours is not None:
            self.init_palette(self.allocated_colours)
            
        self.fd = file

        self.resetcrc()

        self.fd.write(self.png_magic)

        self.beginchunk(b"IHDR", 0x0d)
        self.writelongcrc(self.width)  # width
        self.writelongcrc(self.height)  # height
        self.writebytecrc(self.bits)  # bit depth
        if self.allocated_colours is not None:
            self.writebytecrc(3)  # color type = indexed
        else:
            self.writebytecrc(6)  # color type = truecolor RGBA
        self.writebytecrc(0)  # compression
        self.writebytecrc(0)  # filter
        self.writebytecrc(0)  # interlace
        self.endchunk()

        if self.allocated_colours is not None:
            self.beginchunk(b"PLTE", self.colors * 3);
            i = 0
            while i < self.colors:
                j = 0
                while j < 3:
                    self.writebytecrc((self.plt[i] >> ((2 - j) * 8)) & 0xFF)
                    j += 1
                i += 1
            self.endchunk()

            self.beginchunk(b"tRNS", self.colors);
            i = 0
            while i < self.colors:
                self.writebytecrc(self.trns[i])
                i += 1
            self.endchunk()

        i = 0
        data = bytearray()
        while i < self.height:
            data += bytes([0])
            k = 0
            while k < self.width:
                (r, g, b, a, c) = self.pixel(k, i)
                if self.allocated_colours:
                    data += bytes([c])
                else:
                    data += bytes([r, g, b, a])
                k += 1
            i += 1

        self.write_compressedchunk(b'IDAT',data)

        if self.text_attributes:
            for key in self.text_attributes.keys():
                val = self.text_attributes[key]
                keybytes = key.encode("utf-8")
                valbytes = val.encode("utf-8")
                chunklen = len(keybytes)+len(valbytes)+5
                self.beginchunk(b"iTXt", chunklen)
                self.writebuffercrc(keybytes)
                self.writebytecrc(0) # NULL terminator for key
                self.writebytecrc(0) # Compression = 0
                self.writebytecrc(0) # Compression method: 0
                # Language tag: ""
                self.writebytecrc(0) # NULL
                # Translated tag: ""
                self.writebytecrc(0) # NULL
                self.writebuffercrc(valbytes)
                self.endchunk()

        self.beginchunk(b"IEND", 0)
        self.endchunk()
    
    def resetcrc(self):
        self.crc = 0

    def writebytes(self, bytes):
        self.fd.write(bytes)

    def writelong(self,l):
        self.writebytes(bytes([(l>>24)&0xFF,(l>>16)&0xFF,(l>>8)&0xFF,l&0xFF]))
        
    def writelongcrc(self,l):
        c3 = bytes([(l>>24)&0xFF])
        c2 = bytes([(l>>16)&0xFF])
        c1 = bytes([(l>>8)&0xFF])
        c0 = bytes([l&0xFF])
        self.crc = crc32(c3,self.crc)
        self.writebytes(c3)
        self.crc = crc32(c2,self.crc)
        self.writebytes(c2)
        self.crc = crc32(c1,self.crc)
        self.writebytes(c1)
        self.crc = crc32(c0,self.crc)
        self.writebytes(c0)

    def writewordcrc(self,s):
        c1 = bytes([(s>>8)&0xFF])
        c0 = bytes([s&0xFF])
        self.crc = crc32(c1,self.crc)
        self.writebytes(c1)
        self.crc = crc32(c0,self.crc)
        self.writebytes(c0)

    def writebytecrc(self,c):
        c = bytes([c])
        self.crc = crc32(c,self.crc)
        self.writebytes(c)

    def writebuffercrc(self,bytes):
        self.crc = crc32(bytes,self.crc)
        self.writebytes(bytes)

    def beginchunk(self,name,len):
        self.writelong(len)
        self.resetcrc()
        self.crc = crc32(name,self.crc)
        self.writebytes(name)

    def endchunk(self):
        self.writelong(self.crc)

    def write_compressedchunk(self,name,data):
        cdata = self.compressor.compress(data) + self.compressor.flush()
        self.writelong(len(cdata))
        self.resetcrc()
        self.writebuffercrc(name)
        self.writebuffercrc(cdata)
        self.writelong(self.crc)


if __name__ == '__main__':
    w = 100
    h = 100
    cnv = PngCanvas(w, h, {"Foo123":"FooBar"})
    for i in range(w):
        for j in range(h):
            cnv.addpixel(i,j,255-i,j,255-j,255)
    cnv.write(open("test.png","wb"))