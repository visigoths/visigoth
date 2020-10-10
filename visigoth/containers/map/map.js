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

// Returns the inverse of matrix `M`.  See http://blog.acipo.com/matrix-inversion-in-javascript/ for full version
function matrix_invert(M){
    if(M.length !== M[0].length){return;}
    var i=0, ii=0, j=0, dim=M.length, e=0, t=0;
    var I = [], C = [];
    for(i=0; i<dim; i+=1){

        I[I.length]=[];
        C[C.length]=[];
        for(j=0; j<dim; j+=1){
            if(i==j){ I[i][j] = 1; }
            else{ I[i][j] = 0; }
            C[i][j] = M[i][j];
        }
    }

    for(i=0; i<dim; i+=1){
        e = C[i][i];
        if(e==0){
            for(ii=i+1; ii<dim; ii+=1){
                if(C[ii][i] != 0){
                    for(j=0; j<dim; j++){
                        e = C[i][j];
                        C[i][j] = C[ii][j];
                        C[ii][j] = e;
                        e = I[i][j];
                        I[i][j] = I[ii][j];
                        I[ii][j] = e;
                    }
                    break;
                }
            }
            e = C[i][i];
            if(e==0){return}
        }

        for(j=0; j<dim; j++){
            C[i][j] = C[i][j]/e;
            I[i][j] = I[i][j]/e;
        }

        for(ii=0; ii<dim; ii++){
            if(ii==i){continue;}

            e = C[ii][i];


            for(j=0; j<dim; j++){
                C[ii][j] -= e*C[i][j];
                I[ii][j] -= e*I[i][j];
            }
        }
    }

    return I;
}

class map {

    constructor(id,width,height,cx,cy,sendfn,config) {
        this.matrix = [1,0,0,1,0,0];
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

        var width = this.width/this.zoom_level;
        var height = this.height/this.zoom_level;

        var m = [[this.matrix[0],this.matrix[2],this.matrix[4]],[this.matrix[1],this.matrix[3],this.matrix[5]],[0,0,1]];
        var im = matrix_invert(m);

        var cx = (im[0][0] * this.cx) + (im[0][1] * this.cy) + im[0][2];
        var cy = (im[1][0] * this.cx) + (im[1][1] * this.cy) + im[1][2];

        this.sendfn({"cx":cx, "cy":cy, "width":width, "height":height},"visible_window");
    }

    move(dx,dy) {
        this.matrix[4] += dx;
        this.matrix[5] += dy;

        this.updateTransform();
        this.sendVisibleWindowUpdate();
    }

    zoom(newzoom) {
        var scale = newzoom / this.zoom_level;
        for(var i=0; i<6; i++) {
            this.matrix[i] *= scale;
        }
        console.log("center cx="+this.cx+"cy="+this.cy);

        this.matrix[4] += (1 - scale) * this.cx;
        this.matrix[5] += (1 - scale) * this.cy;
        this.zoom_level = newzoom;

        this.updateTransform();
        this.sendfn(this.zoom_level,"zoom");
        this.sendVisibleWindowUpdate();
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

        var transform = "matrix(" +  this.matrix.join(' ') + ")";

        this.layerGroup.setAttribute("transform",transform);
        this.popGroup.setAttribute("transform",transform);
    }

    recieve(obj,channel) {
        if (channel == "search") {
            this.sendfn(obj,"search");
        }
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