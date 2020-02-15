# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

import unittest

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.common.button import Button
from visigoth.common.event_handler import EventHandler

jscode = """
function(channel,obj,config,sendfn)
{
    alert("Got event:"+obj+" on channel "+channel);
}
"""

class TestEventHandler(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")
        b = Button("Test")
        d.add(b)
        ev = EventHandler(jscode,{})
        d.add(ev)
        d.connect(b,"events",ev,"events")
        svg = d.draw()
        TestUtils.output(svg,"test_event_handler.svg")
