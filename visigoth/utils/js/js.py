# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

import json

class Js(object):

    subscribe_template = """
        pubsubs_subscribe("%(source)s","%(sourceChannel)s",
            function(obj) { 
                try {
                    var adapter = %(adapterFunction)s; 
                    %(instance)s.recieve(adapter(obj),"%(destChannel)s"); 
                } catch(ex) { 
                    console.log(ex); 
                }
            }
        );
     """

    registered = set()

    @staticmethod
    def getInstanceName(elementId):
        return "%s_js"%(elementId)

    @staticmethod
    def registerJs(doc,targetElement,jscode,classname,x,y,config,constructInstance=True):
        if doc.getFormat() != "html":
            return
        if jscode not in doc.getCodeCache():
            doc.addCode(jscode)
            doc.getCodeCache()[jscode] = True
        if constructInstance:
            Js.constructJs(doc,targetElement,classname,x,y,config)
        Js.registered.add(targetElement)

    @staticmethod
    def isRegistered(targetElement):
        return targetElement in Js.registered

    @staticmethod
    def constructJs(doc,targetElement,classname,x,y,config):
        eid = targetElement.getId()
        sendfn = "function(payload,channel) { pubsubs_publish(\"%s\",payload,channel); }"%(eid)
        instanceName = Js.getInstanceName(eid)
        doc.addCode("var %s = new %s(\"%s\",%d,%d,%f,%f,%s,%s);"%(instanceName,classname,eid,targetElement.getWidth(),targetElement.getHeight(),x,y,sendfn,json.dumps(config)))

    @staticmethod
    def connect(doc,sourceElement,sourceChannel,destElement,destChannel,adapter_fn):
        source = sourceElement.getId()
        dest = destElement.getId()
        instanceName = Js.getInstanceName(dest)
        recfn = Js.subscribe_template%{
            "source":source,
            "sourceChannel":sourceChannel,
            "destChannel":destChannel,
            "instance":instanceName,
            "adapterFunction":adapter_fn}
        doc.addCode(recfn)
