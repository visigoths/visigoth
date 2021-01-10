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

from visigoth.charts import ChartElement
from visigoth.common.axis import Axis
from visigoth.svg import text,polygon,linear_gradient,group
from visigoth.utils.colour import DiscreteColourManager
from visigoth.utils.data import Dataset

class Transition(ChartElement):

    def __init__(self, data, label=0, states=[], width=768, height=768,  colour_manager=None, transition_labels=[],  stroke="black", stroke_width=1, x_axis_label="",y_axis_label="count", font_height=16, text_attributes={}):
        """
        Add a Transition plot

        Arguments:
            data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)
            label (str or int): Identify the column to define the label
            states (list of str or int): The columns to define successive states at each transition point
            width(int): the width of the plot in pixels
            height(int): the height of the plot in pixels
            colour_manager(DiscreteColourManager): a DiscreteColourManager object
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
        self.colour_manager = None
        dataset = Dataset(data)
        if states == []:
            states = list(range(1,len(data[0])))
        if transition_labels == []:
            transition_labels = list(map(lambda s:str(s),states))
        self.data = { row[0]: row[1:] for row in dataset.query([label]+states)}
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

        # order categories according to the colour_manager order
        self.category_order = [c for (c,col) in colour_manager.getCategories()]

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

        if colour_manager == None:
            colour_manager = DiscreteColourManager()
        self.setPalette(colour_manager)

        # make sure that all categories are added to the colour_manager
        for cat in self.categories:
            if cat != "":
                self.getPalette().allocateColour(cat)

        ay = Axis(self.height-self.font_height,"vertical",0,len(self.keys),label=self.y_axis_label,font_height=self.font_height,text_attributes=self.text_attributes)
        self.setAxes(None,ay)
        self.setMargins(0,self.font_height)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getColourForCategory(self,cat):
        if cat == "":
            # flows going through the missing category should be coloured transparent white
            return "#FFFFFF00"
        else:
            return self.getPalette().getColour(cat)

    def defineGradient(self,d,cat0,cat1):
        if (cat0,cat1) in self.gradients:
            return self.gradients[(cat0,cat1)]
        lg = linear_gradient(self.getColourForCategory(cat0),self.getColourForCategory(cat1))
        d.add(lg)
        lgid = lg.getId()
        self.gradients[(cat0,cat1)] = lgid
        return lgid

    def drawTransitionGroup(self,diagram,group,axis_x0,axis_x1,oy,width,height,state,tooltip):
        (pcat0, pcat1, (pidx_min, pidx_max), (poidx_min, poidx_max)) = state
        if pcat0 == pcat1:
            fill = self.getColourForCategory(pcat0)
        else:
            fill = "url(#"+self.defineGradient(diagram,pcat0,pcat1)+")"
        p = polygon([(axis_x0, oy + pidx_min * height),("C"),(axis_x0 + width, oy + pidx_min * height),(axis_x1 - width, oy + poidx_min * height),
                     (axis_x1, oy + poidx_min * height),("L"),
                     (axis_x1, oy + poidx_max * height + height),("C"), (axis_x1 - width, oy + poidx_max * height + height),(axis_x0 + width, oy + pidx_max * height + height),
                     (axis_x0, oy + pidx_max * height + height)], fill, self.stroke, self.stroke_width, tooltip)
        group.add(p)
        return p.getId()

    def drawChart(self,d,cx,cy,chart_width,chart_height):
        oy = cy - chart_height/2
        ox = cx - chart_width/2

        item_height = chart_height / len(self.keys)

        # compute width of each transition "plot"
        plot_width = chart_width / len(self.transitions)

        # x axis labels are the names of each transition point
        # draw a label at the top and bottom
        for transition_label_y in [oy - self.font_height/2, oy+chart_height+self.font_height/2]:
            # and for each transition...
            for transition in range(0,len(self.transitions)+1):
                transition_label_x = ox + transition * plot_width
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
        ay = 0
        for transition in range(0,len(self.transitions)):
            transition_x0 = ox+transition*plot_width
            transition_x1 = ox+(transition+1)*plot_width

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

        return {"categories":self.ids_by_category}