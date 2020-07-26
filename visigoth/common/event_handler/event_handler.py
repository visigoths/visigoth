# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#   and associated documentation files (the "Software"), to deal in the Software without 
#   restriction, including without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all copies or 
#   substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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

    def build(self,fmt):
        pass

    def getWidth(self):
        return 0

    def getHeight(self):
        return 0

    def draw(self,d,cx,cy):
        if d.getFormat() != "html":
            return
        config = self.config
        with open(os.path.join(os.path.split(__file__)[0],"event_handler.js"),"r") as jsfile:
            jscode = jsfile.read()
        cls = "event_handler_"+str(EventHandler.counter)
        EventHandler.counter += 1
        jscode = jscode.replace("<<CLASS_NAME>>",cls)
        jscode = jscode.replace("<<HANDLER_FN>>",self.js)
        Js.registerJs(d,self,jscode,cls,cx,cy,config)

