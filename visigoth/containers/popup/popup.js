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

class popup {

    constructor(id,width,height,x,y,sendfn,config) {
        this.id = id;
        this.width = width;
        this.height = height;
        this.x = x;
        this.y = y;
        this.sendfn = sendfn;
        this.config = config;
        this.dragStartX = 0;
        this.dragStartY = 0;
        this.originX = 0;
        this.originY = 0;
        this.opened = false;
        var that = this;

        this.popup_group = document.getElementById(this.config["pgid"]);
        this.popup_group.onclick = function() {
            that.bringToFront();
        }
    }

    toggle() {
        this.opened = !this.opened;
        if (this.opened) {
            this.show();
        } else {
            this.hide();
        }
    }

    bringToFront() {
        var parent = this.popup_group.parentNode;
        parent.removeChild(this.popup_group);
        parent.appendChild(this.popup_group);
    }

    hide() {
        this.popup_group.setAttribute("visibility","hidden");
    }

    show() {
        this.popup_group.removeAttribute("visibility");
        this.bringToFront();
    }

    recieve(obj,channel) {
        if (obj == "close" && channel == "click") {
            // close button pressed
            this.hide();
            this.opened = false;
            return;
        }
        if (obj["target"] == this.id) {
            if (channel == "toggle") {
                this.toggle();
            }
        }
        if (channel == "show") {
            this.show();
            this.opened = true;
        }
        if (channel == "hide") {
            this.hide();
            this.opened = false;
        }
    }
}