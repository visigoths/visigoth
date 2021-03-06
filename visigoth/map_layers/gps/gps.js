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

class gps {

    constructor(id,width,height,x,y,sendfn,config) {
        this.id = id;
        this.width = width;
        this.height = height;
        this.x = x;
        this.y = y;
        this.sendfn = sendfn;
        this.config = config;

        this.proj = new PROJ_EPSG_3857();

        var ne_min = this.proj.fromLonLat({"lat":this.config["lat_min"],"lon":this.config["lon_min"]});
        
        this.e_min = ne_min["e"];
        this.n_min = ne_min["n"];

        var ne_max = this.proj.fromLonLat({"lat":this.config["lat_max"],"lon":this.config["lon_max"]});
        
        this.e_max = ne_max["e"];
        this.n_max = ne_max["n"];

        var mid_lat = this.config.lat_min+(this.config.lat_max-this.config.lat_min)/2;
        var mid_lon = this.config.lon_min+(this.config.lon_max-this.config.lon_min)/2;

        // this.showMarker(mid_lon,mid_lat);

        var errorCB = function(error) {
            console.log('gps layer error(' + error.code + '): ' + error.message);
        };

        if ("geolocation" in navigator) {
            var that =this;
            this.watchID = navigator.geolocation.watchPosition(function(position) {
                that.showMarker(position.coords.longitude, position.coords.latitude);
            },errorCB);
        }
    }

    showMarker(lon,lat) {
        console.log("marker:"+lon+","+lat);
        if (lon < this.config.lon_min || lon > this.config.lon_max) {
            return;
        }
        if (lat < this.config.lat_min || lat > this.config.lat_max) {
            return;
        }
        
        var ne_mid = this.proj.fromLonLat({"lat":lat,"lon":lon});
        this.e = ne_mid["e"];
        this.n = ne_mid["n"];
        
        var px = this.x - this.width/2 + this.width*(this.e - this.e_min)/(this.e_max-this.e_min);
        var py = this.y + this.height/2 - this.height*(this.n - this.n_min)/(this.n_max-this.n_min);
        
        this.marker = document.getElementById(this.config["marker_id"]);
        this.marker.setAttribute("cx",px);
        this.marker.setAttribute("cy",py);
        this.marker.removeAttribute("visibility");
    }

    zoom(zoom_level) {
        
    }

    recieve(obj,channel) {
        if (channel == "zoom") {
            this.zoom(obj);
        }
    }
    
}