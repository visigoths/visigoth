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