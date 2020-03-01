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

class Constant(object):

    def __init__(self,val):
        self.val = val

    def value(self):
        return self.val

class SumFunction(object):

    def __init__(self):
        pass

    def initialValue(self):
        return 0

    def accumulate(self,acc,val):
        return acc+val

    def finalise(self,acc):
        return acc

class MinFunction(object):

    def __init__(self):
        pass

    def initialValue(self):
        return None

    def accumulate(self,acc,val):
        if acc == None or val < acc:
            return val
        else:
            return acc

    def finalise(self,acc):
        return acc

class MaxFunction(object):

    def __init__(self):
        pass

    def initialValue(self):
        return None

    def accumulate(self,acc,val):
        if acc == None or val > acc:
            return val
        else:
            return acc

    def finalise(self,acc):
        return acc

class CountFunction(object):
    
    def __init__(self):
        pass

    def initialValue(self):
        return 0

    def accumulate(self,acc):
        return acc + 1

    def finalise(self,acc):
        return acc

class AggregationFunction(object):

    def __init__(self,fn,column):
        self.fn = fn
        self.column = column
        self.accumulators = {}

    def aggregate(self,key,row):
        if key not in self.accumulators:
            self.accumulators[key] = self.fn.initialValue() 

        if self.column != None:
            self.accumulators[key] = self.fn.accumulate(self.accumulators[key],row[self.column])
        else:
            self.accumulators[key] = self.fn.accumulate(self.accumulators[key])

    def finalise(self,key):
        return (self.fn.finalise(self.accumulators[key]),)
        
class EqualityFilter(object):

    def __init__(self,column,literal):
        self.column = column
        self.literal = literal

    def allow(self,datum):
        return datum[self.column] == self.literal

class Dataset(object):

    def __init__(self,data):
        self.data = data

    @staticmethod
    def constant(val):
        return Constant(val)

    @staticmethod
    def sum(column):
        return AggregationFunction(SumFunction(),column)

    @staticmethod
    def min(column):
        return AggregationFunction(MinFunction(),column)

    @staticmethod
    def max(column):
        return AggregationFunction(MaxFunction(),column)

    @staticmethod
    def count():
        return AggregationFunction(CountFunction())

    @staticmethod
    def filter(column,op,literal):
        if op == "=" or op == "==":
            return EqualityFilter(column,literal)
        raise Exception("invalid filter operation:"+op)

    def isDiscrete(self,column):
        # FIXME currently mark a column as discrete if values are of type str
        # we need also to consider int columns of "low" cardinality as discrete
        for datum in self.data:
            if column in datatum:
                if datum[column] == None:
                    continue
                if isinstance(datum[column],str):
                    return True
                else:
                    return False
        return False

    def query(self,columns=[],unique=False,filters=[],aggregations=[]):
        rows = []
        if columns == []:
            unique = True
        for datum in self.data:
            row = []
            filtered = False
            for filter in filters:
                if not filter.allow(datum):
                    filtered = True
                    break
            if filtered:
                continue
            for column in columns:
                if column == None:
                    row.append(None)
                elif isinstance(column,Constant):
                    row.append(column.value())  
                elif isinstance(column,int):
                    row.append(datum[column])
                elif column in datum:
                    row.append(datum[column])
                else:
                    row.append(None)
            tup = tuple(row)   
            if not unique or tup not in rows: 
                rows.append(tup)
            for aggregation in aggregations:
                aggregation.aggregate(tup,datum)

        results = []
        for tup in rows:
            result = tup
            for aggregation in aggregations:
                result += aggregation.finalise(tup)
            results.append(result)
        return results