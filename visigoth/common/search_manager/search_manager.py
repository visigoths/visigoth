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

import html

from visigoth.svg import foreign_object
from visigoth.common import DiagramElement, EmbeddedHtml

html_template = """
    <fieldset id="%(id)s"><legend>%(title)s</legend>
    <p>
        <input id="%(control_id)s" size="50" type="text"></input>
        <button id="%(control_id)s_search">Search</button>
    </p>
    </fieldset>
"""

js_template = """
document.getElementById("%(control_id)s_search").onclick = function(evt) {
    var value = document.getElementById("%(control_id)s").value;
    var payload = {"searchstring":value,"mode":"highlight"};
    pubsubs_publish("%(id)s",payload,"search");
};
"""

css = """
fieldset {
    border-width: 2px;
    border-radius: 5px;
}"""

class SearchManager(EmbeddedHtml):
    """
    Create an embedded HTML search manager

    Keyword Arguments:
        title: a title to display above the layer controls
        width(int): width of the embedded HTML
        height(int): height of the embedded HTML
    """

    def __init__(self,title="Search Controls",width=600,height=250):
        EmbeddedHtml.__init__(self,"%(content)s",css,width,height)
        control_id = DiagramElement.getNextId()
        html_content = html_template%({"id":self.getId(),"control_id":control_id,"title":title})
        js_content = js_template%({"id":self.getId(),"control_id":control_id,"title":title})
        self.setHtml(html_content)
        self.setJs(js_content)
