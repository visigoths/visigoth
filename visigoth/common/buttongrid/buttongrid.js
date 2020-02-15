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

class buttongrid {

    constructor(id,width,height,x,y,sendfn,config) {
        this.id = id;
        this.width = width;
        this.height = height;
        this.x = x;
        this.y = y;
        this.sendfn = sendfn;
        this.config = config;
    }

    recieve(obj,channel) {
        // alert("bg:channel="+channel+":obj="+obj)
        if (channel == "click") {
            this.sendfn(obj,"click");
        } else {
            var selected_button_channel = channel;
            var button_channels = this.config["button_channels"];
            this.sendfn("select",selected_button_channel);
            for(var idx=0; idx<button_channels.length; idx++) {
                var button_channel = button_channels[idx];
                if (button_channel != selected_button_channel) {
                    this.sendfn("deselect",button_channel);
                }
            }
        }
    }
}