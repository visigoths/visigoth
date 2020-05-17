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

from .map_layer import MapLayer

from .cartogram import Cartogram
from .chloropleth import Chloropleth
from .cluster import Cluster
from .compass import Compass
from .contour import Contour
from .geoimport import Geoimport
from .geoplot import Geoplot
from .gps import GPS
from .hexbin import Hexbin
from .kde import KDE
from .poi import POI
from .network import Network
from .ruler import Ruler
from .scatter import Scatter
from .voronoi import Voronoi
from .wms import WMS
from .wmts import WMTS
