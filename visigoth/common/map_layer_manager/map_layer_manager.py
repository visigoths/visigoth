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

import html

from visigoth.svg import foreign_object
from visigoth.common import DiagramElement, EmbeddedHtml

start = """<fieldset id="%(id)s"><legend>%(title)s</legend>"""

control_template = """
    <p>
        <input id="%(control_id)s" type="checkbox"></input>
        <label for="%(control_id)s">%(control_label)s</label>
    </p>
"""

js_template = """
document.getElementById("%(control_id)s").checked = %(visible)s;
document.getElementById("%(control_id)s").onclick = function(evt) {
    pubsubs_publish("%(id)s",{"layer":"%(layer_id)s","value":evt.target.checked},"manage_layers");
};
"""

end = """</fieldset>"""

css = """
fieldset {
    border-width: 2px;
    border-radius: 5px;
}"""

class MapLayerManager(EmbeddedHtml):
    """
    Create an embedded HTML map layer manager

    Arguments:
        layers(list): list of dicts containg "label" and "id" keys

    Keyword Arguments:
        title: a title to display above the layer controls
        width(int): width of the embedded HTML
        height(int): height of the embedded HTML
    """

    def __init__(self,map_layers,title="Layer Controls",width=512,height=512):
        EmbeddedHtml.__init__(self,"",css,width,height)
        html_content = start%({"id":self.getId(),"title":html.escape(title,True)})
        js_content = ""
        for map_layer in map_layers:
            control_label = map_layer["label"]
            layer_obj = map_layer["layer"]
            layer_id = layer_obj.getId()
            visible = "false"
            if layer_obj.getVisible():
                visible = "true"
            control_id = DiagramElement.getNextId()
            html_content += control_template%({
                "id":self.getId(),
                "control_label":control_label,
                "control_id":control_id,
                "visible":visible,
                "layer_id":layer_id})
            js_content += js_template%({
                "id":self.getId(),
                "control_label":control_label,
                "control_id":control_id,
                "visible":visible,
                "layer_id":layer_id})

        html_content += end
        self.setHtml(html_content)
        self.setJs(js_content)
