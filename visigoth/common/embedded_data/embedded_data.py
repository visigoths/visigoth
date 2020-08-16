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
import base64
import csv
from io import StringIO, BytesIO
import zipfile
import os

from visigoth.common.diagram_element import DiagramElement
from visigoth.utils.fonts.fontmanager import FontManager
from visigoth.svg import text

from visigoth.utils.data.dataset import Dataset

class EmbeddedData(DiagramElement):
    """
    Create an embedded data link

    Arguments:
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)

     Keyword Arguments:
        text: the text to display in the link
        filename(str): the name of the file to which the download should be saved.  Note that the browser may not honour this.
        columns(list): list of column names / indexes identifying the columns in the data to export (export all if None)
        column_labels(dict): a mapping from column to the CSV header (use column name / index if no mapping)
        zip(bool): whether to put the CSV into a zip file, helping to keep the HTML size down
        font_height(int): the font size for the legend (optional, defaults to 24)
        text_attributes(dict): a dict containing SVG name/value pairs to apply to table body text
        hint(str): a hint to display to instruct the user to right click on the link and select save link as
    """

    def __init__(self,data,text="Download",filename=None,columns=None,column_labels={},zip=True,
                 font_height=24,text_attributes={},hint="(Right Click + Save Link As...)"):
        DiagramElement.__init__(self)
        self.dataset = Dataset(data)
        self.columns = columns if columns else self.dataset.getColumns()
        self.text = text
        self.text_attributes = text_attributes
        self.font_height = font_height
        self.width = 0
        self.height = 0
        self.column_labels = column_labels
        if filename:
            self.filename = filename
        else:
            self.filename = "data.csv"
        self.zip = zip
        self.hint = hint
        self.hint_font_height = self.font_height * 0.7
        self.hint_spacing = self.font_height

    def build(self,fmt):
        if fmt != "html":
            self.width = 0
            self.height = 0
            return
        self.width = FontManager.getTextLength(self.text_attributes, self.text, self.font_height)
        if self.hint:
            self.width += self.hint_spacing
            self.width += FontManager.getTextLength(self.text_attributes, self.hint, self.hint_font_height)
        self.height = self.font_height

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def draw(self,d,cx,cy):
        if d.getFormat() != "html":
            return
        ox = cx - self.width/2
        f = StringIO()
        writer = csv.writer(f,lineterminator='\n',)
        header_row = [self.column_labels.get(col,col) for col in self.columns]
        writer.writerows([header_row]+self.dataset.query(self.columns))
        csvtxt = f.getvalue()
        if not self.zip:
            binary_content = csvtxt.encode("utf-8")
            filename = self.filename
            mime_type = "text/csv"
        else:
            zf = BytesIO()
            zip = zipfile.ZipFile(zf,mode="w",compression=zipfile.ZIP_DEFLATED,compresslevel=9)
            zip.writestr(self.filename,csvtxt)
            zip.close()
            binary_content = zf.getvalue()
            filename = os.path.splitext(self.filename)[0]+".zip"
            mime_type = "application/zip"
        url = "data:"+mime_type+";base64,"+base64.b64encode(binary_content).decode("utf-8")
        width1 = FontManager.getTextLength(self.text_attributes, self.text, self.font_height)
        ts = text(ox+width1/2, cy, self.text, font_height=self.font_height, text_attributes=self.text_attributes)
        ts.setVerticalCenter()
        ts.setUrl(url,download=filename)
        d.add(ts)
        if self.hint:
            width2 = FontManager.getTextLength(self.text_attributes, self.hint, self.hint_font_height)
            ts2 = text(ox + width1 + self.hint_spacing + width2 / 2, cy, self.hint, font_height=self.hint_font_height,
                      text_attributes=self.text_attributes)
            ts2.setVerticalCenter()
            d.add(ts2)