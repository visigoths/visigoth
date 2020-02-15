//    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

class gridsquares {

    constructor(id,width,height,x,y,sendfn,config) {
        this.id = id;
        this.width = width;
        this.height = height;
        this.x = x;
        this.y = y;
        this.sendfn = sendfn;
        this.config = config;
        var that = this;
    }

    

    zoom(zoom_level) {
        var stroke_width = this.config.stroke_width;
        for(var idx in this.config.lines) {
            var lid = this.config.lines[idx];
            var line = document.getElementById(lid);
            line.setAttribute("stroke-width",stroke_width/zoom_level);
        }
        var font_height = this.config.font_height;
        for(var idx in this.config.labels) {
            var lid = this.config.labels[idx];
            var label = document.getElementById(lid);
            label.setAttribute("font-size",font_height/zoom_level);
        }
    }

    
    recieve(obj,channel) {
        if (channel == "zoom") {
            this.zoom(obj);
        }
    }
}