# -*- coding: utf-8 -*-

class Metadata(object):

    def __init__(self,name="",attribution="",url="",description=""):
        self.name = name
        self.attribution = attribution
        self.url = url
        self.description = description

    def getName(self):
        return self.name

    def getAttribution(self):
        return self.attribution

    def getUrl(self):
        return self.url

    def getDescription(self):
        return self.description

    def setDetails(self,name,description="",attribution="",url=""):
        if name:
            self.name = name
        if description:
            self.description = description
        if attribution:
            self.attribution = attribution
        if url:
            self.url = url