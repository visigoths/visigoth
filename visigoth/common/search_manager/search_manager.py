# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
