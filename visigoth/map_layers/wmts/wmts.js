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

class wmts {

    constructor(id,width,height,x,y,sendfn,config) {
        this.id = id;
        this.width = width;
        this.height = height;
        this.x = x;
        this.y = y;
        this.sendfn = sendfn;
        this.config = config;
        this.zoom_level = 1;
        this.loaded_images = {};
    }

    zoom(zoom_level,cx,cy,width,height) {
        var low_x = cx - width/2;
        var high_x = cx + width/2;
        var low_y = cy - height/2;
        var high_y = cy + height/2;
        var target_index = Math.floor(Math.log2(zoom_level));

        for(var i=0; i<this.config.zoom_groups.length; i++) {
            var elt = document.getElementById(this.config.zoom_groups[i]);
            if (i == target_index) {
                elt.removeAttribute("visibility");
                if (this.config["image_urls_by_zoom"]) {
                    var level_key = Math.pow(2,target_index)+"";
                    var image_urls = this.config["image_urls_by_zoom"][level_key];
                    var zoom_level = this.config["zoom_levels"][level_key];
                    var scale = zoom_level["scale"];
                    var offset_x = zoom_level["offset_x"];
                    var offset_y = zoom_level["offset_y"];

                    if (image_urls) {
                        for(var image_id in image_urls) {
                            var image_ele = document.getElementById(image_id);
                            if (image_ele) {
                                var ix = Number.parseFloat(image_ele.getAttribute("x"));
                                var iy = Number.parseFloat(image_ele.getAttribute("y"));
                                var iwidth = Number.parseFloat(image_ele.getAttribute("width"));
                                var iheight = Number.parseFloat(image_ele.getAttribute("height"));

                                ix = ix*scale+offset_x;
                                iy = iy*scale+offset_y;
                                iwidth *= scale;
                                iheight *= scale;

                                if ((iy > high_y) || ((iy+iheight) < low_y) || (ix > high_x) || ((ix+iwidth) < low_x)) {
                                    // this tile is not currently visible so can be skipped
                                } else {
                                    if (this.loaded_images[image_id]) {
                                    } else {
                                        // console.log("loading");
                                        image_ele.setAttribute("href",image_urls[image_id]);
                                        this.loaded_images[image_id] = true;
                                    }
                                }
                            }
                        }
                    }
                }
            } else {
                elt.setAttribute("visibility","hidden");
            }
        }
    }

    recieve(obj,channel) {
        if (channel == "zoom") {
            this.zoom_level = obj; // store the zoom level, a subsequent visible_window event will trigger the zoom
        }
        if (channel == "visible_window") {
            console.log("zoom: cx="+obj["cx"]+", cy="+obj["cy"]+", w="+obj["width"]+",h="+obj["height"]+",z="+this.zoom_level);
            this.zoom(this.zoom_level,obj["cx"],obj["cy"],obj["width"],obj["height"]);
        }
        // console.log("WMTS got:"+channel+":"+JSON.stringify(obj));
    }
}