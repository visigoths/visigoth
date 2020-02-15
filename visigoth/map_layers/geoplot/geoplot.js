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

class geoplot {

    constructor(id,width,height,x,y,sendfn,config) {
        this.id = id;
        this.width = width;
        this.height = height;
        this.x = x;
        this.y = y;
        this.sendfn = sendfn;
        this.config = config;
        var that = this;
        for(var trigger in this.config.popup_map) {
            var elt = document.getElementById(trigger);
            var cb = this.defineCallback(trigger);
            elt.addEventListener("click",cb);
            elt.onkeydown = function(evt) {
                if (evt.keyCode == 13) {
                    cb(evt);
                    return false;
                } else {
                    return true;
                }
            }
        }

        for(var item_group_id in this.config.group_labels) {
            var elt = document.getElementById(item_group_id);
            var label = this.config.group_labels[item_group_id];
            var cb = this.defineLabelCallback(label);
            elt.addEventListener("click",cb);
        }

        this.defineEventSources(this.config.polygons);
        this.defineEventSources(this.config.lines);
        this.defineEventSources(this.config.points);
    }

    defineCallback(trigger) {
        var that = this;

        var cb = function(evt) {
            var dest = that.config.popup_map[trigger];
            var x = evt.pageX;
            var y = evt.pageY;
            if (evt.keyCode==13) {
                x = that.x;
                y = that.y;
            }
            var payload = {"target":dest,"action":"toggle","x":x,"y":y};
            that.sendfn(payload);
        }
        return cb;
    }

    zoom(zoom_level) {
        for (var cid in this.config.circles) {
            var radius = this.config.circles[cid].r;
            var sw = this.config.circles[cid].sw;
            document.getElementById(cid).setAttribute("r",radius/zoom_level);
            document.getElementById(cid).setAttribute("stroke-width",sw/zoom_level);
        }
        for (var mid in this.config.markers) {
            var x = this.config.markers[mid].x;
            var y = this.config.markers[mid].y;
            var scale = 1/zoom_level;
            var tx = -1*x*(scale-1);
            var ty = -1*y*(scale-1);
            var transform = "translate("+tx+","+ty+") scale("+scale+")";
            document.getElementById(mid).setAttribute("transform",transform);
        }
        for (var lid in this.config.lines) {
            var sw = this.config.lines[lid].sw;
            document.getElementById(lid).setAttribute("stroke-width",sw/zoom_level);
        }
        for (var pid in this.config.polygons) {
            var sw = this.config.polygons[pid].sw;
            var elt = document.getElementById(pid);
            elt.setAttribute("stroke-width",sw/zoom_level);
        }
        for (var lid in this.config.labels) {
            var x = this.config.labels[lid].x;
            var y = this.config.labels[lid].y;
            var tx = -1*(x)*(1/zoom_level-1);
            var ty = -1*(y)*(1/zoom_level-1);
            var transform = "translate("+tx+","+ty+") scale("+1/zoom_level+")";
            document.getElementById(lid).setAttribute("transform",transform);
        }
        for (var pid in this.config.popups) {
            var x = this.config.popups[pid].x;
            var y = this.config.popups[pid].y;
            var tx = -1*(x)*(1/zoom_level-1);
            var ty = -1*(y)*(1/zoom_level-1);
            var transform = "translate("+tx+","+ty+") scale("+1/zoom_level+")";
            document.getElementById(pid).setAttribute("transform",transform);
        }
    }

    defineEventSources(source_map) {
        for (var eid in source_map) {
            var id = source_map[eid].id;
            var category = source_map[eid].category;
            var elt = document.getElementById(eid);
            if (id) {
                this.registerEventSource(elt,id,"select_id");
            }
            if (category) {
                this.defineEventSourceCallback(elt,category,"select_category");
            }
        }
    }
    registerEventSource(elt,value,channel) {
        var cb = this.defineEventSourceCallback(value,channel);
        elt.addEventListener("click",cb);
    }

    defineEventSourceCallback(value,channel) {
        var that = this;
        return function() {
            that.sendfn(value,channel);
        }
    }

    updateVisibleWindow(obj) {
        var xmin = obj.cx - obj.width/2;
        var xmax = obj.cx + obj.width/2;
        var ymin = obj.cy - obj.height/2;
        var ymax = obj.cy + obj.height/2;
        for (var pid in this.config.popups) {
            var x = this.config.popups[pid].x;
            var y = this.config.popups[pid].y;
            var elt = document.getElementById(pid);
            if (x < xmin || x > xmax || y < ymin || y > ymax) {
                elt.setAttribute("visibility","hidden");
            } else {
                elt.removeAttribute("visibility");
            }
        }
    }

    defineLabelCallback(label) {
        var that = this;
        var cb = function(evt) {
            that.sendfn(label,"select");
        }
        return cb;
    }

    showOrHideLabels(showNotHide) {
        for(var idx=0; idx<this.config.label_ids.length;idx++) {
            var label_id = this.config.label_ids[idx];
            var label_elt = document.getElementById(label_id);
            if (label_elt) {
                if (showNotHide) {
                    label_elt.removeAttribute("visibility");
                } else {
                    label_elt.setAttribute("visibility","hidden");
                }
            }
        }
    }

    showAll() {
        for(var group_id in this.config.group_properties) {
            var g = document.getElementById(group_id);
            g.removeAttribute("visibility");
        }
    }

    highlight(g,highlighted) {
        if (highlighted) {
            var cls = g.getAttribute("class");
            if (cls) {
                if (cls.indexOf("highlight")==-1) {
                    cls += " highlight";
                }
            } else {
                cls = "highlight";
            }
            g.setAttribute("class",cls);
        } else {
            var cls = g.getAttribute("class");
            
            cls = cls.replace("highlight","");
            g.setAttribute("class",cls);
        }
    }

    recieve(obj,channel) {
        if (channel == "zoom") {
            this.zoom(obj);
        }
        if (channel == "visible_window") {
            this.updateVisibleWindow(obj);
        }
        if (channel == "show_labels") {
            this.showOrHideLabels(obj);
        }
        if (channel == "highlight") {
            this.showAll();
        }
        if (channel == "filter" || channel == "highlight") {
            var search_string = obj.toLowerCase();
            for(var group_id in this.config.group_properties) {
                var g = document.getElementById(group_id);
                var match = false;
                if (search_string == "") {
                    match = (channel == "filter");
                } else {
                    var props = this.config.group_properties[group_id];
                    if (props) {
                        for(var key in props) {
                            var val = String(props[key]).toLowerCase();
                            if (val.indexOf(search_string)>-1) {
                                match = true;
                                break;
                            }
                        }
                    }
                }
                if (match) {
                    if (channel == "filter") {
                        g.removeAttribute("visibility");
                    } else {
                        this.highlight(g,true);
                    }
                } else {
                    if (channel == "filter") {
                        g.setAttribute("visibility","hidden");
                    } else {
                        this.highlight(g,false);
                    }
                }
            }
        }
    }
}