# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

import json
import os.path
import base64
import zipfile
import sqlite3
import tempfile

from visigoth.utils.httpcache import HttpCache

class FontManager(object):

    fonts = {}
    paths = {}

    default_font_name = ""
    default_font_weight = ""
    default_font_style = ""

    db_path = None
    inited = False

    fonts_dir = os.path.join(os.path.split(__file__)[0])

    @staticmethod
    def init():
        if FontManager.inited:
            return
        FontManager.inited = True
        FontManager.db_path = os.path.join(FontManager.fonts_dir,"font_dimensions.db")

    @staticmethod
    def loadFont(fontName):
        conn = sqlite3.connect(FontManager.db_path)
        details = [row for row in conn.execute("SELECT * FROM FONTS WHERE name=\"%s\""%(fontName.lower()))]
        for (name,weight,style,table_name,license) in details:
            key = FontManager.getFontKey(name,weight,style)
            glyph_widths = {}
            for glyph in conn.execute("SELECT * FROM %s"%(table_name)):
                (code,ratio) = glyph
                c = chr(int(code))
                r = float(ratio)
                glyph_widths[c] = r
            FontManager.fonts[key] = {"glyph_widths":glyph_widths,"weight":weight,"style":style}

    @staticmethod
    def setFontDefaults(name,weight,style):
        FontManager.default_font_name = name
        FontManager.default_font_weight = weight
        FontManager.default_font_style = style

    @staticmethod 
    def getFontKey(name,weight,style):
        return name.lower()+"-"+weight+"-"+style

    @staticmethod 
    def registerFont(name,weight,style,binary_path):
        key = FontManager.getFontKey(name,weight,style)
        FontManager.paths[key] = binary_path

    @staticmethod 
    def getTextLength(text_attributes,text,height):
        FontManager.init()
        name = text_attributes.get("font-family",FontManager.default_font_name)
        weight = text_attributes.get("font-weight",FontManager.default_font_weight)
        style = text_attributes.get("font-style",FontManager.default_font_style)
        FontManager.loadFont(name)
        key = FontManager.getFontKey(name,weight,style)
        if key in FontManager.fonts:
            font_meta = FontManager.fonts[key]
            total = 0.0
            for c in text:
                ratio = font_meta["glyph_widths"].get(c,1.0)
                total += height*ratio
            return total 
        else:
            # fallback, assume each char is square
            return len(text)*height

    @staticmethod
    def containsFont(family,weight,style):
        return FontManager.getFontKey(family,weight,style) in FontManager.fonts

    @staticmethod
    def registerFonts():
        for font in os.listdir(FontManager.fonts_dir):
            font_dir = os.path.join(FontManager.fonts_dir, font)
            if not os.path.isdir(font_dir):
                continue
            for font_file in os.listdir(font_dir):
                font_path = os.path.join(font_dir,font_file)
                path_root = os.path.splitext(font_path)[0]
                file_ext = os.path.splitext(font_path)[1]
                if file_ext == ".json":
                    binary_path = path_root + ".woff2"
                    with open(font_path,"r") as fontjson:
                        file_meta = json.loads(fontjson.read())
                        weight = file_meta["weight"]
                        style = file_meta["style"]
                        FontManager.registerFont(font,weight,style,binary_path)
                    
    @staticmethod
    def getCssFontFace(name,weight,style):
        conn = sqlite3.connect(FontManager.db_path)

        key = FontManager.getFontKey(name,weight,style)
        if key in FontManager.paths:
            path = FontManager.paths[key]
            mimetype = "font/woff2"
        else:
            details = [row for row in conn.execute("SELECT * FROM FONTS WHERE name=\"%s\" AND weight=\"%s\" AND style=\"%s\""%(name.lower(),weight,style))]
            for (_,weight,style,_,license) in details:
                filename = name
                if weight == "normal" and style == "italic":
                    filename += "-Italic.ttf"
                elif weight == "bold" and style == "normal":
                    filename += "-Bold.ttf"
                elif weight == "bold" and style == "italic":
                    filename += "-BoldItalic.ttf"
                else:
                    filename += "-Regular.ttf"
                url = "https://github.com/google/fonts/blob/master/%s/%s/static/%s?raw=true"%(license,name.lower(),filename)
                # url = "https://raw.githubusercontent.com/google/fonts/master/%s/%s/%s"%(license,name.lower(),filename)
                path=HttpCache.fetch(url,returnPath=True)
                mimetype = "font/ttf"

        with open(path,"r+b") as fontfile:
                uri="data:"+mimetype+";charset=US-ASCII;base64,"+str(base64.b64encode(fontfile.read()),"utf-8")
                return """
                @font-face {
                        font-family: '%s';
                        font-weight: %s;
                        font-style: %s;
                        src: url('%s');
                }"""%(name,weight,style,uri)

    @staticmethod
    def getCssFontImport(name):
        return "@import url('https://fonts.googleapis.com/css?family=%s')"%(name)
    