# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.common import Space
from visigoth.map_layers import WMS, POI

tweets = [{"id": "1094594877923491840", "lon": -0.28002518, "lat": 51.55696202},
    {"id": "1094595003945488384", "lon": -0.11993334, "lat": 51.53098437},
    {"id": "1094595017631514624", "lon": -0.12731805, "lat": 51.50711486},
    {"id": "1094595262889291777", "lon": -0.48618965, "lat": 51.4718463},
    {"id": "1094595309081116672", "lon": -0.126, "lat": 51.551},
    {"id": "1094595530804449280", "lon": -0.1317595, "lat": 51.50830388},
    {"id": "1094595627860746241", "lon": -0.12731805, "lat": 51.50711486},
    {"id": "1094596872352624640", "lon": -0.12731805, "lat": 51.50711486}]

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    d = Diagram(fill="white",margin_left=200,margin_right=200)
    poi = POI()
    for tweet in tweets:
        poi.addTweet(tweet["id"],tweet["lon"],tweet["lat"])
 
    m1 = Map(512,width_to_height=1)
    m1.addLayer(WMS(type="osm"))
    m1.addLayer(poi)
    d.add(Space(100))
    d.add(Box(m1))

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

