//    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
//    Copyright (C) 2020  Niall McCarroll
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU Affero General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU Affero General Public License for more details.
//
//    You should have received a copy of the GNU Affero General Public License
//    along with this program.  If not, see <https://www.gnu.org/licenses/>.

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