//    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
//    Copyright (C) 2020  Niall McCarroll
//
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

class super_delegate {

    constructor(sendfn,id) {
        this.sendfn = sendfn;
        this.id;
    }

    recieve(obj,channel) {
        if (channel == "visibility") {
            var visible = obj;
            if (visible) {
                document.getElementById(this.id).setAttribute("visibility","visible");
            } else {
                document.getElementById(this.id).setAttribute("visibility","hidden");
            }

            this.sendfn(visible,"visibility");
        }
    }
}


class slicing_delegate {

    constructor(sendfn,start_slice,slices) {
        this.current_slice = start_slice;
        this.sendfn = sendfn;
        this.slices = slices;
    }

    setVisibility(slice,visibility) {
        slice = ""+slice;
        if (this.slices[slice]) {
            var ids = this.slices[slice];
            for(var idx=0; idx<ids.length;idx++) {
                var ele = document.getElementById(ids[idx]);
                ele.setAttribute("visibility",visibility);
            }
        } else {
            console.log("Unable to find slice: "+slice);
        }
    }

    recieve(slice) {
        this.setVisibility(this.current_slice,"hidden");
        this.setVisibility(slice,"visible");
        this.current_slice = slice;
    }
}

class brushing_delegate {

    constructor(sendfn,categories) {
        this.sendfn = sendfn;
        this.categories = categories;
        var that = this;
        this.highlights = {};
        this.original_classes = {};

        if (this.categories) {
            for (var category in this.categories) {
                var cb = this.createBrushingCB(category);
                var ids = this.categories[category];
                for(var idx in ids) {
                    try {
                        document.getElementById(ids[idx]).onclick = cb;
                    } catch(e) {
                        alert(ids[idx]);
                    }
                }
            }
        }
    }

    createBrushingCB(category) {
        var that = this;
        var cb = function(evt) {
            var ids = that.categories[category];
            for(var idx in ids) {
                var id = ids[idx];
                var ele = document.getElementById(id);
                if (that.highlights[id]) {
                    ele.setAttribute("class",that.original_classes[id]);
                    delete that.highlights[id];
                    delete that.original_classes[id];
                } else {
                    var cls = ele.getAttribute("class");
                    that.highlights[id] = true;
                    that.original_classes[id] = cls;
                    ele.setAttribute("class",cls+" highlight");
                }
            }
            var payload = {"action":"brush","category":category};
            that.sendfn(payload);
        }
        return cb;
    }

    recieve(obj,channel) {
        var action = obj["action"];
        if (action == "brush") {
            var category = obj["category"];
            var ids = this.categories[category];
            if (ids) {
                for(var idx in ids) {
                    var id = ids[idx];
                    var ele = document.getElementById(id);
                    if (this.highlights[id]) {
                        var cls = this.original_classes[id];
                        ele.setAttribute("class",cls);
                        delete this.original_classes[id];
                        delete this.highlights[id];
                    } else {
                        var cls = ele.getAttribute("class");
                        this.original_classes[id] = cls;
                        this.highlights[id] = true;
                        ele.setAttribute("class",cls+" highlight");
                    }
                }
            }
        }
    }
}

var pubsubs = {};

function pubsubs_subscribe(target,channel,callback) {
    if (!pubsubs[target]) {
        pubsubs[target] = [];
    }
    pubsubs[target].push({"callback":callback,"channel":channel});
}

function pubsubs_publish(source,value,channel) {
    if (pubsubs[source]) {
        var subs = pubsubs[source];
        for(var i=0;i<subs.length;i++) {
            if (!channel || channel==subs[i].channel) {
                subs[i].callback(value);
            }
        }
    }
}

class PROJ_EPSG_3857 {

    constructor() {
        this.name = "EPSG:3857";
        this.C1 = 20037508.34;
    }

    fromLonLat(lon_lat) {
        var lon = lon_lat["lon"];
        var lat = lon_lat["lat"];
        var e = lon * this.C1 / 180;
        var n = Math.log(Math.tan((90+lat) * Math.PI / 360.0)) / (Math.PI / 180);
        n = n * this.C1 / 180;
        return {"e":e,"n":n};
    }

    toLonLat(e_n) {
        var e = e_n["e"];
        var n = e_n["n"];
        var lon = e * 180 / this.C1;
        var lat = n * 180 / this.C1;
        lat = 180/Math.PI * (2 * Math.atan(Math.exp(lat*math.PI/180)) - math.PI/2);
        return {"lat":lat,"lon":lon};
    }
}
