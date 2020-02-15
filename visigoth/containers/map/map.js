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

class map {

    constructor(id,width,height,cx,cy,sendfn,config) {
        this.id = id;
        this.width = width;
        this.height = height;
        this.cx = cx;
        this.cy = cy;
        this.sendfn = sendfn;
        this.config = config;
        this.layerGroup = document.getElementById(this.config.layerGroupId);
        this.popGroup = document.getElementById(this.config.popGroupId);
        this.overlay = this.config.overlayId ? document.getElementById(this.config.overlayId) : null;
        this.zoom_level = 1;
        this.offset_x = 0;
        this.offset_y = 0;
        var that = this;
        if (this.overlay) {
            this.overlay.addEventListener("mousedown", function(event) {
                event.preventDefault();
                that.dragStart(event);
            });

            this.overlay.addEventListener("mouseup", function(event) {
                event.preventDefault();
                that.dragEnd(event);
            });

            this.overlay.addEventListener("touchstart", function(event) { event.preventDefault();
                event.clientX = event.touches[0].clientX;
                event.clientY = event.touches[0].clientY;
                that.dragStart(event);
            }, {"passive":false,"capture":true});

            this.overlay.addEventListener("touchmove", function(event) {
                event.preventDefault();
                event.clientX = event.touches[0].clientX;
                event.clientY = event.touches[0].clientY;
                that.dragMove(event);
            }, {"passive":false,"capture":true});

            this.overlay.addEventListener("touchend", function(event) {
                event.preventDefault();
                that.dragEnd(event);
            }, {"passive":false,"capture":true});
        }

        this.drag_x = 0;
        this.drag_y = 0;
    }

    dragEnd(event) {
        this.overlay.onmousemove = function() {};
        this.overlay.ontouchmove = function() {};
    }

    dragStart(event) {
        this.drag_x = event.clientX;
        this.drag_y = event.clientY;
        var that = this;
        this.overlay.onmousemove = function(event) { event.preventDefault();  that.dragMove(event); event.stopPropagation(); }
    }

    dragMove(event) {
        var dx = event.clientX - this.drag_x;
        var dy = event.clientY - this.drag_y;
        this.move(dx,dy);
        this.drag_x = event.clientX;
        this.drag_y = event.clientY;
    }

    sendVisibleWindowUpdate() {
        var cx = this.cx+this.offset_x/this.zoom_level;
        var cy = this.cy+this.offset_y/this.zoom_level;
        var width = this.width/this.zoom_level;
        var height = this.height/this.zoom_level;
        this.sendfn({"cx":cx, "cy":cy, "width":width, "height":height},"visible_window");
    }

    move(dx,dy) {
        this.offset_x -= (dx / (this.zoom_level-1));
        this.offset_y -= (dy / (this.zoom_level-1));

        this.updateTransform();
        this.sendVisibleWindowUpdate();
    }

    zoom(newzoom) {
        if (newzoom >= 1 && newzoom <= this.config.max_zoom) {
            this.offset_x *= this.zoom_level/newzoom;
            this.offset_y *= this.zoom_level/newzoom;
            this.zoom_level = newzoom;    
            this.updateTransform();
            this.sendfn(this.zoom_level,"zoom");
            this.sendVisibleWindowUpdate();
        }
    }

    updateTransform() {
        if (this.zoom_level == 1) {
            this.offset_x = 0;
            this.offset_y = 0;
        }

        var frac = 0.5;
        var minx = -1*this.width*frac;
        // console.log("minx:"+minx);
        if (this.offset_x < minx) {
            this.offset_x = minx
        }
        
        var maxx = this.width*frac;
        if (this.offset_x > maxx) {
            this.offset_x = maxx
        }

        var miny = -1*this.height*frac
        if (this.offset_y < miny) {
            this.offset_y = miny;
        }
        
        var maxy = this.height*frac;
        if (this.offset_y > maxy) {
            this.offset_y = maxy;
        }

        // console.log("width:"+this.width+",zoom:"+this.zoom_level+",offsets:"+this.offset_x+","+this.offset_y);

        var tx = -1*(this.cx+this.offset_x)*(this.zoom_level-1);
        var ty = -1*(this.cy+this.offset_y)*(this.zoom_level-1);
        var transform = "translate("+tx+","+ty+") scale("+this.zoom_level+")";
        this.layerGroup.setAttribute("transform",transform);
        this.popGroup.setAttribute("transform",transform);
    }

    recieve(obj,channel) {
        if (channel == "pan") {
            if (obj == "e") {
                this.move(-20,0);
            }
            if (obj == "w") {
                this.move(20,0);
            }
            if (obj == "n") {
                this.move(0,20);
            }
            if (obj == "s") {
                this.move(0,-20);
            }
            return;
        }
        if (channel == "zoom") {
            this.zoom(obj);
            return;
        }
        if (channel == "manage_layers") {
            var layer = obj["layer"];
            var value = obj["value"];
            if (typeof(value) == "number") {
                document.getElementById(layer).setAttribute("opacity",value);
            } else {
                var opacity = 0.0;
                if (value) {
                    opacity = this.config.opacities[layer];
                }
                document.getElementById(layer).setAttribute("opacity",opacity);
            }
        }
    }
}