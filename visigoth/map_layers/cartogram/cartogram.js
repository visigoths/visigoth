//    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
//    Copyright (C) 2020  Niall McCarroll
//   Permission is hereby granted, free of charge, to any person obtaining a copy of this software
//   and associated documentation files (the "Software"), to deal in the Software without 
//   restriction, including without limitation the rights to use, copy, modify, merge, publish,
//   distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
//   Software is furnished to do so, subject to the following conditions:
//
//   The above copyright notice and this permission notice shall be included in all copies or 
//   substantial portions of the Software.
//
//   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
//   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
//   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
//   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

class cartogram {

    constructor(id,width,height,x,y,sendfn,config) {
        this.id = id;
        this.width = width;
        this.height = height;
        this.x = x;
        this.y = y;
        this.sendfn = sendfn;
        this.config = config;
        if (this.config["categories"]) {
            this.brushing_handler = new brushing_delegate(sendfn,this.config["categories"]);
        }
        for (var cid in this.config["links"]) {
            var elt = document.getElementById(cid);
            var link_id = this.config["links"][cid];
            elt.onmouseover = this.defineHoverCallback(link_id,true);
            elt.onmouseout = this.defineHoverCallback(link_id,false);
        }
    }

    defineHoverCallback(link_id,make_visible) {
        var that = this;
        var cb = function(evt) {
            var link = document.getElementById(link_id);
            if (make_visible) {
                link.setAttribute("visibility","visible");
            } else {
                link.setAttribute("visibility","hidden");
            }
        }
        return cb;
    }

    recieve(obj,channel) {
        if (this.brushing_handler) {
            this.brushing_handler.recieve(obj,channel);
        }
    }
}