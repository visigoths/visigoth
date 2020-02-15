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

class alternative {

    constructor(id,width,height,x,y,sendfn,config) {
        this.id = id;
        this.width = width;
        this.height = height;
        this.x = x;
        this.y = y;
        this.sendfn = sendfn;
        this.config = config;
        var that = this;
        if (this.config.group_ids.length>0) {
            this.display(this.config.group_ids[0]);
        }
    }

    display(show_id) {
        for(var idx=0; idx<this.config.group_ids.length; idx++) {
            var group_id = this.config.group_ids[idx];
            var elt = document.getElementById(group_id);
            if (group_id == show_id) {
                this.show(elt);
            } else {
                this.hide(elt);
            }
        }
    }


    hide(elt) {
        elt.setAttribute("visibility","hidden");
    }

    show(elt) {
        elt.removeAttribute("visibility");
    }

    recieve(obj,channel) {
        if (channel == "show") {
            this.display(obj);
        }
    }
}