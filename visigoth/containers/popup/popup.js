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