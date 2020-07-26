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