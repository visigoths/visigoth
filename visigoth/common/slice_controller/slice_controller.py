# -*- coding: utf-8 -*-

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

from visigoth.common import DiagramElement, EmbeddedHtml
import json

html_template = """
    <fieldset id="%(id)s"><legend>%(title)s</legend>
    <p>
        <input type="range" id="%(control_id)s_slider" min="0" max="11" style="width:200px;">
        <input id="%(control_id)s_value" size="50" type="text" readonly style="width:200px;"></input>
        <button id="%(control_id)s_backwards">&lt;</button>
        <button id="%(control_id)s_forwards">&gt;</button>
    </p>
    </fieldset>
"""

js_template = """

class SliceManager {
    constructor() {
        this.index = 0;
        this.values = %(values)s;
        this.value_ele = document.getElementById("%(control_id)s_value");
        this.slider_ele = document.getElementById("%(control_id)s_slider");
        this.slider_ele.setAttribute("max",this.values.length-1);
        this.updateValue();
    }
    
    forwards() {
        if (this.index < this.values.length-1) {
            this.index += 1;
            this.updateValue();
            this.emit();
        }
    }
    
    backwards() {
        if (this.index > 0) {
            this.index -= 1;
            this.updateValue();
            this.emit();
        }
    }
    
    jump(index) {
        this.index = Number.parseInt(index);
        this.updateValue();
        this.emit();
    }
    
    emit() {
        pubsubs_publish("%(id)s",this.values[this.index],"slice");
    }
    
    updateValue() {
        this.value_ele.value = this.values[this.index];
        this.slider_ele.value = this.index;
    }
}

var %(control_id)s = new SliceManager();

document.getElementById("%(control_id)s_forwards").onclick = function(evt) {
    %(control_id)s.forwards();
};

document.getElementById("%(control_id)s_backwards").onclick = function(evt) {
    %(control_id)s.backwards();
};

document.getElementById("%(control_id)s_slider").onchange = function(evt) {
    %(control_id)s.jump(document.getElementById("%(control_id)s_slider").value);
};
"""

css = """
fieldset {
    border-width: 2px;
    border-radius: 5px;
}"""

class SliceController(EmbeddedHtml):
    """
    Create an embedded HTML slice manager

    Keyword Arguments:
        title: a title to display above the slice controls
        width(int): width of the embedded HTML
        height(int): height of the embedded HTML
    """

    def __init__(self,title="Slice Controls",width=512,height=100):
        EmbeddedHtml.__init__(self,"%(content)s",css,width,height)
        self.control_id = DiagramElement.getNextId()
        self.title = title
        html_content = html_template%({"id":self.getId(),"control_id":self.control_id,"title":title})
        js_content = js_template%({"id":self.getId(),"control_id":self.control_id,"title":title,"values":json.dumps([])})
        self.setHtml(html_content)
        self.setJs(js_content)

    def handleConnectTo(self,channel_out,dest):
        if channel_out == "slice":
            slices = dest.getSlices()
            js_content = js_template % ({"id": self.getId(), "control_id": self.control_id, "title": self.title, "values": json.dumps(slices)})
            self.setJs(js_content)
