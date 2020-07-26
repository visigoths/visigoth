//    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

class panzoom {

    constructor(id,width,height,cx,cy,sendfn,config) {
        this.id = id;
        this.width = width;
        this.height = height;
        this.cx = cx;
        this.cy = cy;
        this.sendfn = sendfn;
        this.config = config;
        var that = this;
        this.zoom_index = this.config.initial_zoom;
        this.zoom_levels = this.config.zoom_levels;
        this.zoom_level = this.zoom_levels[this.zoom_index];

        this.setHandler("plus",function() { that.zoom(true); });
        this.setHandler("minus",function() { that.zoom(false); });
        this.setHandler("n");
        this.setHandler("s");
        this.setHandler("e");
        this.setHandler("w");

    }

    zoom(inNotOut) {
        if (inNotOut) {
            this.zoom_index += 1;
        } else {
            this.zoom_index -= 1;
        }
        if (this.zoom_index < 0) {
            this.zoom_index = 0;
        }
        if (this.zoom_index >= this.zoom_levels.length) {
            this.zoom_index = this.zoom_levels.length-1;
        }
        this.zoom_level = this.zoom_levels[this.zoom_index];
        for(var i=0; i<this.config.zoom_segments.length; i++) {
            var elt = document.getElementById(this.config.zoom_segments[i]);
            if (i <= this.zoom_index) {
                elt.setAttribute("fill",this.config.stroke);    
            } else {
                elt.setAttribute("fill",this.config.fill);
            }
        }
        this.sendfn(this.zoom_level,"zoom");
    }

    push(ele) {
        ele.setAttribute("fill","red");
        window.setTimeout(function() { ele.setAttribute("fill","white");},200);
    }

    setHandler(btn,cb) {
        var ele = document.getElementById(this.config[btn]);
        var that = this;
        var btn_ele = document.getElementById(this.config["btn_"+btn]);
        ele.onclick = function(event) { 
            if (cb) { 
                cb();
            } else { 
                that.sendfn(btn,"pan"); 
            }
            event.stopPropagation();
            that.push(btn_ele);
        };
        ele.onkeydown = function(evt) {
            evt.stopPropagation();
            if (evt.keyCode == 13) {
                if (cb) { 
                    cb();
                } else { 
                    that.sendfn(btn,"pan"); 
                }
                that.push(btn_ele);
            } 
        }
    }

    recieve(obj,channel) {
    }
}