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

from visigoth.charts import ChartElement
from visigoth.utils.elements.axis import Axis
from visigoth.svg import text,polygon,linear_gradient,group

class Transition(ChartElement):

    def __init__(self, width, height, data, palette,transition_labels,  stroke="black", stroke_width=1, x_axis_label="",y_axis_label="count", font_height=16, text_attributes={}):
        """
        Add a Transition plot

        Arguments:
            width(int): the width of the plot in pixels
            height(int): the height of the plot in pixels
            data(dict): data describing a set of transitions in the form of a dictionary mapping an item id to a tuple(category0,category1,...) denoting a transition between categories
            palette(DiscretePalette): a DiscretePalette object
            transition_labels(list): list containing the labels for each of the transition points

        Keyword Arguments:
            x_axis_label(str) : label for the x axis
            y_axis_label(str) : label for the y axis
            stroke (str): stroke color for circumference of points
            stroke_width (int): stroke width for circumference of points
            font_height (int): the height of the font for text labels
            text_attributes (dict): SVG attribute name value pairs to apply to labels
        """

        super(Transition,self).__init__()
        self.width = width
        self.height = height
        self.palette = None
        self.data = data
        self.transition_labels = transition_labels
        self.x_axis_label = x_axis_label # TODO currently unused
        self.y_axis_label = y_axis_label
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.category_counts = []
        self.categories = set()
        self.gradients = {}
        self.stroke = stroke
        self.stroke_width = stroke_width
        for key in self.data:
            cats = self.data[key]
            for i in range(0,len(cats)):
                while i >= len(self.category_counts):
                    self.category_counts.append({})
                cat = cats[i]
                self.categories.add(cat)
                if cat not in self.category_counts[i]:
                    self.category_counts[i][cat] = 0
                self.category_counts[i][cat] += 1

        self.keys = sorted([key for key in self.data])
        self.transition_count = len(self.category_counts)-1

        # order categories according to the palette order
        self.category_order = [c for (c,col) in palette.getCategories()]

        # data structure mapping from category to a list of SVG ids, supporting brushing
        self.ids_by_category = { cat:[] for cat in self.category_order}

        # if some instances are assigned missing category "", add this to the bottom of the order
        if "" in self.categories:
            self.category_order.append("")

        # construct the transitions
        self.transitions = []

        for transition in range(0,self.transition_count):
            self.transitions.append(([],[]))
            for side in [0, 1]:
                otherside = 1 - side
                for cat0 in self.category_order:
                    for cat1 in self.category_order:
                        for key in self.keys:
                            catA = self.data[key][transition+side]
                            catB = self.data[key][transition+otherside]
                            if catA == cat0 and catB == cat1:
                                self.transitions[transition][side].append(key)

        self.palette = {k: col for (k, col) in palette.getCategories()}

        # flows going through the missing category should be coloured transparent white
        self.palette[""] = "#FFFFFF00"

        self.ay = Axis(self.height-self.font_height,"vertical",0,len(self.keys),label=self.y_axis_label,font_height=self.font_height,text_attributes=self.text_attributes)
        self.ay.build()

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getXAxis(self):
        return None

    def getYAxis(self):
        return self.ay

    def defineGradient(self,d,cat0,cat1):
        if (cat0,cat1) in self.gradients:
            return self.gradients[(cat0,cat1)]
        lg = linear_gradient(self.palette[cat0],self.palette[cat1])
        d.add(lg)
        lgid = lg.getId()
        self.gradients[(cat0,cat1)] = lgid
        return lgid

    def drawTransitionGroup(self,diagram,group,axis_x0,axis_x1,oy,width,height,state,tooltip):
        (pcat0, pcat1, (pidx_min, pidx_max), (poidx_min, poidx_max)) = state
        if pcat0 == pcat1:
            fill = self.palette[pcat0]
        else:
            fill = "url(#"+self.defineGradient(diagram,pcat0,pcat1)+")"
        p = polygon([(axis_x0, oy + pidx_min * height),("C"),(axis_x0 + width, oy + pidx_min * height),(axis_x1 - width, oy + poidx_min * height),
                     (axis_x1, oy + poidx_min * height),("L"),
                     (axis_x1, oy + poidx_max * height + height),("C"), (axis_x1 - width, oy + poidx_max * height + height),(axis_x0 + width, oy + pidx_max * height + height),
                     (axis_x0, oy + pidx_max * height + height)], fill, self.stroke, self.stroke_width, tooltip)
        group.add(p)
        return p.getId()

    def drawChart(self,d,cx,cy):
        oy = cy - self.height/2
        ox = cx - self.width/2

        # compute the width of chart without the y-axis
        chart_width = self.width - self.ay.getWidth()
        # ... and the height of the chart without the x-axis labels
        chart_height = self.height - self.font_height

        item_height = chart_height / len(self.keys)

        # compute width of each transition "plot"
        plot_width = chart_width / len(self.transitions)

        # labels
        ay = self.font_height
        for transition in range(0,len(self.transitions)+1):
            transition_label_x = ox + self.ay.getWidth() + transition * plot_width
            transition_label_y = oy + self.font_height/2
            t = text(transition_label_x, transition_label_y, self.transition_labels[transition])
            t.addAttrs(self.text_attributes)
            t.addAttr("font-size", self.font_height)
            if transition == 0:
                pos = "start"
            elif transition == len(self.transitions):
                pos = "end"
            else:
                pos = "middle"
            t.addAttr("text-anchor", pos)
            t.setVerticalCenter()

            d.add(t)

        grp = group()
        d.add(grp)

        transition_width = chart_width/(2*len(self.transitions))

        # transition curves
        for transition in range(0,len(self.transitions)):
            transition_x0 = ox+self.ay.getWidth()+transition*plot_width
            transition_x1 = ox+self.ay.getWidth()+(transition+1)*plot_width

            points0 = self.transitions[transition][0]
            points1 = self.transitions[transition][1]

            state = None
            for idx in range(0,len(points0)):
                key = points0[idx]
                cat0 = self.data[key][transition]
                cat1 = self.data[key][transition+1]
                oidx = points1.index(key)
                if state == None:
                    state = (cat0,cat1,(idx,idx),(oidx,oidx))
                else:
                    (pcat0,pcat1,(pidx_min,pidx_max),(poidx_min,poidx_max)) = state
                    if cat0 == pcat0 and cat1 == pcat1:
                        state = (cat0,cat1,(pidx_min,idx),(min(oidx,poidx_min),max(oidx,poidx_max)))
                    else:
                        count = 1 + pidx_max - pidx_min
                        svgid = self.drawTransitionGroup(d,grp,transition_x0,transition_x1,ay+oy,transition_width,item_height,state,pcat0+"=>"+pcat1+"(%d)"%(count))
                        if cat0:
                            self.ids_by_category[cat0].append(svgid)
                        if cat1 and cat1 != cat0:
                            self.ids_by_category[cat1].append(svgid)
                        state = (cat0, cat1, (idx, idx), (oidx, oidx))

            if state != None:
                (pcat0, pcat1, (pidx_min, pidx_max), (poidx_min, poidx_max)) = state
                count = 1 + pidx_max - pidx_min
                svgid = self.drawTransitionGroup(d,grp,transition_x0, transition_x1, ay+oy, transition_width, item_height, state, pcat0 + "=>" + pcat1+"(%d)"%(count))
                if pcat0:
                    self.ids_by_category[cat0].append(svgid)
                if pcat1 and pcat1 != pcat0:
                    self.ids_by_category[cat1].append(svgid)

        # y-axis
        self.ay.draw(d,cx-self.width/2+self.ay.getWidth()/2,oy+self.font_height+self.ay.getHeight()/2)

        return {"categories":self.ids_by_category}