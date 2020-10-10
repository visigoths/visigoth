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

import bisect

class Search(object):

    @staticmethod
    def binary_search(sorted_list,value):
        """
        Search for nearest value in a sorted list of numeric values.
        It is assumed that there are no repeated values in the list.

        If there are ties, return the lowest index

        :param sorted_list: list of numeric values, sorted
        :param value: value to search for
        :return: (index,nearest-value) pair
        """
        index = bisect.bisect(sorted_list,value)
        if index >= len(sorted_list):
            return (len(sorted_list)-1,sorted_list[-1])
        elif index == 0:
            return (0,sorted_list[0])
        else:
            diff0 = abs(value-sorted_list[index-1])
            diff1 = abs(value-sorted_list[index])
            if diff0 <= diff1:
                return (index-1,sorted_list[index-1])
            else:
                return (index, sorted_list[index])

        return sorted_list[index-1], sorted_list[index]



