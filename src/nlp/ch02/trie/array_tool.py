# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-07-13
    FileName   : array_tool.py
    Author     : Honghe
    Descreption: 
"""

class ArrayTool:
    @staticmethod
    def binary_search(branches, node):
        high = len(branches) - 1
        if len(branches)<1:
            return high
        low = 0
        while low<=high:
            mid = (low+high)>>1
            cmp = branches[mid].compare_to(node)
            if cmp<0:
                low = mid + 1
            elif cmp>0:
                high = mid - 1
            else:
                return mid
        return -(low+1)


