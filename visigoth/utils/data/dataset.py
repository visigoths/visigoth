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
        if val is not None:
            return acc+val
        else:
            return acc

    def finalise(self,acc):
        return acc

class MinFunction(object):

    def __init__(self):
        pass

    def initialValue(self):
        return None

    def accumulate(self,acc,val):
        if acc == None or (val is not None and val < acc):
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
        if acc == None or (val is not None and val > acc):
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


class CountNoneFunction(object):

    def __init__(self):
        pass

    def initialValue(self):
        return 0

    def accumulate(self, acc, val):
        if val is None:
            return acc + 1
        else:
            return acc

    def finalise(self, acc):
        return acc

class AggregationFunction(object):

    def __init__(self,fn,column=None):
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

    def __len__(self):
        return len(self.data)

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
    def count_none(column):
        return AggregationFunction(CountNoneFunction(),column)

    @staticmethod
    def filter(column,op,literal):
        if op == "=" or op == "==":
            return EqualityFilter(column,literal)
        raise Exception("invalid filter operation:"+op)

    def getColumns(self):
        columns = []
        for row in self.data:
            if isinstance(row,tuple) or isinstance(row,list):
                if len(columns) < len(row):
                    columns = list(range(0,len(row)))
            elif isinstance(row,dict):
                for key in row:
                    if key not in columns:
                        columns.append(key)
        return columns

    def isDiscrete(self,column):
        # FIXME currently mark a column as discrete if values are of type str
        # we need also to consider int columns of "low" cardinality as discrete
        for datum in self.data:
            if isinstance(datum,dict) and not column in datum:
                continue
            if datum[column] == None:
                continue
            if isinstance(datum[column],str):
                return True
            else:
                return False
        return False

    def query(self,columns=[],unique=False,filters=[],aggregations=[],flatten=False):
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
                if column is None:
                    row.append(None)
                elif isinstance(column,Constant):
                    row.append(column.value())  
                elif isinstance(column,int) and column < len(datum):
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

        if aggregations:
            rows2 = []
            for tup in rows:
                if tup not in rows2:
                    rows2.append(tup)
            rows = rows2

        results = []
        for tup in rows:
            result = tup
            for aggregation in aggregations:
                result += aggregation.finalise(tup)
            if flatten:
                results += result
            else:
                results.append(result)
        return results