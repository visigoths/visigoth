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

class button {

    constructor(id,width,height,x,y,sendfn,config) {
        this.id = id;
        this.width = width;
        this.height = height;
        this.x = x;
        this.y = y;
        this.sendfn = sendfn;
        this.config = config;
        var that = this;
        this.rect =  document.getElementById(this.id);
        this.rect.onclick = function() {
            that.press();
        }

        this.rect.onkeydown = function(evt) {
            if (evt.keyCode == 13) {
                that.press();
                return false;
            } else {
                return true;
            }
        }
        this.highlighted = this.config["initially_selected"];
        this.update();
    }

    update() {
        var button_border = document.getElementById(this.config["rectangle"]);
        var push_colour = this.config["push_fill"];
        var normal_colour = this.config["fill"];

        if (this.highlighted) {
            button_border.setAttribute("fill",push_colour);
        } else {
            button_border.setAttribute("fill",normal_colour);
        }
    }

    press() {
        this.highlighted = true;
        this.update();
        this.highlighted = false;
        var that = this;
        window.setTimeout(function() { that.update(); },200);
        this.sendfn(this.config["click_value"],"click");
        this.sendfn("select","ch"+this.id);
    }

    recieve(obj,channel) {
        // alert("b:channel="+channel+":obj="+obj);
        if (obj == "select") {
            this.highlighted = true;
            this.update();
        }
        if (obj == "deselect") {
            this.highlighted = false;
            this.update();
        }
    }
}