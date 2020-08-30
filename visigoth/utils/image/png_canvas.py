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

from zlib import adler32, crc32
from math import log

class PngCanvas(object):
    
    def __init__(self,height,width,palette):
        self.height = height
        self.width = width
        self.bits = 8
        self.data = [0 for i in range(0,width*height)]
        self.group_bytes=int(self.width / (8 / self.bits) + 1)
        self.colors=(1 << self.bits)
        self.crc = 0
        self.init_palette(palette)
        self.png_magic = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"

    def init_palette(self,palette):
        self.plt = []
        self.trns = []
        for (r,g,b,t) in palette:
            self.plt.append((r<<16)|(g<<8)|b)
            self.trns.append(t)
        for p in range(0,256-len(palette)):
            self.plt.append(0)
            self.trns.append(255)
    
    def addpixel(self,x,y,col):
        """Add a pixel with a colour index to the canvas, coordinate system is left-right (x) and top-bottom (y)"""
        self.data[x+(y*self.width)] = col
        
    def pixel(self,x,y):
        return self.data[x+(y*self.width)]
        
    def write(self,file):

        i = 0
        j = 0
        k = 0
        zcrc = 0
        zero = 0xF1
        filter = 0
    
        self.fd = file

        self.resetcrc()
    
        self.fd.write(self.png_magic)
    
        self.beginchunk(b"IHDR", 0x0d)
        self.writelongcrc(self.width)	    # width 
        self.writelongcrc(self.height)       # height 
        self.writebytecrc(self.bits)	    # bit depth 
        self.writebytecrc(3)	    # color type 
        self.writebytecrc(0)	    # compression 
        self.writebytecrc(0) 	    # filter 
        self.writebytecrc(0)	    # interlace 
        self.endchunk()
    
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

        self.beginchunk(b"IDAT", (self.height * (self.group_bytes + 4 + 1)) + 4 + 2)
        self.writewordcrc(((0x0800 + 30) // 31) * 31 )	# compression method 
    
        zcrc = 1
        i = 0
        while i < self.height:
            if i == (self.height-1):    
                self.writebytecrc(0x01) 
            else:
                self.writebytecrc(0)
            self.Xwritewordcrc(self.group_bytes)
            self.Xwritewordcrc(~self.group_bytes)
         
            # write PNG row filter - 0 = unfiltered 
            zcrc = adler32(bytes([filter]),zcrc)
            self.writebytecrc(filter)
            
            k = 0
            while k < self.width:
                c = self.pixel(k,i)
                zcrc = adler32(bytes([c]),zcrc)
                self.writebytecrc(c)
                k += 1
                
            i += 1
    
        self.writelongcrc(zcrc)
        # print "zcrc = " + str(zcrc)
    
        self.endchunk()
    
        self.beginchunk(b"IEND", 0)
        self.endchunk()
    
    def resetcrc(self):
        self.crc = 0
    
    def writelong(self,l):
        self.fd.write(bytes([(l>>24)&0xFF,(l>>16)&0xFF,(l>>8)&0xFF,l&0xFF]))
        
    def writelongcrc(self,l):
        c3 = bytes([(l>>24)&0xFF])
        c2 = bytes([(l>>16)&0xFF])
        c1 = bytes([(l>>8)&0xFF])
        c0 = bytes([l&0xFF])
        
        self.crc = crc32(c3,self.crc)
        self.fd.write(c3)
        self.crc = crc32(c2,self.crc)
        self.fd.write(c2)
        self.crc = crc32(c1,self.crc)
        self.fd.write(c1)
        self.crc = crc32(c0,self.crc)
        self.fd.write(c0)
    
    
    def Xwritelongcrc(self,l):
        c3 = bytes([(l>>24)&0xFF])
        c2 = bytes([(l>>16)&0xFF])
        c1 = bytes([(l>>8)&0xFF])
        c0 = bytes([l&0xFF])
        
        self.crc = crc32(c0,self.crc)
        self.fd.write(c0)
        self.crc = crc32(c1,self.crc)
        self.fd.write(c1)
        self.crc = crc32(c2,self.crc)
        self.fd.write(c2)
        self.crc = crc32(c3,self.crc)
        self.fd.write(c3)
    
    
    
    def writewordcrc(self,s):
    
        c1 = bytes([(s>>8)&0xFF])
        c0 = bytes([s&0xFF])
       
        self.crc = crc32(c1,self.crc)
        self.fd.write(c1)
        self.crc = crc32(c0,self.crc)
        self.fd.write(c0)
    
    def Xwritewordcrc(self,s):
     
        c1 = bytes([(s>>8)&0xFF])
        c0 = bytes([s&0xFF])
       
        self.crc = crc32(c0,self.crc)
        self.fd.write(c0)
        self.crc = crc32(c1,self.crc)
        self.fd.write(c1)
    
    def writebytecrc(self,c):
        c = bytes([c])
        self.crc = crc32(c,self.crc)
        self.fd.write(c)
    
    
    def beginchunk(self,name,len):
            
        self.writelong(len)
        self.resetcrc()
        self.crc = crc32(name,self.crc)
        self.fd.write(name)

    def endchunk(self):
        self.writelong(self.crc)

if __name__ == '__main__':
    cnv = PngCanvas(1, 1, [(255,255,255,0)])
    cnv.addpixel(0,0,0)
    from io import BytesIO
    bio = BytesIO()
    cnv.write(bio)
    print(bio.getvalue())