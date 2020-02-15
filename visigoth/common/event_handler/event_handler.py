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

from visigoth.utils.js import Js
from visigoth.common.diagram_element import DiagramElement

import os
import math

class EventHandler(DiagramElement):
    """
    Create an event handler based on a javascript function

    Arguments:
        js(str) : javascript function of the form function(channel,event,config,sendfn) { /* body */ }
        config(dict) : configuration passed into each invocation (must be JSON serialisable)

    Notes:
        The function is invoked with the following parameters:

        channel is the name of the channel upon which the event is recieved
        obj is the event value
        config is the configuration of the function (this can be mutated between invocations)
        sendfn is a function for sending events which takes parameters obj (the event value) and channel (the name of the channel to output the event to)
    """

    counter = 0

    def __init__(self,js,config={}):
        DiagramElement.__init__(self)
        self.js = js
        self.config = config

    def build(self):
        pass

    def getWidth(self):
        return 0

    def getHeight(self):
        return 0

    def draw(self,d,cx,cy):
        config = self.config
        with open(os.path.join(os.path.split(__file__)[0],"event_handler.js"),"r") as jsfile:
            jscode = jsfile.read()
        cls = "event_handler_"+str(EventHandler.counter)
        EventHandler.counter += 1
        jscode = jscode.replace("<<CLASS_NAME>>",cls)
        jscode = jscode.replace("<<HANDLER_FN>>",self.js)
        Js.registerJs(d,self,jscode,cls,cx,cy,config)

