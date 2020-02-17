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


template = """
    <fieldset id="%(id)s"><legend>%(title)s</legend>
    <p>
        <input id="%(control_id)s" type="text"></input>
        <label for="%(control_id)s">Search String</label>
        <button id="%(control_id)s_search">Search</button>
        <input type="radio" id="%(control_id)s_filter" name="%(control_id)s_search_type" value="filter" checked="checked"></input>
        <label for="%(control_id)s_filter">Filter</label>
        <input type="radio" id="%(control_id)s_highlight" name="%(control_id)s_search_type" value="highlight"></input>
        <label for="%(control_id)s_highlight">Highlight</label>
    </p>
    </fieldset>
    <script>
    <![CDATA[
          document.getElementById("%(control_id)s_search").onclick = function(evt) {
              var value = document.getElementById("%(control_id)s").value;
              var mode = "filter";
              if (document.getElementById("%(control_id)s_highlight").checked) {
                mode = "highlight";
              }
              var payload = {"searchstring":value,"mode":mode};
              alert(JSON.stringify(payload));
              pubsubs_publish("%(id)s",payload,"search");
          };
    ]]>
    </script>
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

    def __init__(self,title="Search Controls",width=600,height=150):
        EmbeddedHtml.__init__(self,"%(content)s",css,width,height)
        control_id = DiagramElement.getNextId()
        html_content = template%({"id":self.getId(),"control_id":control_id,"title":title})
        print(html_content)
        self.substituteHtml({"content":html_content})
