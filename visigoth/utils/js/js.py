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

import json

from visigoth.svg import javascript_snippet

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
        if jscode not in doc.getCodeCache():
            doc.add(javascript_snippet(jscode))
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
